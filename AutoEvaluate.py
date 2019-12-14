#!/usr/bin/env python
# coding: utf-8

import requests
import re
import time
import json
from bs4 import BeautifulSoup

onestop_data = {'username': 'Your user name', # 填入用户名
                'password': 'Your password', # 填入密码
                'remember': 'checked'}

# ------------------- login onestop -------------------------
onestop_link = "http://onestop.ucas.ac.cn/Ajax/Login/0"

headers = { # 请求头信息
    'X-Requested-With': 'XMLHttpRequest'
}

o = requests.Session()
Onestop_Login = o.post(url = onestop_link, data = onestop_data, headers = headers, verify=False, timeout=10)
res = json.loads(Onestop_Login.text)

if (res['f'] == False): # check login status
    raise Exception(res['msg'])
else:
    print("ONESTOP LOGIN SUCCESS")
# -------------------------------------------------------

# ------------------- login sep -------------------------
s = requests.Session()
Sep_Login = s.get(url=res['msg'],verify=False,timeout=10) # login
sl = BeautifulSoup(Sep_Login.text, 'lxml')


if (sl.find('a',title='退出系统') == None): # check login status
    raise Exception("Sep Login Error")
else:
    print("SEP LOGIN SUCCESS")
# -------------------------------------------------------

# -------------------  login jwxk -----------------------
jwxk = s.get('http://sep.ucas.ac.cn/portal/site/226/821')
jwxk = BeautifulSoup(jwxk.text, 'lxml')
j_link = jwxk.noscript.meta.attrs['content'][6:]

c = requests.Session()
j_login = c.get(url=j_link,cookies = s.cookies.get_dict())
requests.utils.add_dict_to_cookiejar(c.cookies, {'sepuser': s.cookies.get_dict()['sepuser']}) # set jwxk cookies
# -------------------------------------------------------

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


# ----------------  Course Evaluation -------------------
print('Course Evaluation')
EvaPage = c.get("http://jwxk.ucas.ac.cn/evaluate/course/59585")
eva = BeautifulSoup(EvaPage.text, 'lxml')
hrefnum = re.compile(r"(\d+)")

for row in eva.find_all('tr'): 
    rowa = row.find_all('a')
    if (rowa == []): continue
    href = rowa[3].get('href')
    rowstr = list(map(lambda x: x.string, rowa))
    if (rowstr[3] == '评估'):
        CourseNum = hrefnum.findall(href)[0]
        res = c.post("http://jwxk.ucas.ac.cn/evaluate/saveCourseEval/" + CourseNum, data = cdata)
        print(rowstr[0:4])
        time.sleep(1)
print('Done')
    
    
# ----------------  Teacher Evaluation -------------------
print('Teacher Evaluation')
EvaPage = c.get("http://jwxk.ucas.ac.cn/evaluate/teacher/59585")
eva = BeautifulSoup(EvaPage.text, 'lxml')
hrefnum = re.compile(r"(\d+)")

for row in eva.find_all('tr'): 
    rowa = row.find_all('a')
    if (rowa == []): continue
    href = rowa[3].get('href')
    rowstr = list(map(lambda x: x.string, rowa))
    if (rowstr[3] == '评估'):
        CourseNum = hrefnum.findall(href)[0]
        TeacherNum = hrefnum.findall(href)[1]
        res = c.post("http://jwxk.ucas.ac.cn/evaluate/saveTeacherEval/" + CourseNum + '/' + TeacherNum, data = tdata)
        print(rowstr[0:4])
        time.sleep(1)
print('Done')