from dianping_spider import DianPingSpider
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='一个大众点评爬虫示例')
    parser.add_argument('--keyword', '-k', default='美术培训', type=str, help='搜索关键词')
    parser.add_argument('--cityid', '-c', default=160, type=int, help='城市代码')
    parser.add_argument('--numpages', '-n', default=2, type=int, help='搜索页面数量')
    parser.add_argument('--output', '-o', default='dianpin.csv', type=str, help='输出文件路径')
    args = parser.parse_args()
    spider = DianPingSpider(keyword=args.keyword, city_id=args.cityid, num_pages=args.numpages)
    try:
        spider.crawl()
    except Exception as e:
        return
    spider.save_csv(args.output)
    os.system("pause")

if __name__ == "__main__":
    main()