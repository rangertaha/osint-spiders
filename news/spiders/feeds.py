
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import feedparser

from news.items import FeedUrl

with open('test.txt') as f:
    domains = f.readlines()

URLS = ['http://{0}'.format(domain.strip()) for domain in domains if 'www'
        in domain]

WWW_URLS = ['http://www.{0}'.format(domain.strip()) for domain in domains if
        'www' not in domain]

URLS.extend(WWW_URLS)


class FeedSpider(CrawlSpider):
    name = 'feeds'
    start_urls = URLS

    rules = (
        Rule(LinkExtractor(allow=('.*', )), callback='parse_item'),
    )

    def parse_item(self, response):
        try:
            page = feedparser.parse(response.body)
            if page.bozo == 0:
                item = FeedUrl()
                item['url'] = response.url
                return item
        except:
            pass