# -*- coding: utf-8 -*-

import base64
import os
import ssl
import sys
import time
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
#from pyvirtualdisplay import Display
from helium import *

# 关闭证书验证
ssl._create_default_https_context = ssl._create_unverified_context

try:
	TG_BOT_TOKEN = os.environ['TG_BOT_TOKEN']
except:
	# 本地调试用
	TG_BOT_TOKEN = ''

try:
	TG_USER_ID = os.environ['TG_USER_ID']
except:
	# 本地调试用
	TG_USER_ID = ''

try:
	EMAIL = os.environ['EMAIL']
except:
	# 本地调试用
	EMAIL = ''

try:
	PWD = os.environ['PWD']
except:
	# 本地调试用
	PWD = ''

policy={

 }

def urlDecode(s):
	return str(base64.b64decode(s + '=' * (4 - len(s) % 4))).split('\'')[1]

def delay(i):
	time.sleep(i)

def push(body):
	printRealTime('- waiting for push result')
	# tg push
	if TG_BOT_TOKEN == '' or TG_USER_ID == '':
		printRealTime('*** No TG_BOT_TOKEN or TG_USER_ID ***')
	else:
		server = 'https://api.telegram.org'
		tgurl = server + '/bot' + TG_BOT_TOKEN + '/sendMessage'
		rq_tg = requests.post(tgurl, data={'chat_id': TG_USER_ID, 'text': body}, headers={
			'Content-Type': 'application/x-www-form-urlencoded'})
		if rq_tg.status_code == 200:
			printRealTime('- tg push Done!')
		else:
			printRealTime('*** tg push fail! ***', rq_tg.content.decode('utf-8'))
	printRealTime('- finish!')
	# kill_browser()

def login():
	printRealTime('开始登录')
	delay(2)
	write(EMAIL, into=S('#login-username'))
	delay(2)
	write(PWD, into=S('#login-password'))
	delay(2)
	click('登录')

def getCountry():
	delay(2)
	go_to(urlCntentPage)
	delay(2)
	table = driver.find_element(By.CLASS_NAME, 'Table__TableElement-sc-evwssh-0.dIoJPZ')
	table_rows = table.find_elements(By.TAG_NAME, 'tr')
	printRealTime('***总行数:'+str(len(table_rows)))
	
def printRealTime(msg):
	print(msg, flush=True)


##
urlLogin = urlDecode('aHR0cHM6Ly9hY2NvdW50cy5zcG90aWZ5LmNvbS96aC1DTi9sb2dpbg==')
urlCntentPage = urlDecode('aHR0cHM6Ly93d3cuc3BvdGlmeS5jb20vaGstemgvYWNjb3VudC9vdmVydmlldy8=')

##
block = False
# robot = 0
#display = Display(visible=0, size=(800, 800))
#display.start()
printRealTime('- loading...')
driver = uc.Chrome( use_subprocess=True)
driver.set_window_size(785, 650)
delay(2)
set_driver(driver)
printRealTime('- 完成初始化...')

r = requests.get("http://ip.p3terx.com")
printRealTime(str(r.text))

go_to(urlLogin)
login()
getCountry()
