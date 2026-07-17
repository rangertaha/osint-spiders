"""Tests for the item definitions in news.items."""

import pytest

from news.items import Article, Feed, FeedItem, FeedUrl

EXPECTED_FIELDS = {
    FeedUrl: {"timestamp", "url"},
    Feed: {"timestamp", "domain", "title", "description", "url", "image", "crawled"},
    FeedItem: {
        "timestamp",
        "domain",
        "title",
        "description",
        "url",
        "images",
        "authors",
    },
    Article: {
        "timestamp",
        "domain",
        "published",
        "title",
        "description",
        "url",
        "image",
        "authors",
        "keywords",
        "length",
    },
}


@pytest.mark.parametrize("item_cls", list(EXPECTED_FIELDS), ids=lambda c: c.__name__)
def test_declared_fields(item_cls):
    assert set(item_cls.fields) == EXPECTED_FIELDS[item_cls]


def test_field_assignment_roundtrip():
    item = Article(title="Hello", url="http://example.com/a")
    item["length"] = 42
    assert dict(item) == {"title": "Hello", "url": "http://example.com/a", "length": 42}


def test_unknown_field_rejected():
    item = FeedUrl()
    with pytest.raises(KeyError):
        item["not_a_field"] = "x"
