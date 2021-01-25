import logging
from datetime import datetime

import azure.functions as func

from email_client.email_client import send_email


def main(msg: func.QueueMessage) -> None:
    logging.info(f"Python queue trigger function processed a queue item: {msg.id}")

    try:
        json = msg.get_json()

        recipient = json['recipient']
        competition = json['competition']
        home_team = json['homeTeam']
        away_team = json['awayTeam']
        matchdate = datetime.fromisoformat(json['matchdate'])

        subject = "Fixture Notification - 1 hour to go"
        timestamp = f"{matchdate.hour % 12 if matchdate.hour > 12 else matchdate.hour}:{matchdate.minute:02}{'AM' if matchdate.hour < 12 else 'PM'}"
        body = f"{competition} - {home_team} vs. {away_team}, {timestamp}"
        send_email(subject, body, recipient)

        logging.info(f"Processing complete")
    except Exception as ex:
        logging.error(ex)
