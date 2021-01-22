import unittest
from fixture_parser import get_fixtures, parse_fixtures

class FixtureParserTestCase(unittest.TestCase):
    def test_get_fixtures(self):
        self.assertEqual(get_fixtures("akjscajsnc"), "abc")

    def test_parse_fixtures(self):
        self.assertEqual(parse_fixtures([]), 123)