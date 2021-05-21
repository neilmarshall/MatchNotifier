import argparse
from uuid import uuid4

from azure.data.tables import TableServiceClient

from configuration_manager import Config


parser = argparse.ArgumentParser(description='Command-line client for registering for match notifications')
parser.add_argument('email_address', help='Email address to send notifications to')
parser.add_argument('competition_name', help='Competition name for filtering receive notfications')
parser.add_argument('team_name', help='Team name for filtering notfications')

if __name__ == '__main__':
    try:
        args = parser.parse_args()
        config = Config()
        table_client = TableServiceClient.from_connection_string(conn_str=config.get_connection_string())
        table = table_client.create_table_if_not_exists(config.parameters['TableName'])
        entity = {
            'PartitionKey': args.email_address,
            'RowKey': str(uuid4()),
            'CompetitionName': args.competition_name,
            'TeamName': args.team_name
        }
        table.create_entity(entity)
    except Exception as e:
        print(f"An unexpected error was encountered: {e}")
