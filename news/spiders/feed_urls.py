# -*- coding: utf-8 -*-
"""


"""
import time
import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import feedparser
import newspaper

from news.items import FeedUrl







with open('news/news.txt') as f:
    domains = f.readlines()

URLS = ['http://{0}'.format(domain.strip()) for domain in domains if 'www'
        in domain]

WWW_URLS = ['http://www.{0}'.format(domain.strip()) for domain in domains if
        'www' not in domain]

URLS.extend(WWW_URLS)


class NewsFeedSpider(CrawlSpider):
    name = 'urls'
    allowed_domains = [domain.strip() for domain in domains]
    start_urls = URLS
    content_types = ['text/xml', 'application/xml', 'rss', 'xml']

    rules = (
        Rule(LxmlLinkExtractor(
            allow=('.*\.xml$', '.*\.atom$', '.*\.rss$', '.*\.feed$', '.*\.feeds$'),
        ), callback='parse_item'),

        Rule(LxmlLinkExtractor(
            allow=('.*xml.*', '.*xml.*', '.*rss.*', '.*feed.*', '.*feeds.*'),
        ), callback='parse_item', follow=True),

        Rule(LxmlLinkExtractor(
            allow=('.*', ),
        )),
    )

    def parse_item(self, response):
        cts = response.headers.get('Content-Type')
        for ct in self.content_types:
            if ct in cts:
                print response.url
                url = FeedUrl()
                url['url'] = response.url
                yield url

