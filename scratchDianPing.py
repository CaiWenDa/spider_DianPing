from dianping_spider import DianPingSpider
import argparse

def main():
    parser = argparse.ArgumentParser(description='一个大众点评爬虫示例')
    parser.add_argument('--keyword', '-k', default='美术培训', type=str, help='搜索关键词')
    parser.add_argument('--cityid', '-c', default=160, type=int, help='城市代码')
    parser.add_argument('--numpage', '-n', default=2, type=int, help='搜索页面数量')
    parser.add_argument('--output', '-o', default='dianpin.csv', type=str, help='输出文件路径')
    args = parser.parse_args()
    spider = DianPingSpider(keyword=args.keyword, cityid=args.cityid, numpage=args.numpage)
    spider.crawl()
    spider.save_csv(args.output)

if __name__ == "__main__":
    main()