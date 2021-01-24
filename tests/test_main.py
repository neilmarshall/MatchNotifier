import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from main import main


class MainTestCase(unittest.TestCase):
    mock_environ = MagicMock(get = MagicMock(return_value = 'mock_get_fixtures_url'))

    mock_entities = [
        {'PartitionKey': 'test@test.com', 'RowKey': '1', 'CompetitionName': 'Premier League', 'TeamName': 'Liverpool'},
        {'PartitionKey': 'test@test.com', 'RowKey': '2', 'CompetitionName': 'The FA Cup', 'TeamName': 'Liverpool'},
        {'PartitionKey': 'test@test.com', 'RowKey': '3', 'CompetitionName': 'The FA Cup', 'TeamName': 'Chelsea'}
    ]

    mock_table_client = MagicMock(list_entities = MagicMock(return_value = mock_entities))

    mock_table_service_client = MagicMock()
    mock_table_service_client.from_connection_string.return_value = mock_table_service_client
    mock_table_service_client.get_table_client.return_value = mock_table_client

    mock_get_fixtures = MagicMock(return_value=[
        ('Chelsea', 'Arsenal', datetime(2021, 1, 24, 12, 0, 0)),
        ('Burnley', 'Liverpool', datetime(2021, 1, 24, 16, 30, 0))
    ])

    @patch('main.os.environ', mock_environ)
    @patch('main.TableServiceClient', mock_table_service_client)
    @patch('main.get_fixtures', mock_get_fixtures)
    @patch('main.send_email')
    def test_main(self, mock_send_email):
        main(None)
        self.mock_get_fixtures.assert_called_once_with(
            'mock_get_fixtures_url',
            {'Premier League': ['Liverpool'], 'The FA Cup': ['Liverpool', 'Chelsea']}
        )
        mock_send_email.assert_called_once_with(
            'Fixture Notification',
            'Chelsea vs. Arsenal, 12:00PM\nBurnley vs. Liverpool, 4:30PM',
            'test@test.com'
        )
