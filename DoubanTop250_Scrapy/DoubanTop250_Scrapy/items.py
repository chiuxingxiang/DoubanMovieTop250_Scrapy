# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanTop250Item(scrapy.Item):
    rank = scrapy.Field()
    score = scrapy.Field()
    title_CN = scrapy.Field()
    title_EN = scrapy.Field()
    url = scrapy.Field()
    detail = scrapy.Field()
    pass
