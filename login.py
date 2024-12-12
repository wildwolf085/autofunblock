from lib.logininfo import write_value
from lib.account import send_verification_code, login


if __name__ == "__main__":
    num = input("请输入手机号:")
    res = send_verification_code(num)
    if res.get("code") == 0:
        print("发送成功")
    else:
        print(f"发送失败! {res.get('message')}")
        input()
        exit()

    while True:
        code = input("请输入验证码:")
        res2 = login(num, code)
        print(res2.get("token"))
        if res.get("errorCode") == 400:
            print(f"登录失败! {res.get('message')}")
        else:
            print("登录成功! token 已经写入 setting.ini")
            write_value("token", res2.get("token"))
            break
