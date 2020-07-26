import scrapy
from scrapy.selector import Selector
from spiders.items import SpidersItem


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):
        movies = Selector(response=response).xpath('//div[@class="channel-detail movie-item-title"]')
        for movie in movies[:10]:
            item = SpidersItem()
            title = movie.xpath('./a/text()')
            link = movie.xpath('./a/@href')
            item['title'] = title.extract_first().strip()
            item['link'] = 'https://maoyan.com' + link.extract_first().strip()  # 拼接完整的 url
            yield scrapy.Request(url=item['link'], meta={'item': item}, callback=self.parse2)

    def parse2(self, response):
        item = response.meta['item']
        info = Selector(response=response).xpath('//div[@class="movie-brief-container"]')
        types = info.xpath('./ul/li/a/text()').extract()
        date = info.xpath('./ul/li[last()]/text()').extract_first().strip()
        item['types'] = types
        item['date'] = date

        yield item
