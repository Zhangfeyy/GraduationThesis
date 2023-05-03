from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

import xlwt
import xlrd
from bs4 import BeautifulSoup
import time
import json

book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('个人主页', cell_overwrite_ok=True)
sheet.write(0, 0, '昵称')
sheet.write(0, 1, '性别')
sheet.write(0, 2, '关注数')
sheet.write(0, 3, '粉丝数')
sheet.write(0, 4, '获赞数')
sheet.write(0, 5, '播放数')

data_excel = xlrd.open_workbook('../search_video/UpList.xls')
table = data_excel.sheets()[0]
names = table.col_values(2, start_rowx=1, end_rowx=None)


def save_to_excel():
    global n

    all_h = browser.window_handles
    browser.switch_to.window(all_h[0])
    time.sleep(2)

    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    username = soup.find(id='h-name').string
    gender = soup.find(id='h-gender').attrs['class']
    ins = soup.find(id='n-gz').string
    fans = soup.select('p#n-fs')[0].string
    likes = soup.select('p#n-bf')[0].string
    plays = soup.select('p#n-bf')[1].string
    print(f'爬取: {username} 性别: {gender} 关注数: {ins} 粉丝数: {fans} 获赞数: {likes} 播放量: {plays}')

    sheet.write(n, 0, username)
    sheet.write(n, 1, gender)
    sheet.write(n, 2, ins)
    sheet.write(n, 3, fans)
    sheet.write(n, 4, likes)
    sheet.write(n, 5, plays)


def search_name(name):
    time.sleep(1)
    input_elem = browser.find_element(By.CSS_SELECTOR, '.search-input-el')
    input_elem.send_keys(name)
    input_elem.send_keys(Keys.ENTER)


def goto_page():
    global n
    try:
        link = WAIT.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'a.text1.p_relative')))
        link.click()
        browser.close()
        save_to_excel()
    except TimeoutException:
        print('超时')
    n += 1


if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=options)
    browser.set_window_size(1920, 1080)
    WAIT = WebDriverWait(browser, 10)

    n = 1
    browser.get('https://search.bilibili.com/upuser')

    browser.delete_all_cookies()
    with open('jsoncookie.json', 'r') as f:
        ListCookies = json.loads(f.read())

    for cookie in ListCookies:
        browser.add_cookie({
            'domain': 'bilibili.com',
            'name': cookie['name'],
            'value': cookie['value'],
            'path': '/',
            'expires': None,
            'httponly': False,
        })

    browser.get('https://search.bilibili.com/upuser')

    for name in names:
        print(name)
        browser.get('https://search.bilibili.com/upuser')
        search_name(name)
        goto_page()

    browser.quit()

book.save('个人信息统计3.xls')
print(f'共爬取{n - 1}条信息')
