from datetime import datetime
from bs4 import BeautifulSoup

def parse_fixtures(data):
    """Parse a HTML response object into a data structure representing matches, grouped by competition"""
    soup = BeautifulSoup(data, 'html.parser')
    competitions = soup.find_all(class_="qa-match-block")
    fixtures = {}
    for competition in competitions:
        competition_name = competition.find('h3').text
        fixtures[competition_name] = []
        matches = competition.find('ul').find_all('li')
        for match in matches:
            home_team, away_team = map(lambda b: b.text, match.find_all(class_="qa-full-team-name"))
            timestamp = match.find(class_="sp-c-fixture__number").text
            if timestamp == 'P':
                continue
            hour, minute = map(int, timestamp.split(':'))
            matchdate = datetime(datetime.today().year, datetime.today().month, datetime.today().day, hour, minute)
            fixtures[competition_name].append((home_team, away_team, matchdate))
    return fixtures