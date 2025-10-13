from dianping_spider import DianPingSpider
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='一个大众点评爬虫示例')
    parser.add_argument('--keyword', '-k', required=True, type=str, help='搜索关键词')
    parser.add_argument('--city_id', '-c', required=True, type=int, help='城市代码')
    parser.add_argument('--num_pages', '-n', default=1, type=int, help='搜索页面数量')
    parser.add_argument('--output', '-o', default='dianpin.csv', type=str, help='输出文件路径')
    parser.add_argument('--wait_range', '-w', nargs=2, type=int, metavar=('MIN', 'MAX'), help='等待秒数的最小值和最大值（必须同时指定）')
    args = parser.parse_args()
    if args.wait_range and len(args.wait_range) != 2:
        parser.error('必须同时指定最小值和最大值，或都不指定')
    elif args.wait_range and len(args.wait_range) == 2 and args.wait_range[0] >= args.wait_range[1]:
        parser.error('最小值必须小于最大值')
    else:
        wait_range = args.wait_range if args.wait_range else [2, 5]
    spider = DianPingSpider(keyword=args.keyword, city_id=args.city_id, num_pages=args.num_pages, wait_range=wait_range, output_file=args.output)
    try:
        spider.crawl()
    except Exception as e:
        return
    os.system("pause")

if __name__ == "__main__":
    main()