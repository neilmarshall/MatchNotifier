def filter_fixtures(fixtures, competition_name, team_name):
    if competition_name not in fixtures:
        return None
    for (home_team, away_team, matchdate) in fixtures[competition_name]:
        if home_team == team_name or away_team == team_name:
            return (home_team, away_team, matchdate)