"""Offline tests for the spider parse methods using synthetic responses."""

from datetime import datetime

from scrapy.http import HtmlResponse, TextResponse, XmlResponse

from news.items import Article, FeedUrl
from news.spiders.articles import ArticleSpider
from news.spiders.feed_item import FeedItemSpider
from news.spiders.feed_urls import FeedUrlSpider
from news.spiders.news_sites import NewsSiteSpider

RSS_BODY = b"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Example News</title>
    <link>http://news.example.com/</link>
    <description>Synthetic feed for tests</description>
    <item>
      <title>First story</title>
      <link>http://news.example.com/first</link>
      <description>Story body</description>
    </item>
  </channel>
</rss>
"""


class FakeNewspaperArticle:
    """Stand-in for newspaper.Article: no network, no NLP models."""

    text = "word " * 400  # > 1500 characters

    def __init__(self, url, language="en"):
        self.url = url
        self.publish_date = datetime(2026, 1, 1)
        self.title = "Synthetic headline"
        self.summary = "Synthetic summary"
        self.top_image = "http://news.example.com/img.png"
        self.authors = ["A. Reporter"]
        self.keywords = ["news"]

    def download(self, input_html=None):
        self.html = input_html

    def parse(self):
        pass

    def nlp(self):
        pass


class TestArticleSpider:
    def make_response(self, url="http://news.example.com/world/story.html"):
        return HtmlResponse(
            url=url,
            body=b"<html><body><p>hello</p></body></html>",
            encoding="utf-8",
        )

    def test_parse_item_yields_article(self, monkeypatch):
        monkeypatch.setattr(
            "news.spiders.articles.newspaper.Article", FakeNewspaperArticle
        )
        spider = ArticleSpider()
        items = list(spider.parse_item(self.make_response()))
        assert len(items) == 1
        article = items[0]
        assert isinstance(article, Article)
        assert article["domain"] == "http://news.example.com/"
        assert article["title"] == "Synthetic headline"
        assert article["description"] == "Synthetic summary"
        assert article["url"] == "http://news.example.com/world/story.html"
        assert article["authors"] == ["A. Reporter"]
        assert article["length"] > 1500

    def test_parse_item_drops_short_articles(self, monkeypatch):
        class ShortArticle(FakeNewspaperArticle):
            text = "too short"

        monkeypatch.setattr("news.spiders.articles.newspaper.Article", ShortArticle)
        spider = ArticleSpider()
        assert list(spider.parse_item(self.make_response())) == []

    def test_parse_item_drops_untitled_articles(self, monkeypatch):
        class UntitledArticle(FakeNewspaperArticle):
            def parse(self):
                self.title = ""

        monkeypatch.setattr("news.spiders.articles.newspaper.Article", UntitledArticle)
        spider = ArticleSpider()
        assert list(spider.parse_item(self.make_response())) == []

    def test_start_urls_built_from_data_file(self):
        spider = ArticleSpider()
        assert spider.start_urls
        assert all(url.startswith("http://") for url in spider.start_urls)
        assert spider.allowed_domains


class TestFeedItemSpider:
    def test_parse_valid_feed_returns_item(self):
        response = XmlResponse(url="http://news.example.com/rss.xml", body=RSS_BODY)
        item = FeedItemSpider().parse(response)
        assert isinstance(item, FeedUrl)
        assert item["url"] == "http://news.example.com/rss.xml"

    def test_parse_invalid_feed_returns_none(self):
        # Malformed XML makes feedparser set bozo, so the spider drops it.
        response = TextResponse(
            url="http://news.example.com/broken.xml",
            body=b'<?xml version="1.0"?><rss><channel><unclosed></rss>',
            encoding="utf-8",
        )
        assert FeedItemSpider().parse(response) is None


class TestFeedUrlSpider:
    def make_response(self, content_type):
        return TextResponse(
            url="http://news.example.com/rss.xml",
            body=RSS_BODY,
            headers={"Content-Type": content_type},
        )

    def test_parse_item_yields_url_for_xml_content(self):
        spider = FeedUrlSpider()
        items = list(spider.parse_item(self.make_response("application/xml")))
        assert len(items) == 1
        assert isinstance(items[0], FeedUrl)
        assert items[0]["url"] == "http://news.example.com/rss.xml"

    def test_parse_item_ignores_html_content(self):
        spider = FeedUrlSpider()
        assert list(spider.parse_item(self.make_response("text/html"))) == []


class TestNewsSiteSpider:
    def test_parse_item_returns_feed_url(self):
        response = HtmlResponse(
            url="http://news.example.com/feeds/index.rss",
            body=b"<html></html>",
            encoding="utf-8",
        )
        item = NewsSiteSpider().parse_item(response)
        assert isinstance(item, FeedUrl)
        assert item["url"] == "http://news.example.com/feeds/index.rss"
