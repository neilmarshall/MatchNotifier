import unittest
from datetime import datetime
from unittest.mock import call, MagicMock, patch

from run import main


class MainTestCase(unittest.TestCase):
    mock_entities =  {
        "test1@test.com": {
            "Premier League": [
                "Liverpool"
            ]
        },
        "test2@test.com": {
            "The FA Cup": [
                "Liverpool",
                "Chelsea"
            ],
            "Premier League": [
                "Liverpool",
                "Arsenal"
            ]
        }
    }

    mock_get_config = MagicMock(return_value={
        "fixtures_URL": "mock_get_fixtures_url",
        "entities": mock_entities
    })

    mock_get_fixtures = MagicMock(side_effect=(
        [('The FA Cup', 'Chelsea', 'Arsenal', datetime(2021, 1, 24, 12, 0, 0)),
         ('Premier League', 'Burnley', 'Liverpool', datetime(2021, 1, 24, 16, 30, 0))],
        [('Premier League', 'Burnley', 'Liverpool', datetime(2021, 1, 24, 16, 30, 0))]
    ))

    @patch('run.get_config', mock_get_config)
    @patch('run.get_fixtures', mock_get_fixtures)
    @patch('run.send_email')
    def test_main(self, mock_send_email):
        main()
        call_count = len(self.mock_entities)
        self.assertEqual(self.mock_get_fixtures.call_count, call_count)
        self.mock_get_fixtures.assert_has_calls((
            call('mock_get_fixtures_url', {'Premier League': ['Liverpool']}),
            call('mock_get_fixtures_url', {'The FA Cup': ['Liverpool', 'Chelsea'], 'Premier League': ['Liverpool', 'Arsenal']})
        ))
        self.assertEqual(mock_send_email.call_count, call_count)
        mock_send_email.assert_has_calls((
            call('Fixture Notification', 'The FA Cup - Chelsea vs. Arsenal, 12:00PM\nPremier League - Burnley vs. Liverpool, 4:30PM', 'test1@test.com'),
            call('Fixture Notification', 'Premier League - Burnley vs. Liverpool, 4:30PM', 'test2@test.com')
        ))
