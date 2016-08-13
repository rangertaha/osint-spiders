# -*- coding: utf-8 -*-
"""


"""
import time
import scrapy
from scrapy.spiders import CrawlSpider, Rule
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
        ), callback='parse_item'),

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

        #page = feedparser.parse(response.body)

        '''
        item = FeedUrl()
        item['url'] = response.url
        print response.url
        return item
        '''








"""



        try:
            page = feedparser.parse(response.body)
            if page.bozo == 0:
                item = FeedUrl()
                item['url'] = response.url
                return item
        except:
            pass





        class ProfileSpider(scrapy.Spider):
            name = 'myspider'

            def start_requests(self):
                while (True):
                    yield self.make_requests_from_url(
                        self._pop_queue()
                    )

            def _pop_queue(self):
                while (True):
                    yield self.queue.read()





import nsq
import tornado.ioloop
import time

def pub_message():
    writer.pub('test', time.strftime('%H:%M:%S'), finish_pub)

def finish_pub(conn, data):
    print data

writer = nsq.Writer(['127.0.0.1:4150'])
tornado.ioloop.PeriodicCallback(pub_message, 1000).start()
nsq.run()







"""
