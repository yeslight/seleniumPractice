# -*- coding: utf-8 -*-

import base64
import os
import ssl
import sys
import time
from random import randint
from qiniu import Auth, put_file, etag
import qiniu.config
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
    QN_AK = os.environ['QN_AK']
except:
    # 本地调试用
    QN_AK = ''
    
try:
    QN_SK = os.environ['QN_SK']
except:
    # 本地调试用
    QN_SK = ''

try:
    BUCKET_NAME = os.environ['BUCKET_NAME']
except:
    # 本地调试用
    BUCKET_NAME = ''

policy={

 }

def urlDecode(s):
    return str(base64.b64decode(s + '=' * (4 - len(s) % 4))).split('\'')[1]

def delay(i):
    time.sleep(i)

def push(body):
    print('- waiting for push result')
    # tg push
    if TG_BOT_TOKEN == '' or TG_USER_ID == '':
        print('*** No TG_BOT_TOKEN or TG_USER_ID ***')
    else:
        server = 'https://api.telegram.org'
        tgurl = server + '/bot' + TG_BOT_TOKEN + '/sendMessage'
        rq_tg = requests.post(tgurl, data={'chat_id': TG_USER_ID, 'text': body}, headers={
            'Content-Type': 'application/x-www-form-urlencoded'})
        if rq_tg.status_code == 200:
            print('- tg push Done!')
        else:
            print('*** tg push fail! ***', rq_tg.content.decode('utf-8'))
    print('- finish!')
    # kill_browser()
    
def openAndGetMail():
    driver.tab_new(urlMail)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(5)
    global EMAIL
    try:
        times = 1
        while len(EMAIL)<8:
            time.sleep(2)
            print('***开始获取邮箱')
            EMAIL = str(driver.find_element(By.CLASS_NAME, 'mail.icon.copyable').get_attribute("data-clipboard-text"))
            if times >5:
                break
    except Exception as e:
        print('Error:', e)
    print('***获取到邮箱：' + EMAIL)
    delay(1)
    driver.switch_to.window(driver.window_handles[0])
    
def loginStep1():
    write(EMAIL, into=S('@email'))
    delay(2)
    click('send passcode to email')
    time.sleep(5)
    
def loginStep2():
    print('***填入code' )
    write(EMAIL_CODE, into=S('@mailcode'))
    delay(2)
    click('Register')
    time.sleep(5)
    print('***跳过邀请码' )
    driver.switch_to.default_content()
    click('Skip')
    time.sleep(10)
    
def getEmailCode():
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(5)
    table = driver.find_element(By.CLASS_NAME, 'ui.celled.selectable.table')
    table_rows = table.find_elements(By.TAG_NAME, 'tr')
    print('***总行数:'+str(len(table_rows)))
    times = 1
    try:
        while len(table_rows)<2:
            print('第'+str(times)+'等待')
            times = times+1
            time.sleep(2)
            table_rows = table.find_elements(By.TAG_NAME, 'tr')
    except Exception as e:
        print('Error:', e)
    table_rows[len(table_rows)-1].click()
    time.sleep(2)
    content = driver.find_element(By.ID, 'mailcard')
    content_rows = content.find_elements(By.TAG_NAME, 'b')
    
    if len(content_rows)>0:
        global EMAIL_CODE
        EMAIL_CODE = content_rows[len(content_rows)-1].text
        print('***验证码:'+EMAIL_CODE)
        driver.switch_to.window(driver.window_handles[0])

def getSubUrl():
    print('***进入sub页面' )
    go_to(urlCntentPage)
    delay(5)
    global SUB_URL
    print('***查找链接' )
    SUB_URL = str(driver.find_element_by_xpath('//button[text()="copy to clipboard"]').get_attribute("data-clipboard-text"))
    push(EMAIL+'\n\n'+SUB_URL)
    
def pushToQn():
    print('下载文件')
    r = requests.get(SUB_URL)
    with open("temp.yaml", "wb") as code:
        code.write(r.content)
    filename = 'gla.yaml'
    q = Auth(QN_AK, QN_SK)
    token = q.upload_token(BUCKET_NAME, filename, 3600, policy)
    localfile = './temp.yaml'
    ret, info = put_file(token, filename, localfile, version='v2')
    print(info)
    push('转存至七牛成功')

def checkin():
    print('***进入签到页面' )
    go_to(urlCheckin)
    delay(2)
    driver.find_element(By.CLASS_NAME, 'ui.positive.button').click()
    delay(5)
    print('***签到成功' )
    push('签到成功')


##
urlLogin = urlDecode('aHR0cHM6Ly9nbGFkb3Mucm9ja3MvcmVnaXN0ZXI=')
urlCntentPage = urlDecode('aHR0cHM6Ly9nbGFkb3Mucm9ja3MvY29uc29sZS9jbGFzaA==')
urlMail = urlDecode('aHR0cDovL3d3dy5seWh4eS5sb3Zl')
urlCheckin = urlDecode('aHR0cHM6Ly9nbGFkb3Mucm9ja3MvY29uc29sZS9jaGVja2lu')
EMAIL = ''
EMAIL_CODE = ''
SUB_URL = ''
##
block = False
# robot = 0
#display = Display(visible=0, size=(800, 800))
#display.start()
print('- loading...')
driver = uc.Chrome(use_subprocess=True)
driver.set_window_size(785, 650)
delay(2)
set_driver(driver)
print('- 完成初始化...')


go_to(urlLogin)
openAndGetMail()
loginStep1()
getEmailCode()
if len(EMAIL_CODE)>1:
    print('***验证码有效，准备注册')
    loginStep2()
    getSubUrl()
    pushToQn()
    checkin()
else:
    print('***验证码获取异常')
