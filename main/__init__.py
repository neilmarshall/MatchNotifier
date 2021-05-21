import json
import logging
from datetime import datetime, timedelta
from itertools import groupby

import azure.functions as func
from azure.data.tables import TableServiceClient
from azure.storage.queue import BinaryBase64EncodePolicy, QueueClient, QueueServiceClient
from dateutil.tz import gettz

from configuration_manager import Config
from email_client.email_client import send_email
from fixture_parser.get_fixtures import get_fixtures


def get_timeout(year, month, day, hour, minute, *, tz='BST', offset=3600):
    dt_local = datetime(year, month, day, hour, minute, tzinfo=gettz(tz))
    return (dt_local - timedelta(seconds=offset) - datetime.now(gettz(tz))).seconds


def enqueue_notifcation(queue_client, recipient, competition, home_team, away_team, matchdate):
    try:
        content = json.dumps({
            'recipient': recipient,
            'competition': competition,
            'homeTeam': home_team,
            'awayTeam': away_team,
            'matchdate': matchdate.isoformat()
        })
        visibility_timeout = get_timeout(matchdate.year, matchdate.month, matchdate.day, matchdate.hour, matchdate.minute)
        logging.info(f"Enqueueing notification with time delay {visibility_timeout} seconds")
        if visibility_timeout > 0:
            encoded_content = BinaryBase64EncodePolicy().encode(content.encode('utf-8'))
            queue_client.send_message(encoded_content, visibility_timeout=visibility_timeout)
    except Exception as ex:
        logging.error(ex, exc_info=True, stack_info=True)


def main(mytimer: func.TimerRequest) -> None:
    try:
        config = Config()

        table_service_client = TableServiceClient.from_connection_string(conn_str=config.get_connection_string())
        table_client = table_service_client.get_table_client(config.parameters["TableName"])

        queue_service_client = QueueServiceClient.from_connection_string(conn_str=config.get_connection_string())
        queue_client = queue_service_client.get_queue_client(config.parameters["QueueName"])

        fixtures_URL = config.parameters["FixturesURL"]

        entities = sorted(table_client.list_entities(), key=lambda o: o['PartitionKey'])
        for email, _entities in groupby(entities, key=lambda o: o['PartitionKey']):
            fixture_filter = {}
            grouped_entities = sorted(_entities, key=lambda o: o['CompetitionName'])
            for competition_name, _grouped_entities in groupby(grouped_entities, key=lambda o: o['CompetitionName']):
                team_names = [o['TeamName'] for o in _grouped_entities]
                fixture_filter[competition_name] = team_names

            fixtures = get_fixtures(fixtures_URL, fixture_filter)

            if fixtures:
                body = []
                for fixture in fixtures:
                    logging.info(f"Fixture found: {fixture}")
                    competition, home_team, away_team, matchdate = fixture
                    timestamp = f"{matchdate.hour % 12 if matchdate.hour > 12 else matchdate.hour}:{matchdate.minute:02}{'AM' if matchdate.hour < 12 else 'PM'}"
                    body.append(f"{competition} - {home_team} vs. {away_team}, {timestamp}")
                    logging.info("Enqueueing notification...")
                    enqueue_notifcation(queue_client, email, competition, home_team, away_team, matchdate)
                subject = "Fixture Notification"
                send_email(subject, '\n'.join(body), email)
            else:
                logging.info("No fixtures found today")
    except Exception as ex:
        logging.error(ex, exc_info=True, stack_info=True)
