from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import time


def get_source():
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    sob(soup)


def sob(soup):
    infos = soup.select("li.small-item.fakeDanmu-item")
    for info in infos:
        title = info.select('a.title')[0].string
        titles.append(title)


def turn_page(btn):
    time.sleep(1)
    print('下一页')
    btn.click()
    get_source()


def next_page(page_num):
    WAIT = WebDriverWait(browser, 5)
    try:
        print(f'正在爬取：{page_num}')
        next_btn = WAIT.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#submit-video-list > ul.be-pager > li.be-pager-next')))
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

    ids = [17075276, 34149649, 327750329, 11542441, 77587039, 402361670]
    for uid in ids:
        titles = []
        url = 'https://space.bilibili.com/%d/video'
        browser.get(url % uid)

        time.sleep(2)
        try:
            total_btn = browser.find_element(By.CSS_SELECTOR,
                                             "#submit-video-list > ul.be-pager > li:nth-child(6) > a")
            total = int(total_btn.text)
        except:
            try:
                total_btn = browser.find_element(By.CSS_SELECTOR,
                                                 "#submit-video-list > ul.be-pager > li:nth-child(5) > a")
                total = int(total_btn.text)
            except:
                print("出现故障")

        print(f'ID: {uid} 总页数: {total}')
        get_source()

        for i in range(2, total + 1):
            next_page(i)

        print(titles)

    browser.quit()
