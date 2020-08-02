import scrapy
from scrapy.selector import Selector
from spiders.items import SpidersItem


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']
    header = {
        'Cookie': '__mta=108886717.1595746864015.1595746990576.1595750256786.5; uuid_n_v=v1; uuid=C4064090CF0D11EA84945F632DCF0A4D8D0B8CE986ED4FA1A5DF764899054947; _csrf=cc22244000e0cb4545dc4fba39835376bd716a9dfb32352439a8183eea8eaff7; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1595746863; _lxsdk_cuid=17389ecc837c8-0451626c3d648-15356650-13c680-17389ecc837c8; _lxsdk=C4064090CF0D11EA84945F632DCF0A4D8D0B8CE986ED4FA1A5DF764899054947; mojo-uuid=f5014f1d514958ccd91c2b07fb1ddc88; mojo-session-id={"id":"67b05808821b4609886449918e6ec14a","time":1596375047953}; mojo-trace-id=10; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1596377754; __mta=108886717.1595746864015.1595750256786.1596377754746.6; _lxsdk_s=173af5e1f30-5db-992-85b%7C%7C19',
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse, headers=self.header)

    def parse(self, response):
        movies = Selector(response=response).xpath('//div[@class="movie-hover-info"]')
        for movie in movies[:10]:
            item = SpidersItem()
            item['title'] = movie.xpath('./div[1]/span[1]/text()').extract_first()
            item['types'] = movie.xpath('./div[2]/text()').extract()[1].strip()
            item['date'] = movie.xpath('./div[4]/text()').extract()[1].strip()
            yield item
