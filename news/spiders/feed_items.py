
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import feedparser

from news.items import FeedUrl

with open('news/test.txt') as f:
    domains = f.readlines()

URLS = ['http://{0}'.format(domain.strip()) for domain in domains if 'www'
        in domain]

WWW_URLS = ['http://www.{0}'.format(domain.strip()) for domain in domains if
        'www' not in domain]

URLS.extend(WWW_URLS)


class FeedSpider(CrawlSpider):
    name = 'feeds'
    allowed_domains = domains
    start_urls = URLS

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        #Rule(LinkExtractor(allow=('category\.php',), deny=('subsection\.php',))),
        Rule(LinkExtractor(allow=('.*xml$', '.*xml.*', '.*rss.*', '.*feed.*', '.*feeds.*'), attrs=('href', 'data-url'))),

        Rule(LinkExtractor(allow=('.*xml$', '.*xml.*', '.*rss.*', '.*feed.*', '.*feeds.*')), callback='parse_item'),
    )

    def parse_item(self, response):
        item = FeedUrl()
        item['url'] = response.url
        print response.url
        return item

        try:
            page = feedparser.parse(response.body)
            if page.bozo == 0:
                item = FeedUrl()
                item['url'] = response.url
                return item
        except:
            pass