from dianping_spider import DianPingSpider
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='一个大众点评爬虫示例')
    parser.add_argument('--keyword', '-k', default='美术培训', type=str, help='搜索关键词')
    parser.add_argument('--cityid', '-c', default=160, type=int, help='城市代码')
    parser.add_argument('--numpages', '-n', default=2, type=int, help='搜索页面数量')
    parser.add_argument('--output', '-o', default='dianpin.csv', type=str, help='输出文件路径')
    parser.add_argument('--range', '-r', nargs=2, type=int, metavar=('MIN', 'MAX'), help='等待秒数的最小值和最大值（必须同时指定）')
    args = parser.parse_args()
    if args.range and len(args.range) != 2:
        parser.error('必须同时指定最小值和最大值，或都不指定')
    elif args.range and len(args.range) == 2 and args.range[0] >= args.range[1]:
        parser.error('最小值必须小于最大值')
    else:
        wait_range = args.range if args.range else [2, 5]
    spider = DianPingSpider(keyword=args.keyword, city_id=args.cityid, num_pages=args.numpages, wait_range=wait_range)
    try:
        spider.crawl()
        spider.save_csv(args.output)
    except Exception as e:
        return
    os.system("pause")

if __name__ == "__main__":
    main()