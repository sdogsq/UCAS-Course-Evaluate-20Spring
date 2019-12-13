#!/usr/bin/env python
# coding: utf-8

import requests
import re
import time
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt 
from bs4 import BeautifulSoup
# 请求头信息

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language': 'en',
    'Cache-Control': 'max-age=0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'DNT':'1',
    'Host':'sep.ucas.ac.cn',
    'Origin': 'http://sep.ucas.ac.cn',
    'Referer': 'http://sep.ucas.ac.cn/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}

regex = re.compile(r"'(.*?)'")

sep_link = "http://sep.ucas.ac.cn/slogin"

params_nocode = {'userName':'Your User Name', # 填入用户名
          'pwd':'Your password', #填入密码
          'sb':'sb'}


params_withcode = {'userName':'Your User Name',#填入用户名
          'pwd':'Your password', #填入密码
          'certCode': '',
          'sb':'sb'}


def localtime():
    return time.asctime( time.localtime(time.time()) )



s = requests.Session()
c = requests.Session()

# ------------------- login sep -------------------------
s = requests.Session()
Sep_Login = s.post(url=sep_link, data=params_nocode,headers=headers,verify=False,timeout=10) # login
sl = BeautifulSoup(Sep_Login.text, 'lxml')

if (sl.find('input', attrs={'name':'certCode'}) !=None):  # verCode needed
    vpic = s.get('http://sep.ucas.ac.cn/changePic?code='+str(int(round(time.time() * 1000))))
    image = Image.open(BytesIO(vpic.content))
    #image.show()
    plt.imshow(image)
    plt.show()
    
    #SendEmail(' 需要登录验证码 ','000')
    vcode = input()
    
    
    params_withcode['certCode'] = vcode
    Sep_Login = s.post(url=sep_link, data=params_withcode,headers=headers,verify=False,timeout=10) 
    sl = BeautifulSoup(Sep_Login.text, 'lxml')

if (sl.find('a',title='退出系统') == None): # check login status
    raise Exception("Sep Login Error")
else:
    print(" SEP LOGIN SUCCESS")
# -------------------------------------------------------

# -------------------  login jwxk ------------------------ 
jwxk = s.get('http://sep.ucas.ac.cn/portal/site/226/821')
jwxk = BeautifulSoup(jwxk.text, 'lxml')
j_link = jwxk.noscript.meta.attrs['content'][6:]

c = requests.Session()
j_login = c.get(url=j_link,cookies = s.cookies.get_dict())
requests.utils.add_dict_to_cookiejar(c.cookies, {'sepuser': s.cookies.get_dict()['sepuser']}) # set jwxk cookies
# -------------------------------------------------------


# ----------------- Evaluate Course ---------------------
cdata = { # Post Data
    'subjectiveRadio': 22,
    'subjectiveCheckbox': 28,
    'item_2': 5,
    'item_3': 5,
    'item_67': 5,
    'item_5': 5,
    'item_6': 5,
    'item_7': 5,
    'item_68': 5,
    'item_69': 5,
    'item_71': 5,
    'item_72': 5,
    'item_73': 5,
    'item_74': 5,
    'item_75': 5,
    'item_77': 5,
    'item_78': 5,
    'item_79': 5,
    'item_80': 5,
    'item_81': 5,
    'item_83': 5,
    'item_84': 5,
    'item_85': 5,
    'item_86': 5,
    'item_14': '作业（包括作业、报告、测验测试、论文等）有助于我的能力的提高',
    'item_15': '作业（包括作业、报告、测验测试、论文等）有助于我的能力的提高',
    'item_16': '作业（包括作业、报告、测验测试、论文等）有助于我的能力的提高',
    'item_17': '作业（包括作业、报告、测验测试、论文等）有助于我的能力的提高',
    'item_18': '作业（包括作业、报告、测验测试、论文等）有助于我的能力的提高',
    'radio_19': '',
    'item_25': ''
}
tdata = {
    'item_34': 5,
    'item_35': 5,
    'item_37': 5,
    'item_38': 5,
    'item_40': 5,
    'item_41': 5,
    'item_42': 5,
    'item_43': '作业（包括作业、报告、测验测试、论文等）有助于我的能力的提高',
    'item_44': '作业（包括作业、报告、测验测试、论文等）有助于我的能力的提高',
    'item_48': 5,
    'item_49': 5,
    'item_50': 5,
    'item_52': 5,
    'item_53': 5,
    'item_54': 5,
    'item_55': 5,
    'item_56': 5,
    'item_60': 5,
    'item_62': 5,
    'item_63': 5,
    'item_64': 5,
    'item_65': 5,
    'item_66': 5,
    'subjectiveCheckbox': '',
    'subjectiveRadio': ''
}

EvaPage = c.get("http://jwxk.ucas.ac.cn/evaluate/course/59585")

eva = BeautifulSoup(EvaPage.text, 'lxml')

hrefnum = re.compile(r"(\d+)")
for a in eva.find_all('a', string='评估', href=True):
    CourseNum = hrefnum.findall(a['href'])[0]
    res = c.post("http://jwxk.ucas.ac.cn/evaluate/saveCourseEval/" + CourseNum,data = cdata)
    print(CourseNum)
    time.sleep(1)

EvaPage = c.get("http://jwxk.ucas.ac.cn/evaluate/teacher/59585")

eva = BeautifulSoup(EvaPage.text, 'lxml')

hrefnum = re.compile(r"(\d+)")
for a in eva.find_all('a', string='评估', href=True):
    CourseNum = hrefnum.findall(a['href'])[0]
    TeacherNum = hrefnum.findall(a['href'])[1]
    res = c.post("http://jwxk.ucas.ac.cn/evaluate/saveTeacherEval/" + CourseNum + '/' + TeacherNum,data = tdata)
    print(CourseNum, TeacherNum)
    time.sleep(1)