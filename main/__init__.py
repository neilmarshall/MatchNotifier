import datetime
import logging
import os
from itertools import groupby

import azure.functions as func
from azure.data.tables import TableServiceClient

from email_client.email_client import send_email
from fixture_parser.get_fixtures import get_fixtures


def main(mytimer: func.TimerRequest) -> None:
    try:
        table_client = TableServiceClient.from_connection_string(conn_str=os.environ["AzureWebJobsStorage"])
        table = table_client.get_table_client(os.environ["TableName"])

        fixtures_URL = os.environ.get("FixturesURL")

        entities = sorted(table.list_entities(), key=lambda o: o['PartitionKey'])
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
                    home_team, away_team, matchdate = fixture
                    body.append(f"{home_team} vs. {away_team}, {matchdate.hour % 12}:{matchdate.minute:02}{'AM' if matchdate.hour < 12 else 'PM'}")
                subject = "Fixture Notification"
                send_email(subject, '\n'.join(body), email)
            else:
                logging.info("No fixtures found today")
    except Exception as ex:
        logging.error(ex)
