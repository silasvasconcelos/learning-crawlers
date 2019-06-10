# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PostItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    posted_at = scrapy.Field()
    posted_by_name = scrapy.Field()
    posted_by_profile_url = scrapy.Field()
    body = scrapy.Field()