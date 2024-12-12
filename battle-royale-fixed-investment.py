import random
import time
from lib.battleroyale import get_real_room, battle_royale_information, battle_royale_investment
from lib.snowfunction import decompose_number, currenttime, cleanT

probability_gems = ""
gem_mode = 0
fixed_investment_mode = 0

is_paid = 0
is_updated = 0
roomid = 0
rock_num = 0
win_m = 0
issue = 0
prevRoomNumber = 0


def information_request():
    global gem_mode, rock_num, probability_gems, fixed_investment_mode, roomid
    print("信息配置")
    print("1. 固定宝石")
    print("2. 概率宝石(多个数,英文逗号分隔)")
    print("例: 0.1, 0.1, 0.2, 0.2, 0.2 为 40% 0.1 60% 0.2")
    gem_mode = input("输入宝石模式(1-2): ")
    if gem_mode == "1":
        rock_num = input("输入投入定投宝石: ")
    elif gem_mode == "2":
        probability_gems = input("请按照例子书写概率：").split(",")

    print("1. 固定房间")
    print("2. 随机房间")
    print("3. 加一模式")
    fixed_investment_mode = input("输入定投模式(1-3): ")
    if fixed_investment_mode == "1":
        roomid = input("输入房间号(1-8): ")


def throw_in_gems():
    global rock_num
    if gem_mode == "1":
        pass
    elif gem_mode == "2":
        rock_num = random.choice(probability_gems).strip()


def throw_into_the_room():
    global roomid
    if fixed_investment_mode == "1":
        pass
    elif fixed_investment_mode == "2":
        roomid = random.randint(1, 8)
    elif fixed_investment_mode == "3":
        roomid = (int(prevRoomNumber) + 1) if int(prevRoomNumber) <= 7 else 1


def investment(rock_num):
    r = battle_royale_investment(roomNumber=roomid, costMedal=rock_num)
    if r.get("message", "ok") == "ok":
        print(f"{currenttime()}  投入 {get_real_room(roomid)} 宝石 {rock_num}")
    else:
        print(f"{currenttime()}  投入失败 {r.get('message', 'ok')}")


def main():
    global is_paid, is_updated, roomid, rock_num, win_m, issue, prevRoomNumber
    try:
        issue_info = battle_royale_information()
        new_issue, prevRoomNumber = issue_info["issue"], issue_info["prevRoomNumber"]
        if issue_info["myWinMedal"] != "0":
            win_m = float(issue_info["myWinMedal"])

        if not is_updated and new_issue != issue:
            if is_paid:
                # 判断上局胜负
                red = "\033[31m凉了TAT\033[39m"
                if int(roomid) == int(prevRoomNumber):
                    print(f"{currenttime()}  第 {new_issue-1} 期 {red}")
                else:
                    win_m_num = round(win_m-float(rock_num),4) if win_m else "不知道"
                    print(
                        f"{currenttime()}  第 {new_issue-1} 期 赢得 {win_m_num} 宝石"
                    )
            print(f"{currenttime()}  进入第 {new_issue} 期")
            issue = new_issue
            is_paid = 0
            is_updated = 1

        # 倒计时 40 秒后投入
        if 5 < battle_royale_information()["countdown"] < 40 and not is_paid:
            throw_in_gems()
            throw_into_the_room()

            for i in decompose_number(rock_num):
                investment(i)

            is_paid = 1
            is_updated = 0

    except Exception as e:
        print(e)
    time.sleep(3)


if __name__ == "__main__":
    cleanT()
    information_request()
    cleanT()

    print(f"{currenttime()} 开始")

    while 1:
        main()
