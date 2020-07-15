#!/usr/bin/env python
# coding: utf-8

import requests
import re
import time
import json
from bs4 import BeautifulSoup

onestop_data = {'username': 'Your Username', # 填入用户名
                'password': 'Your Password', # 填入密码
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
    'subjectiveRadio': 103,
    'subjectiveCheckbox': '110,',
    'item_88': 5,
    'item_89': 5,
    'item_90': 5,
    'item_92': 5,
    'item_93': 5,
    'item_94': 5,
    'item_95': 5,
    'item_96': 5,
    'item_116': 5,
    'item_117': 5,
    'item_118': 5,
    'item_119': 5,
    'item_120': 5,
    'item_122': 5,
    'item_123': 5,
    'item_124': 5,
    'item_125': 5,
    'item_126': 5,
    'item_128': 5,
    'item_129': 5,
    'item_130': 5,
    'item_131': 5,
    'item_97': '课程与作业（包括作业、报告、测验测试、论文等）有助于我的能力的提高',
    'item_98': '课程与作业（包括作业、报告、测验测试、论文等）有助于我的能力的提高',
    'item_99': '课程与作业（包括作业、报告、测验测试、论文等）有助于我的能力的提高',
    'item_100': '课程与作业（包括作业、报告、测验测试、论文等）有助于我的能力的提高',
    'item_101': '课程与作业（包括作业、报告、测验测试、论文等）有助于我的能力的提高',
    'radio_102': '103',
    'item_108': '110,'
}
tdata = {
    'subjectiveRadio': '',
    'subjectiveCheckbox': '',
    'item_133': 5,
    'item_134': 5,
    'item_136': 5,
    'item_137': 5,
    'item_139': 5,
    'item_140': 5,
    'item_141': 5,
    'item_142': 5,
    'item_143': 5,
    'item_144': 5,
    'item_148': 5,
    'item_149': 5,
    'item_150': 5,
    'item_151': 5,
    'item_152': 5,
    'item_153': 5,
    'item_155': 5,
    'item_156': 5,
    'item_157': 5,
    'item_158': 5,
    'item_159': 5,
    'item_145': '治学严谨、备课充分、讲课认真、因材施教',
    'item_146': '治学严谨、备课充分、讲课认真、因材施教'
}


# ----------------  Course Evaluation -------------------
print('Course Evaluation')
EvaPage = c.get("http://jwxk.ucas.ac.cn/evaluate/course/59587")
eva = BeautifulSoup(EvaPage.text, 'lxml')
hrefnum = re.compile(r"(\d+)")

for row in eva.find_all('tr'): 
    rowa = row.find_all('a')
    if (len(rowa) < 4): continue
    href = rowa[3].get('href')
    rowstr = list(map(lambda x: x.string, rowa))
    if (rowstr[3] == '评估'):
        CourseNum = hrefnum.findall(href)[1]
        res = c.post("http://jwxk.ucas.ac.cn/evaluate/saveCourseEval/59586/" + CourseNum, data = cdata)
        print(rowstr[0:4])
        time.sleep(1)
print('Done')
    
    
# ----------------  Teacher Evaluation -------------------
print('Teacher Evaluation')
EvaPage = c.get("http://jwxk.ucas.ac.cn/evaluate/teacher/59587")
eva = BeautifulSoup(EvaPage.text, 'lxml')
hrefnum = re.compile(r"(\d+)")

for row in eva.find_all('tr'): 
    rowa = row.find_all('a')
    if (len(rowa) < 4): continue
    href = rowa[3].get('href')
    rowstr = list(map(lambda x: x.string, rowa))
    if (rowstr[3] == '评估'):
        CourseNum = hrefnum.findall(href)[1]
        TeacherNum = hrefnum.findall(href)[2]
        res = c.post("http://jwxk.ucas.ac.cn/evaluate/saveTeacherEval/59586/" + CourseNum + '/' + TeacherNum, data = tdata)
        print(rowstr[0:4])
        time.sleep(1)
print('Done')
