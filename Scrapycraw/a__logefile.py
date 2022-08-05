import scrapy


class ALogefileSpider(scrapy.Spider):
    name = '--logefile'
    allowed_domains = ['.']
    start_urls = ['http://./']

    def parse(self, response):
        pass
