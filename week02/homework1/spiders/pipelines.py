# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pandas as pd


class SpidersPipeline:
    def process_item(self, item, spider):
        title = item['title']
        types = item['types']
        date = item['date']
        movie_info = [[title, types, date]]
        df = pd.DataFrame(movie_info)
        df.to_csv('./movies_maoyan.csv', mode='a', encoding='utf8', index=False, header=False)  # a is append, 可对原文件修改

        return item
