# -*- coding: utf-8 -*-
import scrapy


class Feed(scrapy.Item):
    domain = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    crawled = 'DateTime'


class FeedItem(scrapy.Item):
    domain = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    images = scrapy.Field()
    authors = scrapy.Field()
