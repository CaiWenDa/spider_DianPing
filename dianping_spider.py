from bs4 import BeautifulSoup
import time
import re
import random
from browser_client import BrowserClient
import saver
from logger import logger

class DianPingSpider:
    def __init__(self, keyword, city_id, num_pages, wait_range, output_file):
        self.keyword = keyword
        self.city_id = city_id
        self.num_pages = num_pages
        self.shop_data = [["店铺名称", "电话"]]
        self.browser_client = BrowserClient()
        self.wait_range = wait_range
        self.output_file = output_file

    def parse_shop_page(self, shop_url):
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
        if not phone_str or not phone_str:
            raise Exception("未找到数据")
        logger.info(f"抓取到店铺: {shop_name}, 电话: {phone_str}")
        return [shop_name, phone_str]

    def random_wait(self, wait_range):
        if len(wait_range) == 2:
            min_seconds, max_seconds = wait_range
            time.sleep(random.randint(min_seconds, max_seconds))
        else:
            time.sleep(2)

    def get_data(self):
        return self.shop_data

    def save_csv(self, output_file):
        saver.save_csv(output_file, self.shop_data)
        logger.info(f"数据已保存到 {output_file}")

    def add_csv_row(self, output_file, row):
        saver.add_csv_row(output_file, row)
        logger.info(f"已添加新行到 {output_file}: {row}")

    def crawl(self):
        count = 0
        base_url = f"https://www.dianping.com/search/keyword/{self.city_id}/0_{self.keyword}"
        url = base_url
        try:
            self.browser_client.get(base_url)
            logger.info("登录判定中...")
            self.browser_client.wait_for_element('class name', "tit", timeout=60)
            logger.info(f"成功访问页面: {base_url}")
        except Exception as err:
            logger.error(f"初始页面访问失败: {err}")
            self.browser_client.close()
            raise err
        for page_num in range(1, self.num_pages + 1):
            if page_num > 1:
                url = base_url + f"/p{page_num}"
            try:
                self.browser_client.get(url)
                self.browser_client.wait_for_element('class name', "tit", timeout=60)
                html = self.browser_client.get_page_source()
                soup = BeautifulSoup(html, 'html.parser')
                div_tit_tags = soup.find_all('div', {'class': 'tit'})
                for div_tit in div_tit_tags:
                    shop_url = div_tit.a.attrs['href'] if div_tit.a else None
                    logger.info(f"解析店铺链接: {shop_url}")
                    if shop_url:
                        try:
                            shop_item = self.parse_shop_page(shop_url)
                            self.shop_data.append(shop_item)
                            self.add_csv_row(self.output_file, shop_item)
                            count += 1
                        except Exception as err:
                            logger.error(f"解析店铺失败: {shop_url}, 错误: {err}")
                        self.random_wait(self.wait_range)
            except Exception as err:
                logger.error(f'[第{page_num}页] 发生错误，检查是否登录: {err}')
                continue
        
        logger.info(f"成功解析 {count} 条目")
        self.browser_client.close()