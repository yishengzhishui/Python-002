看视频

第一遍跟着老师的思路走，理解代码逻辑；

第二遍边写作业边看，理解代码细节

- 创建项目 `scrapy startproject spiders`
- `cd spiders/spiders` 需要再进入下一层目录，进入刚创建的项目文件里爬虫项目文件
- 创建爬虫 `scrapy gensipder movies maoyan.com`
- items 设置对应要爬取的内容 `name = scrapy.Field()` scrapy.Field 只返回一个值，使用管道 piplines，需在 setting 开启`item_pipeline`
- 运行爬虫命令 `scrapy crawl movies`




别的人遇到但是我没碰到的问题，先记录一下：

##### scrapy 反爬

1、`settings.py` 中 添加 `COOKIES_ENABLED = True`

2、添加到爬虫文件中

```python
# movies.py

from http.cookies import SimpleCookie
cookies_fromchrome = '贴进去从 chrome 复制的 cookie'

cookie = SimpleCookie(cookies_fromchrome)
cookies = {i.key:i.value for i in cookie.values()}

# 将cookies添加到 scrapy.Request中
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],callback=self.parse,dont_filter=False,cookies=self.cookies)
```

