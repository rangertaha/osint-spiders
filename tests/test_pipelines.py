"""Tests for ElasticsearchPipeline with a fully mocked Elasticsearch client."""

import hashlib
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from scrapy.settings import Settings

import news.pipelines
from news.items import Article
from news.pipelines import ElasticsearchPipeline


@pytest.fixture
def es_client_cls(monkeypatch):
    """Replace the Elasticsearch class in the pipeline module with a mock."""
    mock_cls = MagicMock(name="Elasticsearch")
    monkeypatch.setattr(news.pipelines, "Elasticsearch", mock_cls)
    return mock_cls


def make_crawler(settings_dict):
    return SimpleNamespace(settings=Settings(settings_dict))


def test_from_crawler_uses_elasticsearch_url(es_client_cls):
    crawler = make_crawler({"ELASTICSEARCH_URL": "http://es.example:9200"})
    pipeline = ElasticsearchPipeline.from_crawler(crawler)
    es_client_cls.assert_called_once_with("http://es.example:9200")
    assert pipeline.es is es_client_cls.return_value


def test_from_crawler_defaults_to_localhost(es_client_cls):
    pipeline = ElasticsearchPipeline.from_crawler(make_crawler({}))
    es_client_cls.assert_called_once_with("http://localhost:9200")
    assert pipeline.es is es_client_cls.return_value


def test_get_id_is_md5_of_url(es_client_cls):
    pipeline = ElasticsearchPipeline()
    url = "http://example.com/article"
    expected = hashlib.md5(url.encode("utf-8")).hexdigest()
    assert pipeline.get_id(Article(url=url)) == expected


def test_get_id_without_url_is_none(es_client_cls):
    pipeline = ElasticsearchPipeline()
    assert pipeline.get_id(Article(title="no url")) is None


def test_process_item_indexes_document(es_client_cls):
    pipeline = ElasticsearchPipeline()
    item = Article(url="http://example.com/article", title="Title")

    result = pipeline.process_item(item, spider=None)

    assert result is item
    assert "timestamp" in item  # stamped by the pipeline
    mock_es = es_client_cls.return_value
    mock_es.index.assert_called_once()
    kwargs = mock_es.index.call_args.kwargs
    assert kwargs["index"] == "news"
    assert kwargs["id"] == pipeline.get_id(item)
    assert kwargs["document"]["url"] == "http://example.com/article"
    assert kwargs["document"]["title"] == "Title"
