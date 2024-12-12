from requests import Session
from lib.logininfo import headers

session = Session()
session.headers = headers


def mine(state):
    """
    state 0: 暂停挖矿
    state 1: 开始挖矿
    state 2: 自动加时
    """

    url = "https://block-api.lucklyworld.com/v11/api/cave/auto/digging/save"

    payload = f"state={state}&caveType=1"

    response = session.post(url, data=payload)

    return response.json()


def remaining_mining_time():
    url = "https://block-api.lucklyworld.com/v11/api/cave/auto/digging/page"

    response = session.post(url)

    data = response.json()

    return round(float(data["autoDiggingOddSecond"]) / 3600, 2)
