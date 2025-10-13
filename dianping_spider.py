from bs4 import BeautifulSoup
import time
import re
import random
from browser_client import BrowserClient
from saver import save_csv

class DianPingSpider:
    def __init__(self, keyword, cityid, numpage):
        self.keyword = keyword
        self.cityid = cityid
        self.numpage = numpage
        self.data = [["店铺名称", "电话"]]
        self.browser = BrowserClient()

    def parse_shop(self, shop_url):
        try:
            self.browser.get(shop_url)
            page_source = self.browser.get_page_source()
            soup = BeautifulSoup(page_source, 'html.parser')
            # 获取店铺名称
            span_shopName = soup.find('span', {'class': 'shopName'})
            shopName = ''
            if span_shopName:
                shopName = span_shopName.get_text()
            # 获取电话
            script_txt = soup.prettify()
            m = re.search(r'"phoneNos":\s*\[(.*?)\]', script_txt)
            phone_num_list = []
            if m:
                raw_phone_num = m.groups()[0].replace('"', '')
                phone_num_list = raw_phone_num.split(",")
            phone_num = ' '.join(phone_num_list) if phone_num_list else ''
            print(shopName, phone_num_list)
            self.data.append([shopName, phone_num])
        except Exception as e:
            print(f"解析店铺失败: {shop_url}, 错误: {e}")

    def random_wait(self, min_seconds, max_seconds):
        time.sleep(random.randint(min_seconds, max_seconds))
    
    def get_data(self):
        return self.data

    def save_csv(self, output_file):
        save_csv(output_file, self.data)

    def crawl(self):
        for page in range(1, self.numpage):
            if page == 1:
                url = f"https://www.dianping.com/search/keyword/{self.cityid}/0_{self.keyword}"
            else:
                url = f"https://www.dianping.com/search/keyword/{self.cityid}/0_{self.keyword}/p{page}"
            try:
                self.browser.get(url)
                print("登录判定")
                self.browser.wait_for_element('class name', "tit", timeout=20)
                print(f"成功访问页面: {url}")
                page_source = self.browser.get_page_source()
                soup = BeautifulSoup(page_source, 'html.parser')
                div_tits = soup.find_all('div', {'class': 'tit'})
                for tit in div_tits:
                    shop_link = tit.a.attrs['href'] if tit.a else None
                    print(shop_link)
                    if shop_link:
                        self.parse_shop(shop_link)
                        self.random_wait(2, 5)
            except Exception as err:
                print(f'[第{page}页] 发生错误: {err}')
                continue
        self.browser.close()