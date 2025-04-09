import re
import time
from pymysql import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv
import os
import json
from utils.query import querys


def init():
    try:
        conn = connect(host='localhost', user='root', passwd='root', database='steamdata', port=3306, charset='utf8mb4')
        sql = '''
                create table games(
                    id int primary key autoincrement,
                    title varchar(255),
                    icon varchar(2555),
                    time varchar(255),
                    compatible varchar(255),
                    evaluate varchar(255),
                    discount varchar(255),
                    original_price varchar(255),
                    now_price varchar(255),
                    types varchar(2555),
                    summary text,
                    recentlyComment varchar(255),
                    allComment varchar(255),
                    firm varchar(255),
                    publisher varchar(255),
                    imgList text,
                    video text,
                    detailLink varchar(2555)
                )
                '''
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except:
        pass
    if not os.path.exists('./temp1.csv'):
        with open('./temp1.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(
                ["title", "icon", "time", "compatible", "evaluate", "discount", "original_price", "now_price",
                 "detailLink"]
            )


def save_to_csv(rowData):
    with open('./temp1.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(rowData)
        print('saved')


def save_to_sql():
    with open('./temp1.csv', 'r', encoding='utf-8') as r_f:
        reader = csv.reader(r_f)
        for i in reader:
            if i[0] == 'title':
                continue
            querys('''
                insert into games (title, icon, time, compatible, evaluate, discount, original_price, now_price, detailLink)
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
            ''', [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]])

def spider(spiderTarget, startPage):
    print('URL' + spiderTarget % startPage)
    browser = startBrowser()
    browser.get(spiderTarget % startPage)
    time.sleep(5)
    scroll_position = 0
    scroll_amount = 200
    max_scroll_amount = 2000
    while scroll_position < max_scroll_amount:
        scroll_script = f"window.scrollBy(0, {scroll_amount})"
        browser.execute_script(scroll_script)
        scroll_position += scroll_amount
        time.sleep(0.5)
    game_List = browser.find_elements(by=By.XPATH, value="//a[@class='search_result_row ds_collapse_flag  app_impression_tracked']")

    for game in game_List:
        try:
            title = game.find_element(by=By.XPATH,
                                      value="./div[@class='responsive_search_name_combined']/div[1]/span[@class='title']").text
            icon = game.find_element(by=By.XPATH, value="./div[@class='col search_capsule']/img").get_attribute('src')
            compatibleList = game.find_elements(by=By.XPATH,
                                                value="./div[@class='responsive_search_name_combined']/div[1]/div/span")
            compatible = []
            for i in compatibleList:
                if (re.search('win', i.get_attribute("class"))):
                    compatible.append(re.search('win', i.get_attribute("class")).group())
                elif (re.search('mac', i.get_attribute("class"))):
                    compatible.append(re.search('mac', i.get_attribute("class")).group())
                elif (re.search('linux', i.get_attribute("class"))):
                    compatible.append(re.search('linux', i.get_attribute("class")).group())
            times = game.find_element(by=By.XPATH, value="./div[@class='responsive_search_name_combined']/div[2]").text
            evaluate = ''
            if re.search('mixed', game.find_element(by=By.XPATH,
                                                    value="./div[@class='responsive_search_name_combined']/div[3]/span").get_attribute(
                    'class')):
                evaluate = 'Mixed'
            else:
                evaluate = 'Positive'
            try:
                discount = 100 - int(re.search('\d+', game.find_element(by=By.XPATH,
                                                                        value=".//div[@class='discount_pct']").text).group())
            except:
                discount = 0
            original_price = float(re.search(r'\b\d+\.\d+\b', game.find_element(by=By.XPATH,
                                                                                value=".//div[@class='discount_original_price']").text).group())
            now_price = float(re.search(r'\b\d+\.\d+\b', game.find_element(by=By.XPATH,
                                                                           value=".//div[@class='discount_final_price']").text).group())
            detailLink = game.get_attribute('href')
            print(detailLink)
            save_to_csv([title, icon, times, json.dumps(compatible), evaluate, discount, original_price, now_price, detailLink])

        except:
            pass

def startBrowser():
    service = Service('./chromedriver.exe')
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(service=service, options=option)

    return browser

def main(spiderTarget):
    # for i in range(1, 10):
    #    spider(spiderTarget, i)
    save_to_sql()

if __name__ == '__main__':
    spiderTarget = 'https://store.steampowered.com/search/?specials=1&page=%s'
    main(spiderTarget)