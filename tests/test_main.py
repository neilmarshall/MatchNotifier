import unittest
from datetime import datetime
from dateutil.tz import gettz, tzutc
from unittest.mock import call, MagicMock, patch

from main import get_timeout, main


class MainTestCase(unittest.TestCase):
    mock_environ = MagicMock(get = MagicMock(return_value = 'mock_get_fixtures_url'))

    mock_entities = [
        {'PartitionKey': 'test1@test.com', 'RowKey': '1', 'CompetitionName': 'Premier League', 'TeamName': 'Liverpool'},
        {'PartitionKey': 'test1@test.com', 'RowKey': '2', 'CompetitionName': 'The FA Cup', 'TeamName': 'Liverpool'},
        {'PartitionKey': 'test1@test.com', 'RowKey': '3', 'CompetitionName': 'The FA Cup', 'TeamName': 'Chelsea'},
        {'PartitionKey': 'test2@test.com', 'RowKey': '4', 'CompetitionName': 'Premier League', 'TeamName': 'Liverpool'}
    ]

    mock_table_client = MagicMock(list_entities = MagicMock(return_value = mock_entities))

    mock_table_service_client = MagicMock()
    mock_table_service_client.from_connection_string.return_value = mock_table_service_client
    mock_table_service_client.get_table_client.return_value = mock_table_client

    mock_get_fixtures = MagicMock(side_effect=(
        [('The FA Cup', 'Chelsea', 'Arsenal', datetime(2021, 1, 24, 12, 0, 0)),
         ('Premier League', 'Burnley', 'Liverpool', datetime(2021, 1, 24, 16, 30, 0))],
        [('Premier League', 'Burnley', 'Liverpool', datetime(2021, 1, 24, 16, 30, 0))]
    ))

    @patch('main.os.environ', mock_environ)
    @patch('main.TableServiceClient', mock_table_service_client)
    @patch('main.QueueServiceClient')
    @patch('main.get_fixtures', mock_get_fixtures)
    @patch('main.send_email')
    def test_main(self, mock_send_email, mock_queue_service_client):
        main(None)
        call_count = len(set(map(lambda o: o['PartitionKey'], self.mock_entities)))
        self.assertEqual(self.mock_get_fixtures.call_count, call_count)
        self.mock_get_fixtures.assert_has_calls((
            call('mock_get_fixtures_url', {'Premier League': ['Liverpool'], 'The FA Cup': ['Liverpool', 'Chelsea']}),
            call('mock_get_fixtures_url', {'Premier League': ['Liverpool']})
        ))
        self.assertEqual(mock_send_email.call_count, call_count)
        mock_send_email.assert_has_calls((
            call('Fixture Notification', 'The FA Cup - Chelsea vs. Arsenal, 12:00PM\nPremier League - Burnley vs. Liverpool, 4:30PM', 'test1@test.com'),
            call('Fixture Notification', 'Premier League - Burnley vs. Liverpool, 4:30PM', 'test2@test.com')
        ))
    
    @patch('main.datetime')
    def test_get_timeout(self, mock_datetime):
        mock_datetime.side_effect = [
            datetime(2021, 9, 5, 17, 30, tzinfo=gettz('BST')),
            datetime(2021, 9, 5, 17, 30, tzinfo=tzutc())
        ]
        mock_datetime.now = lambda _: datetime(2021, 9, 5, 8, 30, tzinfo=tzutc())
        self.assertEqual(get_timeout(2021, 9, 5, 17, 30), 32400)
