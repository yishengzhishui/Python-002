# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pandas as pd
import pymysql


class SpidersPipeline:
    # def process_item(self, item, spider):
    #     title = item['title']
    #     types = item['types']
    #     date = item['date']
    #     movie_info = [[title, types, date]]
    #     df = pd.DataFrame(movie_info)
    #     df.to_csv('./movies_maoyan.csv', mode='a', encoding='utf8', index=False, header=False)  # a is append, 可对原文件修改
    #
    #     return item

    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DATABASE')
        host = spider.settings.get('MYSQL_HOST')
        port = spider.settings.get('MYSQL_PORT')
        user = spider.settings.get('MYSQL_USER')
        password = spider.settings.get('MYSQL_PASSWORD')

        self.db_conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password, charset='utf8mb4')
        self.db_cur = self.db_conn.cursor()

    # # 关闭数据库
    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    # # 对数据进行处理
    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    # #插入数据
    def insert_db(self, item):
        values = (
            item['title'],
            item['types'],
            item['date'],
        )
        # con
        sql = "INSERT INTO Movies (Title, Types, Date) VALUES (%s, %s, %s)"

        self.db_cur.execute(sql, values)
