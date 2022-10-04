from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: bool
    error: str


class LeagueInfo(BaseModel):
    id: int
    name: str


class LeagueInfoResponse(BaseResponse):
    result: list[LeagueInfo]


class TeamInfo(BaseModel):
    id: int
    name: str
    # league_id: int


class TeamInfoResponse(BaseResponse):
    result: list[TeamInfo]
