from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import time
import re
import random
import csv

# 浏览器设置
def get_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    # 添加保持登录的数据路径：安装目录一般在 %userprofile%\AppData\Local\Google\Chrome\User Data
    home_dir_windows = os.environ['USERPROFILE']
    options.add_argument(r"user-data-dir={}\AppData\Local\Google\Chrome\Selenium Data".format(home_dir_windows))
    options.add_argument('--ignore-certificate-errors') 
    options.add_argument('--ignore-ssl-errors')
    return options

def save_csv(data):
    with open('dianpin.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerows(data)

# 初始化 driver
def init_chrome_driver():
    executable_paths=r".\chromedriver.exe"
    service = webdriver.ChromeService(executable_path=executable_paths)
    options = get_chrome_options()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

import argparse
# 创建解析器
parser = argparse.ArgumentParser(description='一个大众点评爬虫示例')
# 添加参数
parser.add_argument('--keyword', '-k', default='美术培训', type=str, help='搜索关键词')
parser.add_argument('--cityid', '-c', default=160, type=int, help='城市代码')
parser.add_argument('--numpage', '-n', default=2, type=int, help='搜索页面数量')
# 解析参数
args = parser.parse_args()

# 最大化窗口（默认不是最大化）
driver = init_chrome_driver()
driver.maximize_window()

i = 0
data = [["店铺名称", "电话"]]
search_keyword = args.keyword
city_id = args.cityid # 郑州=160
page_num = args.numpage
for page in range(1, page_num):
    # print(line) line 结尾有\n
    # 设置浏览器需要打开的url
    if page == 1:
        url = r"https://www.dianping.com/search/keyword/{}/0_{}".format(city_id, search_keyword)
    else:
        url = r"https://www.dianping.com/search/keyword/{}/0_{}/".format(city_id, search_keyword) + "p" + str(page)
    i += 1
    try:
        # 发送请求
        driver.get(url)
        print("登录判定")
        el = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.CLASS_NAME, "tit").is_displayed())
        print("成功访问页面")
        driver.get(url)
        page_source = driver.page_source
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(page_source, 'html.parser')
        # 定位浏览器窗口中元素
        div_tits = soup.find_all('div', {'class':'tit'})
        for tit in div_tits:
            shop_link = tit.a.attrs['href']
            print(shop_link)
            if shop_link:
                driver.get(shop_link)
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')

                # 获取店铺名称
                span_shopName = soup.find('span', {'class':'shopName'})
                shopName = ''
                if span_shopName:
                    shopName = span_shopName.get_text()
                
                # 获取电话
                script_txt = soup.prettify()
                m = re.search(r'"phoneNos":\s*\[(.*?)\]', script_txt)
                if m:
                    raw_phone_num = m.groups()[0].replace('"', '')
                    phone_num_list = raw_phone_num.split(",")
                print(shopName, phone_num_list)
                phone_num = ''
                if phone_num_list:
                    phone_num = ' '.join(phone_num_list)
                # 暂存数据
                data.append([shopName, phone_num])
            # 随机等待若干秒
            time.sleep(random.randint(2, 5))
    except Exception as err:
        print('[{}] '.format(i), err)
        continue

save_csv(data)
driver.close()