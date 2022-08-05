import scrapy


# CSDN的爬虫
class CsdnTitleSpider(scrapy.Spider):
    name = 'csdn_title'
    allowed_domains = ['www.csdn.net']
    start_urls = ['http://www.csdn.net/']

    def parse(self, response):
        pass
