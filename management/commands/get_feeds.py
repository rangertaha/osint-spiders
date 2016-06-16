# -*- coding:utf-8 -*-
"""

"""
import sys
import json
import hashlib
import logging
from datetime import datetime



from django.db.models import Q
from dateutil import parser as tparser
from django.template.loader import get_template
from django.core.management.base import BaseCommand
import newspaper
import feedparser

from news.models import NewsSite, Feed


# Get an instance of a logger
#logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Crawl news sites for rss feeds'
    site = ''

    def handle(self, *args, **options):
        for url, site in self.feeds_urls():
            try:
                self.get_feed(url, site)
            except:
                pass
                #logger.error('Unable to crawl site: {0}'.format(site))

    def feeds_urls(self):

        for site in NewsSite.objects.all():
            urls = self.crawl_feed_urls('http://{0}'.format(site.domain))
            for url in urls:
                yield url, site
        '''
        urls = self.crawl_feed_urls('http://{0}'.format(self.site[0]))
        for url in urls:
            yield url, self.site[0]

        '''

    def crawl_feed_urls(self, url):
        try:
            #paper = newspaper.build(url, memoize_articles=False)
            paper = newspaper.build(url, memoize_articles=False)
            feeds = paper.feed_urls()
        except:
            pass
            #logger.error('Unable to build newspaper form the domain: {0}'.format(self.domain))
        else:
            for feed in feeds:
                yield feed
            del(paper)
            del(feeds)

    def get_feed(self, url, site):
        parse = feedparser.parse(url)

        title = getattr(parse.feed, 'title', None)
        link = getattr(parse.feed, 'link', None)
        description = getattr(parse.feed, 'description', None)
        if link and title and description:
            if len(parse.entries) > 1:
                feed, created = Feed.objects.get_or_create(
                    link=url, title=title, description=description)
                site.feeds.add(feed)
                site.save()
                print len(parse.entries), url
                del(site)
                del(feed)
                del(parse)

