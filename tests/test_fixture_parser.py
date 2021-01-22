import unittest
from unittest.mock import patch
from datetime import datetime

from fixture_parser import filter_fixtures, get_fixtures, parse_fixtures

class FixtureParserTestCase(unittest.TestCase):
    def setUp(self):
        with open('./tests/response_data.txt', encoding='utf-8') as f:
            self.data = f.read()

    def test_filter_fixtures(self):
        fixtures = parse_fixtures(self.data)
        expected = ('KV Oostende', 'Standard Liege', datetime(2021, 1, 22, 20, 0))
        self.assertEqual(filter_fixtures(fixtures, 'Belgian First Division A', 'Standard Liege'), expected)

    @patch('requests.get')
    def test_get_fixtures(self, mock_object):
        mock_object.return_value.content = self.data
        expected = ('KV Oostende', 'Standard Liege', datetime(2021, 1, 22, 20, 0))
        self.assertEqual(get_fixtures('mock_url', 'Belgian First Division A', 'Standard Liege'), expected)

    def test_parse_fixtures(self):
        expected = {
            'Premier League': [
                ('Tottenham Hotspur', 'Liverpool', datetime(2021, 1, 22, 20, 0))
            ],
            "The FA Women's Championship": [
                ('Charlton Athletic Women', 'London City Lionesses', datetime(2021, 1, 22, 19, 45))
            ],
            'Italian Coppa Italia': [
                ('Napoli', 'Spezia', datetime(2021, 1, 22, 20, 0))
            ],
            'Belgian First Division A': [
                ('Cercle Bruges', 'Club Bruges', datetime(2021, 1, 22, 17, 45)),
                ('KV Oostende', 'Standard Liege', datetime(2021, 1, 22, 20, 0))
            ],
            'Brazilian Série A': [
                ('Bahia', 'Corinthians', datetime(2021, 1, 22, 22, 0)),
                ('Grêmio', 'Flamengo', datetime(2021, 1, 22, 23, 0))
            ],
            'Dutch Eredivisie': [
                ('Sparta Rotterdam', 'FC Twente', datetime(2021, 1, 22, 17, 45)),
                ('Ajax', 'Willem II', datetime(2021, 1, 22, 20, 0))
            ],
            'Greek Superleague': [
                ('Panetolikos', 'Atromitos Athens', datetime(2021, 1, 22, 15, 15))
            ],
            'Swiss Super League': [
                ('Sion', 'FC Basel', datetime(2021, 1, 22, 19, 30))
            ]
        }
        self.assertEqual(parse_fixtures(self.data), expected)