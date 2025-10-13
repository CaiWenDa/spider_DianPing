from bs4 import BeautifulSoup
import time
import re
import random
from browser_client import BrowserClient
from saver import save_csv
from logger import logger

class DianPingSpider:
    def __init__(self, keyword, city_id, num_pages):
        self.keyword = keyword
        self.city_id = city_id
        self.num_pages = num_pages
        self.shop_data = [["店铺名称", "电话"]]
        self.browser_client = BrowserClient()

    def parse_shop(self, shop_url):
        try:
            self.browser_client.get(shop_url)
            html = self.browser_client.get_page_source()
            soup = BeautifulSoup(html, 'html.parser')
            # 获取店铺名称
            shop_name_tag = soup.find('span', {'class': 'shopName'})
            shop_name = shop_name_tag.get_text() if shop_name_tag else ''
            # 获取电话
            html_text = soup.prettify()
            phone_match = re.search(r'"phoneNos":\s*\[(.*?)\]', html_text)
            phone_list = []
            if phone_match:
                raw_phone = phone_match.groups()[0].replace('"', '')
                phone_list = raw_phone.split(",")
            phone_str = ' '.join(phone_list) if phone_list else ''
            logger.info(f"抓取到店铺: {shop_name}, 电话: {phone_str}")
            self.shop_data.append([shop_name, phone_str])
        except Exception as e:
            logger.error(f"解析店铺失败: {shop_url}, 错误: {e}")

    def random_wait(self, min_seconds, max_seconds):
        time.sleep(random.randint(min_seconds, max_seconds))

    def get_data(self):
        return self.shop_data

    def save_csv(self, output_file):
        save_csv(output_file, self.shop_data)

    def crawl(self):
        for page_num in range(1, self.num_pages):
            if page_num == 1:
                url = f"https://www.dianping.com/search/keyword/{self.city_id}/0_{self.keyword}"
            else:
                url = f"https://www.dianping.com/search/keyword/{self.city_id}/0_{self.keyword}/p{page_num}"
            try:
                self.browser_client.get(url)
                logger.info("登录判定")
                self.browser_client.wait_for_element('class name', "tit", timeout=20)
                logger.info(f"成功访问页面: {url}")
                html = self.browser_client.get_page_source()
                soup = BeautifulSoup(html, 'html.parser')
                div_tit_tags = soup.find_all('div', {'class': 'tit'})
                for div_tit in div_tit_tags:
                    shop_url = div_tit.a.attrs['href'] if div_tit.a else None
                    logger.info(f"解析店铺链接: {shop_url}")
                    if shop_url:
                        self.parse_shop(shop_url)
                        self.random_wait(2, 5)
            except Exception as err:
                logger.error(f'[第{page_num}页] 发生错误: {err}')
                continue
        self.browser_client.close()