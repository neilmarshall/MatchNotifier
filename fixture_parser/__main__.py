import json
import sys
from pprint import pprint

import requests

from .parse_fixtures import parse_fixtures


if __name__ == '__main__':
    debug = len(sys.argv) > 1 and bool(sys.argv[1])
    if debug:
        breakpoint()
    with open('local.settings.json') as f:
        config = json.load(f)['Values']
    competitionName = config['CompetitionName']
    teamName = config['TeamName']
    fixturesURL = config['FixturesURL']
    response = requests.get(fixturesURL)
    try:
        pprint(parse_fixtures(response.content))
    except Exception as e:
        print(e)
