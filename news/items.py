# -*- coding: utf-8 -*-
import scrapy


class FeedUrl(scrapy.Item):
    url = scrapy.Field()


class NewsSite(scrapy.Item):
    country = scrapy.Field()
    domain = scrapy.Field()
    favicon = scrapy.Field()


class Feed(scrapy.Item):
    site = NewsSite()
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()


class FeedItem(scrapy.Item):
    site = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    authors = scrapy.Field()
