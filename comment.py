# -*- coding:utf-8 -*-
__author__ = 'BLLiu666'

import requests
import re
from bs4 import BeautifulSoup
import xlwt
import time

def getXMLText(url):
    headers = { 
        #'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
        'Cookie': '_T_WM=1ac2628927d2214f7e7f706e00a8c8d7; SUHB=0u5RIOa0_Yk6eX; SCF=AuyvH4HeMnOH7hA_OvhvGXdVTKxs4lwT55723ktHa0dHv5hID7LUt8qiQIR2LBtYcFoNGYz4RnG7pSW_9gQyAmg.; ALF=1549800349; SUB=_2A25xPMcVDeRhGeNL6FAU9CrJyjSIHXVS3uldrDV6PUJbkdAKLXDtkW1NSQBFknIm1j6EoqCA4FxOemt0z8I_oVKW; SSOLoginState=1547220805'
    }
    try:
        r = requests.get(url , headers = headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def getList(list,xml):
    soup = BeautifulSoup(xml,"xml")
    div0 = soup.find_all("div",attrs={"class": "c"})
    div = []
    for i in range(len(div0)):
        if  'id="C' in str(div0[i]):
            div.append(div0[i])
    for i in range(len(div)):
        try:
            #print(div[i])
            pat = re.compile(r'<a href=".*?">')
            ID = pat.search(str(div[i]))[0].replace('<a href="',"").replace('">',"")
            username = re.compile(r'<a href=".*?</a>').search(str(div[i]))[0].replace('<a href="',"").replace('">',"").replace(ID,"").replace("</a>","")
            if "/u" in ID:
                id = ID.replace("/u/","")
            else:
                weiid = ID.replace("/","")
                uurrll = "https://weibo.cn/"+str(weiid)
                xxml = getXMLText(uurrll)
                sssoup = BeautifulSoup(xxml,"xml")
                id = re.compile(r"\d{10}").search(str(sssoup))[0]
            infourl = "https://weibo.cn/" + str(id) + "/info"     #爬取地区和性别
            infohtml = getXMLText(infourl)
            ssoup = BeautifulSoup(infohtml, "xml")
            c = ssoup.find_all("div", attrs={"class": "c"})[2]
            sex = re.findall(r"[性别].*?[<]", str(c))[0].replace("性别:", "").replace("<", "")
            addr = re.findall(r"[地区].*?[<]", str(c))[0].replace("地区:", "").replace("<", "").split(" ")[0]
            ttext = re.compile(r'<span class="ctt.*?</span>').search(str(div[i]))[0]
            like = re.compile(r"赞.*?</a>").search(str(div[i]))[0].replace("赞[","").replace("]</a>","")
            text = ""
            if "回复" in ttext:
                text = re.compile(r'</a>.*?</span>').search(str(ttext))[0].replace("</a>:","").replace("</span>","")
            else:
                text = ttext.replace('<span class="ctt">','').replace('</span>','')
            if "</a>" in text:
                text = text.replace(re.compile(r'<a.*?/a>').search(str(text))[0],"")
            print(text)
            biaoqing = re.findall(r"[[](.*?)[]]", text)
            time = re.compile(r'<span class="ct".*?</span>').search(str(div[0]))[0].replace('<span class="ct">','').replace('</span>','')
            if text:
                list.append([id,username,sex,addr,text,time,like,biaoqing])
        except:
            continue
def getExcel(list):
    excel = xlwt.Workbook(encoding="utf-8")
    sheet = excel.add_sheet("sheet1")
    sheet.write(0,0,"id")
    sheet.write(0, 1, "用户名")
    sheet.write(0, 2, "性别")
    sheet.write(0, 3, "地区")
    sheet.write(0, 4, "评论")
    sheet.write(0, 5, "时间")
    sheet.write(0, 6, "点赞")
    sheet.write(0, 7, "表情")
    for i in range(len(list)):
        t = list[i]
        sheet.write(i+1, 0, t[0])
        sheet.write(i+1, 1, t[1])
        sheet.write(i+1, 2, t[2])
        sheet.write(i+1, 3, t[3])
        sheet.write(i+1, 4, t[4])
        sheet.write(i + 1, 5, t[5])
        sheet.write(i + 1, 6, t[6])
        m = t[7]
        num = 7
        for j in range(len(m)):
            sheet.write(i+1,num,m[j])
            num += 1
    excel.save('comments.xls')

def main():
    i = 0
    list = []
    for i in range(1,100):
        url  = 'https://weibo.cn/comment/GoWl2s5NT?&page={}'.format(i)
        xml = getXMLText(url)
        getList(list,xml)
        print(url)
        i += 1
        print("已爬取"+str(len(list)))
        time.sleep(10)
        if i%5 == 0:
            time.sleep(20)
    getExcel(list)

if __name__ =="__main__":
    main()