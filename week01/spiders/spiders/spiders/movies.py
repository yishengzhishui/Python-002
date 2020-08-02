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
        movies = Selector(response=response).xpath('//div[@class="movie-hover-info"]')
        for movie in movies[:10]:
            item = SpidersItem()
            item['title'] = movie.xpath('./div[1]/span[1]/text()').extract_first()
            item['types'] = movie.xpath('./div[2]/text()').extract()[1].strip()
            item['date'] = movie.xpath('./div[4]/text()').extract()[1].strip()
            yield item
