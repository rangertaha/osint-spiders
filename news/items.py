# -*- coding: utf-8 -*-
import scrapy


class FeedUrl(scrapy.Item):
    url = scrapy.Item()


class Feed(scrapy.Item):
    timestamp = scrapy.Field()
    domain = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    crawled = 'DateTime'


class FeedItem(scrapy.Item):
    timestamp = scrapy.Field()
    domain = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    images = scrapy.Field()
    authors = scrapy.Field()


class Article(scrapy.Item):
    timestamp = scrapy.Field()
    domain = scrapy.Field()
    published = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    authors = scrapy.Field()
    keywords = scrapy.Field()
    length = scrapy.Field()
