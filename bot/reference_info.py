from bot.database.get import leagues, get_teams

DICT_LEAGUE = {}
DICT_TEAM = {}

teams = []

for league in leagues:
    DICT_LEAGUE[league.name] = league.id
    DICT_TEAM[league.id] = get_teams(league)

for i in DICT_TEAM.values():
    teams.extend([*i.values()])


def get_key(team_dic: dict, val: str):
    for k, v in team_dic.items():
        if v == val:
            return k


print(get_key(DICT_TEAM.get(DICT_LEAGUE.get("АПЛ")), "Ливерпуль"))
