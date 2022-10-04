from bot.database.get import leagues, get_teams

DICT_LEAGUE = {}
DICT_TEAM = {}

teams = []

for league in leagues:
    DICT_LEAGUE[league.name] = league.id
    DICT_TEAM[league.id] = get_teams(league)

for i in DICT_TEAM.values():
    teams.extend([*i.keys()])
