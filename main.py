# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Use a breakpoint in the code line below to debug your script.
# Press Ctrl+F8 to toggle the breakpoint.
# Press the green button in the gutter to run the script.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# encoding=utf-8
# -*- coding:utf-8 -*-
import time
from io import BytesIO
from urllib.request import *
from urllib.parse import *
from pytesseract import *
from bs4 import *
from PIL import Image
import requests

if __name__ == '__main__':
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    base_url = 'http://jw2.hustwenhua.net/(dcqnb1mruki253rbjvgqa5zi)/default2.aspx'
    req = Request(base_url, headers=headers)

    resp = urlopen(req)

    form_url = resp.url

    resp_data = BeautifulSoup(resp.read(),"html.parser")

    login_data = {
        'Button1': '',
        'lbLanguage': '',
        'hidPdrs': '',
        'hidsc': ''
    }

    form_content = resp_data.find('form')

    __VIEWSTATE = form_content.find('input')
    login_data['__VIEWSTATE'] = __VIEWSTATE['value']

    login_data['txtUserName'] = '*********'#请输入你的学号

    login_data['textbox1'] = ''

    login_data['textbox2'] = '*********'#请输入你的密码

    login_data['RadioButtonList1'] = "学生"

    captcha_url = urljoin(form_url, 'CheckCode.aspx')
    req_captcha = Request(captcha_url, headers=headers)
    captcha_resp = urlopen(req_captcha)
    img = Image.open(BytesIO(captcha_resp.read())).convert('L')
    s = image_to_string(img)
    img.show()
    s = input()
    login_data['txtSecretCode'] = s

    login_req = Request(form_url, data=urlencode(login_data, encoding='gb2312').encode('gb2312'), headers=dict(headers, **{'Referer':form_url}))

    list_ = [None]

    for _ in list_:

     login_resp = urlopen(login_req)

     data = BeautifulSoup(login_resp.read(),"html.parser")

     xiangdui_url = data.find(name='a', text='成绩查询')['href']
     cj_url = urljoin(login_resp.url,xiangdui_url)

     urlhtml = requests.get(cj_url,headers=dict(headers, **{'Referer':login_resp.url}))

     soup = BeautifulSoup(urlhtml.text, 'lxml')

     # req1 = Request(cj_url,headers=dict(headers, **{'Referer':login_resp.url}))

     max_score_req_data = {
         '__EVENTTARGET':'',
         '__EVENTARGUMENT':'',
         'hidLanguage:':'',
         'ddlXN':'',
         'ddlXQ':'',
         'ddl_kcxz':'',
         'btn_zg':'课程最高成绩'
     }
     __VIEWSTATE1 = soup.find('input',{'name':'__VIEWSTATE'})
     max_score_req_data['__VIEWSTATE'] = __VIEWSTATE1['value'] # TODO

     urlhtml2 = requests.post(cj_url,headers=dict(headers,**{'Referer':cj_url.encode('gb2312')}), data=max_score_req_data)

     soup2 = BeautifulSoup(urlhtml2.text, 'lxml')

     alink = soup2.find_all('td')
     print(alink)

     time.sleep(20)








