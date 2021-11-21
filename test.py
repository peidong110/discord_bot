# # bwysched.p_search_fields
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import time
import requests

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("./fb-auth.json")
default_app = firebase_admin.initialize_app()

print(default_app.name)  # "[DEFAULT]"


from lxml import etree


#
# page = etree.HTML(html)
# tag_a = page.xpath('/html/body/option')
# course_abbr = []
# course_name = []
# for a in tag_a:
#     if a.attrib['value'] != '':
#         course_abbr.append(a.attrib['value'])
#         course_name.append(re.sub('\(.*?\)', '', a.text))
#     print(a.attrib)  # {'value': 'AFRI'}
#     # print(a.get('href'))
#     print(a.text)
#
# print(course_abbr)
# print(course_name)
