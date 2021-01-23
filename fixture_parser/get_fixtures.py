import requests
from .filter_fixtures import filter_fixtures
from .parse_fixtures import parse_fixtures

def get_fixtures(url : str, fixture_filter : dict) -> tuple:
    """Parse and return fixtures from a URL, filtered by competition and team"""
    response = requests.get(url)
    return filter_fixtures(parse_fixtures(response.content), fixture_filter)
