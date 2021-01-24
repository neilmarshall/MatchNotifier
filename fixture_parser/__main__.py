import argparse
import json
from itertools import groupby
from pprint import pprint

import requests
from azure.data.tables import TableServiceClient

from fixture_parser.get_fixtures import get_fixtures


parser = argparse.ArgumentParser(description='Command-line client for running match notifications')
parser.add_argument('-d', '--debug', action='store_true', help='Execute program in debug mode')

if __name__ == '__main__':
    args = parser.parse_args()
    if args.debug:
        breakpoint()
    try:
        with open('local.settings.json') as f:
            config = json.load(f)['Values']
        table_service_client = TableServiceClient.from_connection_string(conn_str=config["AzureWebJobsStorage"])
        table_client = table_service_client.get_table_client(config["TableName"])

        fixtures_URL = config['FixturesURL']

        entities = sorted(table_client.list_entities(), key=lambda o: o['PartitionKey'])
        for email, _entities in groupby(entities, key=lambda o: o['PartitionKey']):
            fixture_filter = {}
            grouped_entities = sorted(_entities, key=lambda o: o['CompetitionName'])
            for competition_name, _grouped_entities in groupby(grouped_entities, key=lambda o: o['CompetitionName']):
                team_names = [o['TeamName'] for o in _grouped_entities]
                fixture_filter[competition_name] = team_names

                fixtures = get_fixtures(fixtures_URL, fixture_filter)
                pprint(fixtures)
    except Exception as e:
        print(e)
