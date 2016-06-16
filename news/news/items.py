# -*- coding: utf-8 -*-
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, String, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, GeoPoint, FacetedSearch

import scrapy

# Setup the connection
connections.create_connection(hosts=settings.ES_DATABASE)




class FeedItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()







# Define analyzers
html_strip = analyzer('html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


class NewsMapping(DocType):
    site = String(fields={'raw': String(index='analyzed')})
    title = String(fields={'raw': String(index='analyzed')})
    description = String(analyzer=html_strip,
                         fields={'raw': String(index='analyzed')})
    # URL of the article
    url = String(fields={'raw': String(index='not_analyzed')})
    authors = String(fields={'raw': String(index='analyzed')})
    published = Date()
    updated = Date()
    location = GeoPoint()

    # For extra data that is related to this search object
    extra = String(fields={'raw': String(index='analyzed')})

    # These objects should not be used by elasticsearch
    image = String(fields={'raw': String(index='no')})
    link = String(fields={'raw': String(index='no')})

    class Meta:
        index = 'news'

    def get_model_attrs(self, model, fields):
        for k, v in fields.iteritems():
            if hasattr(self, k):
                if hasattr(model, v):
                    value = getattr(model, v, None)
                    if value is not None:
                        setattr(self, k, value)

