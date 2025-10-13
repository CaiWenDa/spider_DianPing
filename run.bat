::keyword 搜索关键词
set keyword="美术培训"
::city_id 城市ID，160 为郑州，其他城市参考 location.md 文件
set city_id=160
::num_pages 爬取页数
set num_pages=1
::wait_range 每次请求间隔时间范围，单位秒，两个数字表示最小和最大值
set wait_range=3 6
::output_file 输出文件路径
set output_file="dianping.csv"
python ./scratchDianPing.py --keyword %keyword% --city_id %city_id% --num_pages %num_pages% --wait_range %wait_range% --output_file %output_file%