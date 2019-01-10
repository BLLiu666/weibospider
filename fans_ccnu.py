# -*- coding: utf-8 -*-
# @Author   : Zoe
# @time     : 2019/1/2 11:06
# @File     : fans_info.py
# @Software : PyCharm

import requests
from bs4 import BeautifulSoup
import re
import json
import xlwt
import time


def getHTMLtest(url):           #获取页面源代码
    #cookie
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
        'Cookie': "_T_WM=801be916b8837b79625f0c53f5fce578; SUB=_2A25xA8vbDeRhGeBK7lQY8i_JwjSIHXVSD9WTrDV6PUJbkdBeLXbykW1NR74FrwAxjdVIJLKCTd4mYVtVVuneIQP3; SUHB=0la1Ycv3oHlNrL; SCF=Asxj901_1IbAniuMRS9nPXUbTqUKAvHdthzZ8_5GBaGq6Eltfn-f9O2-SciuGuGfJ0BLSB_Nk_bggAs-ZVqbIlE.; SSOLoginState=1544010636; MLOGIN=1"
        }
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def getInfotest(uid):           #获取个人信息：地区，性别，有标签的获取标签

        url = "https://weibo.cn/" + str(uid) + "/info"  # 爬取地区和性别
        infohtml = getHTMLtest(url)
        soup = BeautifulSoup(infohtml, "xml")
        div = soup.find_all("div", attrs={"class": "c"})[2]
        sex = re.findall(r"[性别].*?[<]", str(div))[0].replace("性别:", "").replace("<", "")
        addr = re.findall(r"[地区].*?[<]", str(div))[0].replace("地区:", "").replace("<", "").split(" ")[0]
        a=[]
        if "标签" in infohtml:
            spanurl = "https://weibo.cn/account/privacy/tags/?uid="+str(uid)+"&st=2675b6"
            spanhtml = getHTMLtest(spanurl)
            spansoup = BeautifulSoup(spanhtml,"xml")
            spandiv = spansoup.find_all("div",attrs={"class":"c"})[2]
            a = re.findall(r"<a href.*?</a>",str(spandiv))
            for i in range(len(a)):
               a[i] = a[i].replace(re.findall(re.compile(r"<a.*?>"),str(a[i]))[0],"").replace("</a>","")
        return sex,addr,a



def getInfoList(nan,nv,list,html):             #获取粉丝id
  try:
    resjson = json.loads(html)
    data = resjson.get("data")
    if data.get("cards") != []:
        cards = data.get("cards")[0]
        card_group = cards.get("card_group")
        print(len(card_group))
        for i in range(len(card_group)):
            try:
                user = card_group[i].get("user")
                uid = user.get("id")
                username = user.get("screen_name")
                sex,addr,a = getInfotest(uid)
                print(uid)
                print(username)
                print(sex)
                print(addr)
                print(a)
                if sex == "男":
                    nan += 1
                if sex == "女":
                    nv += 1
                list.append([uid,username,sex,addr,a])
            except:
                continue
  except:
      return ""

def getExceltest(list):
    excel = xlwt.Workbook(encoding="utf-8")
    sheet = excel.add_sheet("sheet1")
    sheet.write(0, 0, "id")
    sheet.write(0, 1, "用户名")
    sheet.write(0, 2, "性别")
    sheet.write(0, 3, "地区")
    sheet.write(0, 4, "标签")
    for i in range(len(list)):
        t = list[i]
        sheet.write(i + 1, 0, t[0])
        sheet.write(i + 1, 1, t[1])
        sheet.write(i + 1, 2, t[2])
        sheet.write(i + 1, 3, t[3])
        count = 4
        for j in range(len(t[4])):
            sheet.write(i+1,count,t[4][j])
            count += 1

    excel.save('huashi8.xls')


def main():
    id = "1878136331"
    list = []
    nan = 0
    nv = 0
    num = 0
    while num < 51:
        url = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_"+id+"&luicode=10000011&lfid=100505"+id+"&since_id="+str(num+200)
        html = getHTMLtest(url)
        getInfoList(nan,nv,list,html)
        print(url)
        print("data:"+str(len(list)))
        time.sleep(10)
        num +=1
        if num%10 == 0:
            time.sleep(20)

    getExceltest(list)
    print("男:" + str(nan))
    print("女："+ str(nv))

if __name__ == "__main__":
    main()

