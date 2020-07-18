# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class Music163ComPipeline:
    # 打开数据库
    def open_spider(self, spider):
        db_uri = spider.settings.get("MONGODB_URI", "mongodb://localhost:27017")
        db_name = spider.settings.get("MONGODB_DB_NAME", "music163com")

        self.db_client = MongoClient(db_uri)
        self.db = self.db_client[db_name]

    # 关闭数据库
    def close_spider(self, spider):
        self.db_client.close()

    # 对数据进行处理
    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    # 插入数据
    def insert_db(self, item):
        self.db[item.pop("playlist_title")].insert_one(dict(item))
