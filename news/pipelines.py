import hashlib
from datetime import datetime

from elasticsearch import Elasticsearch


class ElasticsearchPipeline:
    def __init__(self, url="http://localhost:9200"):
        # elasticsearch-py 8+ requires an explicit endpoint (the implicit
        # localhost default was removed after 7.x).
        self.es = Elasticsearch(url)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            url=crawler.settings.get("ELASTICSEARCH_URL", "http://localhost:9200")
        )

    def get_id(self, item):
        url = item.get("url")
        if url:
            m = hashlib.md5()
            m.update(url.encode("utf-8"))
            return m.hexdigest()
        return None

    def process_item(self, item, spider):
        doc_id = self.get_id(item)
        item["timestamp"] = datetime.now()
        self.es.index(index="news", id=doc_id, document=dict(item))
        return item
