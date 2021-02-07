# -*- coding = utf-8 -*-
# @Time : 2021/1/24 0:27
# @Auther : cmodog
# @File : main.py
# @Software: PyCharm

import os
import requests
from bs4 import BeautifulSoup

USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]


HEADER_GET = {
    "user-agent": "Mozilla/5.0 (Linux; Android 11; Mi 10 Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.185 Mobile Safari/537.36/lenovoofficialapp/16112154380982287_10181446134/newversion/versioncode-124/"
}

HEADER_COUNT = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
}

def login() -> (requests.session, str):       #登录过程
    url = "https://reg.lenovo.com.cn/auth/v3/dologin"
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
        "Host": "reg.lenovo.com.cn",
        "Referer": "https://www.lenovo.com.cn/"
    }
    data = {"account": USERNAME, "password": PASSWORD, "ticket": "e40e7004-4c8a-4963-8564-31271a8337d8"}
    session = requests.Session()
    r = session.post(url,headers=header,data=data)
    if r.text.find("cerpreg-passport") == -1:       #若未找到相关cookie则返回空值
        return None
    return session

def getContinuousDays(session):
    url = "https://club.lenovo.com.cn/signlist/"
    c = session.get(url,headers=HEADER_COUNT)
    soup = BeautifulSoup(c.text,"html.parser")
    cc = soup.select("body > div.signInMiddleWrapper > div > div.signInTimeInfo > div.signInTimeInfoMiddle > p.signInTimeMiddleBtn")
    cc = cc[0].get_text()
    if cc == " 已签到 ":
        return 1
    return cc[5:6]


def signin(session):
    signin = session.get("https://i.lenovo.com.cn/signIn/add.jhtml?sts=e40e7004-4c8a-4963-8564-31271a8337d8",headers=HEADER_GET)
    check = str(signin.text)
    if "true" in check:
        if "乐豆" in check:
            print("签到成功")
        else:
            print("请不要重复签到")
    else:
        print("签到失败，请重试")

if __name__ == '__main__':
    s = login()
    if not s:
        print("登录失败，请检查账号密码")
    else:
        signin(s)
        print("当前已连续签到%s天"%getContinuousDays(s))
