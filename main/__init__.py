import datetime
import logging
import os

import azure.functions as func

from email_client.email_client import send_email
from fixture_parser.get_fixtures import get_fixtures


# TODO: deal with fixtures that have expired, i.e. full-time scored fixtures
# TODO: allow multiple competitions / teams in configuration
def main(mytimer: func.TimerRequest) -> None:
    try:
        fixtures_URL = os.environ.get("FixturesURL")
        competition_name = os.environ.get("CompetitionName")
        team_name = os.environ.get("TeamName")
        fixture = get_fixtures(fixtures_URL, competition_name, team_name)
        if fixture is not None:
            logging.info(f"Fixture found: {fixture}")
            home_team, away_team, matchdate = fixture
            subject = "Fixture Notification"
            body = f"{home_team} vs. {away_team}, {matchdate.hour % 12}:{matchdate.minute}{'AM' if matchdate < 12 else 'PM'}"
            recipient = os.environ["EmailRecipientAddress"]
            send_email(subject, body, recipient)
        else:
            logging.info(f"No fixtures found today for {team_name} in the {competition_name}")
    except Exception as ex:
        logging.error(ex)
