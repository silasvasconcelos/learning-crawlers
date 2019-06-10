# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from . import settings

from scrapy.exceptions import DropItem
from pymongo import MongoClient

class MongodbBase(object):
    mongo_uri = None
    mongo_db = None
    mongo_collection_name = 'posts'

    def __init__(self, *args, **kwargs):
        self.mongo_uri = settings.MONGO_URI
        self.mongo_db = settings.MONGO_DATABASE

    def get_collection(self, collection=None):
        return None if collection is None else self.db[collection]

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    
    def close_spider(self, spider):
        self.client.close()

class UniquePostPipeline(MongodbBase):

    def open_spider(self, spider):
        super(UniquePostPipeline, self).open_spider(spider)
        posts = self.get_collection(self.mongo_collection_name).find({}, {'url': True})
        urls = [ p.get('url') for p in posts ]
        self.__post_storageds = urls

    def process_item(self, item, spider):
        item_url = item.get('url')
        if item_url in self.__post_storageds:
            raise DropItem("Duplcate item found: %s" % item.get('title', 'Unknown'))
        else:
            self.__post_storageds.append(item_url)
            return item

class MongodbStoragePostPipeline(MongodbBase):
    
    def process_item(self, item, spider):
        self.get_collection(self.mongo_collection_name).insert_one(item)
        return item
