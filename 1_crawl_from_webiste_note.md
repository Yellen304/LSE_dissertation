# 基于Python爬取天气数据信息
| 以公开天气数据库Weather Underground(https://www.wunderground.com/history)为例


## 摘要
1. 基于scrapy框架[ChatGPT]

2. 基于不知道什么网络上找到的教程框架[https://blog.csdn.net/chen_5213/article/details/135129613]
- 如何打开网页的字符串文本（request.get）
- 如何对获取的字符串进行数据提取（xpath）
- 数据的存储与数据标准化处理
3. 基于beautiful soup4 框架


Appendix A. Code Dictionary

****
### 基于scrapy框架
```Python

# 安装scrapy库(此步在终端)
pip install scrapy
# 创建scrapy项目（此步在终端）
scrapy startproject weather_data
# 进入项目并创建新的爬虫（此步在终端）
cd weather_data
# genspider是scrapy库中的一个指令，在我的scrapy项目中创建一个名为“wunderground”的爬虫，该爬虫将以‘wunderground.com’为目标域名。
scrapy genspider wunderground wunderground.com
# 在weather_data/spiders/wunderground.py的文件中贴入以下
# 引入scrapy框架
import scrapy
# datetime是python标准库中的模块，用于处理日期和时间
import datetime
# class是定义了一个名为 WundergroundSpider的爬虫类
## name：爬虫的名称，用于在命令行中运行爬虫时指定。
## allowed_domains：爬虫允许爬取的域名列表，防止爬虫爬取其他网站。
## start_urls：初始URL列表，爬虫会从这些URL开始抓取数据

class WundergroundSpider(scrapy.Spider):
    name = "wunderground"
    allowed_domains = ["wunderground.com"]
    start_urls = []

    # 定义要爬取的城市列表（需要自行添加更多城市）
    cities = {
        "UK": {"Manchester": "EGCC", "London": "EGLL", "Birmingham": "EGBB"},
        "US": {"New York": "KJFK", "Los Angeles": "KLAX", "Chicago": "KORD"},
        "CN": {"Beijing": "ZBAA", "Shanghai": "ZSSS", "Guangzhou": "ZGGG"}
    }

    # 生成start_urls
    ## __init__：初始化方法，用于设置爬虫实例的初始状态。args和kwargs是参数设置
    ## base_url：一个格式化字符串，用于生成每个城市每个月的历史天气数据URL。
    ### 
    ## 循环遍历每个国家、每个城市、每个年份和每个月，生成完整的URL，并将其添加到start_urls列表中（先收集所有的网址）
    def __init__(self, *args, **kwargs):
        super(WundergroundSpider, self).__init__(*args, **kwargs)
        base_url = "https://www.wunderground.com/history/monthly/{code}/date/{year}-{month}"
        for country, cities in self.cities.items():
            for city in cities:
                for year in range(2018, 2021):
                    for month in range(1, 13):
                        url = base_url.format(city=city, year=year, month=month)
                        self.start_urls.append(url)
    # 解析响应
    ## parse：用于处理每个响应的方法。Scrapy会自动调用这个方法来解析从start_urls中抓取到的每个页面。
    ## city和year_month：从URL中提取城市名称和年月。
    ## data：一个字典，用于存储抓取到的数据，包含城市名称、年月和平均气温。
    ## try块：使用XPath提取页面中的平均气温数据。XPath是用于在XML和HTML文档中查找数据的语言。
    def parse(self, response):
        ### 使用斜杠/分割URL字符串，得到一个字符串列表。例如，对于URL https://www.wunderground.com/history/daily/EGCC/date/2018-6，分割后的列表是 ['https:', '', 'www.wunderground.com', 'history', 'daily', 'EGCC', 'date', '2018-6']
        city = response.url.split('/')[5]
        ### response.url.split('/')[5]：获取分割后列表的第六个元素（索引从0开始计数），即城市代码。对于上述示例URL，这个值是 EGCC。下面时间-1是指最后一个元素，即年月信息，因此这个值是‘2018-06’
        year_month = response.url.split('/')[-1]
        ### 创建数据字典。 ‘data’是一个字典，用于储存从URL中提取出来的信息以及后续提取的平均气温数据。在data这个字典中，将city放在‘city’这个键名下，把年月放在‘year_month’这个键名下，并初始化平均气温的键名，值设为missing value，在python中是none。
        data = {
            "city": city,
            "year_month": year_month,
            "average_temperature": None,
        }

        # 提取平均气温数据
        ## try块的使用可以使用Xpath提出页面中的平均气温数据。Xpath是用于在XML和HTML文档中查找数据的语言
        try:
            ### response.xpath()：response 是 Scrapy 在爬取页面时返回的响应对象。xpath() 方法用于在这个响应的HTML文档中查找符合特定XPath表达式的元素。
            ### //td[@class="ng-star-inserted"]/span/text()：这是一个XPath表达式，用于查找目标元素。
            ### //td：查找所有的 <td> 元素，不论它们在文档中的位置。
            ### [@class="ng-star-inserted"]：过滤 <td> 元素，只保留那些 class 属性值为 "ng-star-inserted" 的元素。
            ### /span：在前面筛选出的 <td> 元素中，查找它们的直接子元素 <span>。
            ### /text()：获取 <span> 元素中的文本内容。
            ### .get()：这个方法从匹配的元素中提取第一个元素的文本内容。如果没有匹配的元素，它会返回 None
            temp_element = response.xpath('//td[@class="history-monthly-summary"]/span/text()').get()
            ### 将获取到的数据存放在字典中
            data["average_temperature"] = float(temp_element.strip())
        ## 捕获异常并记录错误信息
        except Exception as e:
            self.logger.error(f"Failed to parse {response.url}: {e}")

        yield data

       ### 命令行输入如何输出的方式
       scrapy crawl wunderground -o weather_data.csv

```


### 基于Beautiful Soup框架
```
# 从模块或包中调用函数、变量(from module or package import variable or function)
## beautifulsoup适用于解析HTML和XML文件的库
from bs4 import BeautifulSoup
import random
## time 提供各种与时间相关的函数
import time
## selenium 是用于自动化浏览器操作的工具（注释：使程序等待网页五秒钟）
from selenium import webdriver

# 定义一段函数
## def用于定义函数，函数是一段可以重复使用的代码块，由函数名称和参数组成。语法为def function_name(parameters): ///return value
def fetch_page_content_with_selenium(url:str):
    # 使用Selenium启动浏览器
    driver = webdriver.Edge()
    driver.get(url)

    # 等待页面加载完成
    time.sleep(5)  # 你可以根据需要调整等待时间

    # 获取页面源代码
    page_source = driver.page_source

    # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(page_source, 'html.parser')

    # 关闭浏览器
    driver.quit()

    return soup
def crawl(website:str="https://www.wunderground.com/history/monthly/ZBNY/date/2024-6")->float:
    soup=fetch_page_content_with_selenium(website)
    raw=str(soup.contents)
    with open(website[website.index('-')+1:]+".txt",'w',encoding='utf-8')as f:
        f.write(raw)
    return 0
def parse(fileName:str)->float:
    with open(fileName,'r',encoding='utf-8') as f:
        raw=f.read()
    if 'Avg Tem' not in raw:
        return -1
    raw=raw[raw.index("Avg Temperature"):]
    raw=raw[:raw.index("</tr>")]
    raw=raw.split('</td>')
    raw=raw[1]
    raw=raw[raw.index('>')+1:]
    return float(raw)
    

if __name__=='__main__':
    answer=""
    for i in range(6,10):
        # avgtemp=crawl("https://www.wunderground.com/history/monthly/ZBNY/date/2018-"+str(i))
        avgtemp=parse(str(i)+".txt")
        print("%03d %.2f"%(i,avgtemp))
        answer+="%d,%.2f\n"%(i,avgtemp)
        # time.sleep(4)
    with open('data.csv','w')as f:
        f.write(answer)
        

```


## Appendix A. Code Dictionary
[xpath]
- 对获取的字符串进行数据提取

【第一次集中问题】
1. 有没有文件可以同时运行终端和编辑器的内容
2.  genspider是scrapy库中的一个指令吗
3. 什么是标准库中的模块
4. 什么是爬虫“类”
5. 什么是URL列表：就是网址
6.  定义初始化方式 def __init__(self, *args, **kwargs)的意思
    - 一种可变参数的构建方式， 没有指定key的参数会被储存在args里，指定key的参数被储存在kwargs里 [https://blog.csdn.net/Jiana_Feng/article/details/107861130]
  - 两种参数的实际运用 [https://cloud.tencent.com/developer/news/1349715]
7. 如何根据实际的URL地址来生成识别URL的字符串
   - 如果实际上的URL不是简单的"https://www.wunderground.com/history/monthly/{city}/date/{year}-{month}"怎么办，比如weather underground中的曼彻斯特2018年6月的URL是‘https://www.wunderground.com/history/daily/EGCC/date/2018-6’，这时候就需要回到上一步的地址代码列表，使用适当的城市代码来表示城市。例如"UK": {"Manchester": "EGCC", "London": "EGLL", "Birmingham": "EGBB"},
8. 什么是响应：request对对象发出请求
9. 看不懂它在【检查】页面提取的数据是在哪里找到的，我怎么没看见
10. 终端不可以复制粘贴吗
11. crawl这个指令在scrapy库中无法找到 [https://blog.csdn.net/qq_45476428/article/details/108719476]

**在obsidian中加入```的作用

