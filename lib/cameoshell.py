from requests import Session
from lib.logininfo import headers

session = Session()
session.headers = headers


def shell_information():
    response = session.post(
        url="https://block-api.lucklyworld.com/v6/api/pets/shells/trade/index",
        headers=headers,
    )
    return response.json()


def shell_market(type, page=1):
    """
    type: 0 求购中, 1 出售中
    """
    urls = [
        "https://block-api.lucklyworld.com/v6/api/pets/shells/trade/purchase/list",
        "https://block-api.lucklyworld.com/v6/api/pets/shells/trade/sale/list",
    ]

    url = urls[type]
    response = session.post(url=urls[type], data="page=1")
    return response.json()["list"]


def shell_transaction(type, tradeId, quantity):
    """
    type: 0 购买, 1 出售
    tradeId: 交易id
    quantity: 数量
    """
    urls = [
        "https://block-api.lucklyworld.com/v6/api/pets/shells/trade/purchase",
        "https://block-api.lucklyworld.com/v6/api/pets/shells/trade/sell",
    ]

    response = session.post(
        url=urls[type], data=f"tradeId={tradeId}&quantity={quantity}"
    )
    return response.json()


def get_shells_trade_log(page=1):
    return session.post(
        url="https://block-api.lucklyworld.com/v6/api/pets/shells/trade/logs",
        data=f"page={page}",
        headers=headers,
    ).json()


def get_shells_trade_logs():
    """获取所有页并写入文件"""
    hasMore = True
    next = 1
    trade_list = []

    while hasMore:
        print(f"\r正在获取第 {next} 页 当前 {len(trade_list)} 条记录", end="")
        data = get_shells_trade_log(next)
        hasMore = data["hasMore"]
        next = data["next"]
        trade_list += data["list"]

    print(f"\r获取完成, 共 {next} 页 {len(trade_list)} 条记录,正在写入", end="")

    with open("data/shells_trade_logs.txt", "w") as f:
        f.write(str(trade_list))

    print(f"\r写入完成 data/shells_trade_logs.txt", end="")
