import requests
from pydantic import ValidationError
from requests import Response

from config import SERVER_API_URL_LEAGUE, SERVER_API_TOKEN, SERVER_API_URL_TEAM, SERVER_API_URL_RESULT
from bot.schemas.server import LeagueInfoResponse, TeamInfoResponse, ResultInfoResponse


def parse_response(response: Response, ResponseModel):
    result = None
    if response.status_code == 200:
        try:
            result = ResponseModel.parse_raw(response.text)
        except ValidationError:
            # Break?
            pass
    else:
        # Break?
        pass
    return result


response = requests.get(url=SERVER_API_URL_LEAGUE, headers={"Authorization": SERVER_API_TOKEN})
league_info: LeagueInfoResponse = parse_response(response, LeagueInfoResponse)
leagues = [el for el in league_info.result]


def get_teams(league) -> dict:
    tmp_dict = {}
    resp = requests.get(url=SERVER_API_URL_TEAM + f'{league.id}', headers={"Authorization": SERVER_API_TOKEN})
    team_info: TeamInfoResponse = parse_response(resp, TeamInfoResponse)
    teams = [el for el in team_info.result]
    for team in teams:
        tmp_dict[team.name] = team.id
    return tmp_dict


def result_info_team(id_team_h, id_team_g):
    d = {}
    resp = requests.get(url=SERVER_API_URL_RESULT + f'{id_team_h}' + f'/{id_team_g}', headers={"Authorization": SERVER_API_TOKEN})
    result_info: ResultInfoResponse = parse_response(resp, ResultInfoResponse)
    return result_info
