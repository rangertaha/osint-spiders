from datetime import datetime
from urllib.parse import urlparse

import newspaper
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from news.items import Article

with open("news/news.txt") as f:
    domains = f.readlines()

URLS = [f"http://{domain.strip()}" for domain in domains]

WWW_URLS = [f"http://www.{domain.strip()}" for domain in domains if "www" not in domain]

URLS.extend(WWW_URLS)


class ArticleSpider(CrawlSpider):
    name = "articles"
    allowed_domains = [domain.strip() for domain in domains]
    start_urls = URLS

    rules = (
        # '.*xml.*', '.*xml.*', '.*rss.*', '.*feed.*', '.*feeds.*'
        Rule(
            LinkExtractor(allow=(r".*//.*/[-\w]+/.+",)),
            callback="parse_item",
        ),
        Rule(LinkExtractor(allow=(r".*",))),
    )

    def parse_item(self, response):
        article = Article(timestamp=datetime.now())
        parsed_uri = urlparse(response.url)
        article["domain"] = f"{parsed_uri.scheme}://{parsed_uri.netloc}/"
        self.logger.info(response.url)

        a = newspaper.Article(url=response.url, language="en")
        a.download(input_html=response.text)
        a.parse()
        a.nlp()

        article["published"] = a.publish_date
        article["title"] = a.title
        article["description"] = a.summary
        article["url"] = a.url
        article["image"] = a.top_image
        article["authors"] = a.authors
        article["keywords"] = a.keywords
        article["length"] = len(a.text)

        title = article.get("title")
        desc = article.get("description")
        url = article.get("url")
        length = article.get("length", 0)

        if title and desc and url and length > 1500:
            yield article
