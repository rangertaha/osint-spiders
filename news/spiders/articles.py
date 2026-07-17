from datetime import datetime
from urllib.parse import urlparse

import newspaper
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from news.items import Article
from news.seeds import load_seed_lines


class ArticleSpider(CrawlSpider):
    name = "articles"

    rules = (
        # '.*xml.*', '.*xml.*', '.*rss.*', '.*feed.*', '.*feeds.*'
        Rule(
            LinkExtractor(allow=(r".*//.*/[-\w]+/.+",)),
            callback="parse_item",
        ),
        Rule(LinkExtractor(allow=(r".*",))),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        domains = load_seed_lines("news.txt")
        self.allowed_domains = domains
        urls = [f"http://{domain}" for domain in domains]
        urls.extend(f"http://www.{domain}" for domain in domains if "www" not in domain)
        self.start_urls = urls

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
