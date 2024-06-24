# 安装scrapy库
pip install scrapy
# 创建scrapy项目
scrapy startproject weather_data
# 进入项目并创建新的爬虫
cd weather_data
scrapy genspider wunderground wunderground.com
import scrapy
import datetime

class WundergroundSpider(scrapy.Spider):
    name = "wunderground"
    allowed_domains = ["wunderground.com"]
    start_urls = []

    # 定义要爬取的城市列表（需要自行添加更多城市）
    cities = {
        "UK": ["London", "Manchester", "Birmingham"],
        "US": ["New York", "Los Angeles", "Chicago"],
        "CN": ["Beijing", "Shanghai", "Guangzhou"]
    }

    # 生成start_urls
    def __init__(self, *args, **kwargs):
        super(WundergroundSpider, self).__init__(*args, **kwargs)
        base_url = "https://www.wunderground.com/history/monthly/{city}/date/{year}-{month}"
        for country, cities in self.cities.items():
            for city in cities:
                for year in range(2018, 2021):
                    for month in range(1, 13):
                        url = base_url.format(city=city, year=year, month=month)
                        self.start_urls.append(url)

    def parse(self, response):
        city = response.url.split('/')[5]
        year_month = response.url.split('/')[-1]
        data = {
            "city": city,
            "year_month": year_month,
            "average_temperature": None,
        }

        # 提取平均气温数据
        try:
            temp_element = response.xpath('//td[@class="ng-star-inserted"]/span/text()').get()
            data["average_temperature"] = float(temp_element.strip())
        except Exception as e:
            self.logger.error(f"Failed to parse {response.url}: {e}")

        yield data