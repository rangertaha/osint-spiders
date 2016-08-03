import time
from datetime import datetime
import scrapy
from scrapy.spiders import CrawlSpider, Rule, BaseSpider, Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import feedparser
import newspaper
from news.items import Article

from urlparse import urlparse





with open('news/news.txt') as f:
    domains = f.readlines()

URLS = ['http://{0}'.format(domain.strip()) for domain in domains]

WWW_URLS = ['http://www.{0}'.format(domain.strip()) for domain in domains if
        'www' not in domain]

URLS.extend(WWW_URLS)


class ArticleSpider(CrawlSpider):
    name = 'articles'
    allowed_domains = domains
    start_urls = URLS

    rules = (
        # '.*xml.*', '.*xml.*', '.*rss.*', '.*feed.*', '.*feeds.*'
        Rule(LxmlLinkExtractor(
             allow=('.*//.*/[-\w]+/.+', ),
        ), callback='parse_item'),

        Rule(LxmlLinkExtractor(
            allow=('.*',),
        )),
    )

    def parse_item(self, response):
        article = Article(timestamp=datetime.now())
        parsed_uri = urlparse(response.url)
        article['domain'] = '{uri.scheme}://{uri.netloc}/'.format(
            uri=parsed_uri)
        print response.url

        a = newspaper.Article(url=response.url, language='en')
        a.html = response.body
        a.build()

        article['published'] = a.publish_date
        article['title'] = a.title
        article['description'] = a.summary
        article['url'] = a.url
        article['image'] = a.top_image
        article['authors'] = a.authors
        article['keywords'] = a.keywords
        article['length'] = len(a.text)

        title = article.get('title', None)
        desc = article.get('description', None)
        url = article.get('url', None)
        length = article.get('length', 0)

        if title and desc and url and length > 1500:
            yield article
        



