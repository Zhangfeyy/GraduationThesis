from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

import xlwt
from bs4 import BeautifulSoup
import time
import json

book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('美妆区UP主信息统计', cell_overwrite_ok=True)
sheet.write(0, 0, '视频名称')
sheet.write(0, 1, '观看次数')
sheet.write(0, 2, 'UP主')

n = 1


def get_source():
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    save_to_excel(soup)


def save_to_excel(soup):
    global n
    infos = soup.find_all(class_='bili-video-card__wrap __scale-wrap')
    for info in infos:
        global n
        title = info.find(class_='bili-video-card__info--tit').get_text()
        views = info.select('.bili-video-card__stats--item > span')[0].string
        up = info.find(class_='bili-video-card__info--author').string
        print(f'爬取: {title} up主: {up} 观看次数: {views}')
        sheet.write(n, 0, title)
        sheet.write(n, 1, views)
        sheet.write(n, 2, up)
        n += 1


def turn_page(btn):
    time.sleep(1)
    print('获取到相应的元素了')
    btn.click()
    get_source()


def next_page(page_num):
    WAIT = WebDriverWait(browser, 5)
    try:
        print(f'正在爬取：{page_num}')
        next_btn = WAIT.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div/div[2]/div/div/button[10]')))
        turn_page(next_btn)
    except TimeoutException:
        try:
            print('尝试获取元素2')
            next_btn = WAIT.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div[2]/div/div/button[10]')))
            turn_page(next_btn)
        except TimeoutException:
            try:
                print('尝试获取元素3')
                next_btn = WAIT.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div[2]/div/div/button[9]')))
                turn_page(next_btn)
            except TimeoutException:
                print('出现故障')
                return next_page(page_num)


if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=options)
    browser.set_window_size(1920, 1080)

    browser.get('https://www.bilibili.com/')
    browser.delete_all_cookies()
    with open('jsoncookie.json', 'r') as f:
        ListCookies = json.loads(f.read())
    for cookie in ListCookies:
        browser.add_cookie({
            'domain': '.bilibili.com',
            'name': cookie['name'],
            'value': cookie['value'],
            'path': '/',
            'expires': None,
            'httponly': False,
        })

    browser.get('https://www.bilibili.com/')
    input = browser.find_element(By.CSS_SELECTOR, '#nav-searchform > div.nav-search-content > input')
    time.sleep(2)
    input.send_keys('跟着B站UP主学化妆')
    input.send_keys(Keys.ENTER)

    all_h = browser.window_handles
    browser.switch_to.window(all_h[1])
    total_btn = browser.find_element(By.CSS_SELECTOR,
                                     "#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div > div.flex_center.mt_x50.mb_x50 > div > div > button:nth-child(10)")
    total = int(total_btn.text)
    print(f'总页数: {total}')
    get_source()

    for i in range(2, total + 1):
        next_page(i)

    browser.quit()

book.save('UpList.xls')
print(f'共爬取{n - 1}条信息')
