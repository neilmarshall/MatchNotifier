def filter_fixtures(fixture_data : dict, fixture_filter : dict):
    """Filter a data structure representing matches for a given competition and team"""
    fixtures = []
    for competition_name in fixture_filter:
        if competition_name not in fixture_data:
            continue
        team_names = set(fixture_filter[competition_name])
        for (home_team, away_team, matchdate) in fixture_data[competition_name]:
            if home_team in team_names or away_team in team_names:
                fixtures.append((competition_name, home_team, away_team, matchdate))
    return fixtures
