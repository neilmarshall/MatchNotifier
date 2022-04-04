import json
import logging
import os

from dotenv import load_dotenv

from email_client.email_client import send_email
from fixture_parser.get_fixtures import get_fixtures

load_dotenv()

log_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.environ["LOG_FOLDER_PATH"])
if not os.path.exists(log_folder_path):
    os.mkdir(log_folder_path)
logging.basicConfig(filename=os.path.join(log_folder_path, os.environ["LOG_FILENAME"]), level=logging.INFO, format='%(levelname)s:%(name)s:%(asctime)s:%(message)s')
logger = logging.getLogger(__name__)

def get_config():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')) as f:
        return json.load(f)


def main():
    try:
        config = get_config()

        fixtures_URL = config["fixtures_URL"]

        for email, entities in config["entities"].items():
            fixture_filter = {}
            for competition_name, team_names in entities.items():
                fixture_filter[competition_name] = team_names

            fixtures = get_fixtures(fixtures_URL, fixture_filter)

            if fixtures:
                body = []
                for fixture in fixtures:
                    logger.info(f"Fixture found - {fixture}")
                    competition, home_team, away_team, matchdate = fixture
                    timestamp = f"{matchdate.hour % 12 if matchdate.hour > 12 else matchdate.hour}:{matchdate.minute:02}{'AM' if matchdate.hour < 12 else 'PM'}"
                    body.append(f"{competition} - {home_team} vs. {away_team}, {timestamp}")
                subject = "Fixture Notification"
                # TODO - uncomment this line once ready
                # send_email(subject, '\n'.join(body), email)
            else:
                logger.info(f"No fixtures found today - {fixture_filter}")
    except Exception as ex:
        logger.error(ex, exc_info=True, stack_info=True)


if __name__ == '__main__':
    main()
