"""Sanity checks for the Scrapy project settings."""

from news import settings


def test_bot_name():
    assert settings.BOT_NAME == "news"


def test_spider_modules():
    assert settings.SPIDER_MODULES == ["news.spiders"]
    assert settings.NEWSPIDER_MODULE == "news.spiders"


def test_elasticsearch_pipeline_enabled():
    assert settings.ITEM_PIPELINES == {"news.pipelines.ElasticsearchPipeline": 300}


def test_elasticsearch_url():
    assert settings.ELASTICSEARCH_URL == "http://localhost:9200"


def test_rabbitmq_queue_name():
    # Used by addsites.py; must exist and be a non-empty string.
    assert isinstance(settings.RABBITMQ_QUEUE_NAME, str)
    assert settings.RABBITMQ_QUEUE_NAME


def test_scrapy_redis_scheduler_configured():
    assert settings.SCHEDULER == "scrapy_redis.scheduler.Scheduler"
    assert settings.DUPEFILTER_CLASS == "scrapy_redis.dupefilter.RFPDupeFilter"


def test_settings_load_through_scrapy():
    """The settings module must be loadable by Scrapy itself."""
    from scrapy.settings import Settings

    s = Settings()
    s.setmodule("news.settings", priority="project")
    assert s.get("ELASTICSEARCH_URL") == "http://localhost:9200"
    assert s.get("RABBITMQ_QUEUE_NAME") == settings.RABBITMQ_QUEUE_NAME
