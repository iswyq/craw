import scrapy


# 百度的爬虫
class BaiduTextSpider(scrapy.Spider):
    name = 'baidu_text'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
