import csv
import os
import time
from lib.battleroyale import battle_royale_information, get_real_room
from lib.snowfunction import cleanT, pTitle, currenttime
from lib.battleroyalecalculation import get_win_stat, get_m_stat


if __name__ == "__main__":
    data = ""
    current_period = 0
    num = 2000
    if not os.path.exists("data/escape.csv"):
        with open("data/escape.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["期数", "时间", "击杀房间", "上局击杀房间", "是否获胜", "消耗宝石", "获得宝石", "我的宝石"]
            )

    while True:
        try:
            data = battle_royale_information()
            win, lose, win_rate = get_win_stat(num)
            paid_m, win_m, total_m = get_m_stat(num)
            cleanT()
            print(
                f"\n {pTitle('大逃杀监控')}\n\n",
                f"当前期数: {data['issue']}\n",
                f"当前时间: {currenttime()}\n\n",
                f"{pTitle('本期信息')}\n\n",
                f"倒计时: {data['countdown']}\t\t是否获胜: {data['myIsWin']}\n",
                f"本期击杀: {get_real_room(data['killNumber'])}\t上期击杀: {get_real_room(data['prevRoomNumber'])}\n",
                f"是否结算: {'是' if data['state']==2 else '否'}\t\t我的宝石: {data['myWallet']}\n",
                f"\n {pTitle(f'近 {num} 场数据胜率')}\n\n",
                f"胜场: {win}\t败场: {lose}\t胜率: {win_rate}\n",
                f"投入: {paid_m}\t赚的: {win_m}\t利润: {total_m}",
            )
            if data["state"] == 2 and current_period != data["issue"]:
                with open("data/escape.csv", "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        [
                            data["issue"],
                            currenttime(),
                            data["killNumber"],
                            data["prevRoomNumber"],
                            data["myIsWin"],
                            data["myCostMedal"],
                            data["myWinMedal"],
                            data["myWallet"],
                        ]
                    )
                current_period = data["issue"]
        except Exception as e:
            print(f"错误: {e}")
        time.sleep(1)
