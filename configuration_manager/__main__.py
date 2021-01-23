import json
import sys
from uuid import uuid4

from azure.data.tables import TableServiceClient


if __name__ == '__main__':
    try:
        email, competition_name, team_name = sys.argv[1:]
        with open('local.settings.json') as f:
            config = json.load(f)['Values']
        table_client = TableServiceClient.from_connection_string(conn_str=config['AzureWebJobsStorage'])
        table = table_client.create_table_if_not_exists(config['TableName'])
        entity = {
            'PartitionKey': email,
            'RowKey': str(uuid4()),
            'CompetitionName': competition_name,
            'TeamName': team_name
        }
        table.create_entity(entity)
    except Exception as e:
        print(f"An unexpected error was encountered: {e}")
