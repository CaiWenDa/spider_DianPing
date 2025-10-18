# 基于 Selenium 的大众点评爬虫示例

## Python 开发环境
anaconda3  
conda-25.5.1  
python-3.14

## 安装
爬虫依赖于 Selenium 和 chrome/edge 浏览器，需要安装最新浏览器和对应版本的 Selenium 驱动程序以及 Python 的 Selenium，BeautifulSoup4 库

1. Selenium 驱动下载

Chrome：
```
https://googlechromelabs.github.io/chrome-for-testing/
```
Edge：
```
https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
```
2. 克隆存储库
```
git clone https://github.com/CaiWenDa/spider_DianPing.git
```

3. 将 Selenium 驱动复制到 spider_DianPing 目录下

4. 安装 Selenium 和 BeautifulSoup4
```
conda create -n scratch
conda activate scratch
conda install conda-forge::selenium
conda install conda-forge::beautifulsoup4
```

## 运行
### 方式一 (仅 Windows)

1. 下载 [Release](https://github.com/CaiWenDa/spider_DianPing/releases/tag/spider) 版本 exe
2. 确保 Selenium 驱动复制到和 exe 相同目录下
3. 修改 run.bat 参数 (参数说明见下方)
4. 直接运行 run.bat

### 方式二
```
python ./scratchDianPing.py [-h] --keyword KEYWORD --city_id CITY_ID [--num_pages NUM_PAGES] [--output OUTPUT] [--wait_range MIN MAX] [--browser {chrome,edge}]
```
## 说明
### 参数
```
[--help -h]
<--keyword -k KEYWORD> 搜索关键词
<--city_id -c CITY_ID> 城市id (详见 docs/lacation.md)
[--num_pages -n NUM_PAGES] 搜索页码范围
[--output -o OUTPUT] 输出文件路径
[--wait_range -w MIN MAX] 等待时间范围 [MIN, MAX] 秒
[--browser -b {chrome,edge}] 浏览器支持 chrome 或 edge
```

## 注意事项

- 由于大众点评的反爬非常严格，即使人工手动搜索频繁也很可能被封，爬虫爬取过程被封很常见，考虑将等待时间范围调大  
- 爬虫识别数据依赖网页格式，由于大众点评这类网站很可能会随时变化网页格式，爬虫可能失效，如果可能，尽量手动修改代码以应对这类情况  
- 本程序仅作为简单爬取示例，目前只能爬取商铺信息的名称和电话，如果需要其他信息，请自行手动修改代码实现，同时欢迎向本项目贡献代码

## 参阅
[城市代码说明](docs/location.md)  
[Selenium 文档](https://www.selenium.dev/documentation/)  
[Selenium Python 开发文档](https://selenium-python.readthedocs.io/index.html)