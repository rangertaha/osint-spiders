# -*- coding: utf-8 -*-
import hashlib
from datetime import datetime

from elasticsearch import Elasticsearch


class ElasticsearchPipeline(object):

    def __init__(self):
        self.es = Elasticsearch()

    def get_id(self, item):
        m = hashlib.md5()
        url = item.get('url', None)
        if url:
            m.update(url)
            return m.hexdigest()

    def process_item(self, item, spider):
        id = self.get_id(item)
        item['timestamp'] = datetime.now()
        self.es.index(index="news", doc_type="article", id=id, body=dict(item))
        return item
