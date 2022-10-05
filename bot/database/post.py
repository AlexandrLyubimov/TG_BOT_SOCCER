import requests

from config import SERVER_API_TOKEN, SERVER_API_URL_ADD_USER


def add_user(chat_id):
    data = {
        "chat_id": f'{chat_id}'
    }
    resp = requests.post(url=SERVER_API_URL_ADD_USER, headers={"Authorization": SERVER_API_TOKEN}, json=data)
    print(f'SENDING: {data} RESULT:{resp.text}')
