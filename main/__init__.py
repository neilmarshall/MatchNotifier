import datetime
import logging

import azure.functions as func

from fixture_parser.get_fixtures import get_fixtures


def main(mytimer: func.TimerRequest) -> None:
    fixture = get_fixtures(r"https://www.bbc.co.uk/sport/football/scores-fixtures/2021-01-28", "Premier League", "Liverpool")
    if fixture is not None:
        logging.info(f"Fixture found: {fixture}")