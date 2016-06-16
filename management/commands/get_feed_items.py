# -*- coding:utf-8 -*-
"""

"""
import json
import hashlib
import logging
from datetime import datetime

import requests
import tempfile
from newspaper import Article
from dateutil import parser as tparser
from django.template.loader import get_template
from django.core.management.base import BaseCommand
from django.core import files
import newspaper
import feedparser
from bs4 import BeautifulSoup


from news.models import NewsSite, Feed, FeedItem, Photo


# Get an instance of a logger
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Collect rss feeds'

    def handle(self, *args, **options):
        for feed in Feed.objects.all():
            parse = feedparser.parse(feed.link)
            entries = self.get_feed_entries(parse)


    def get_feed_entries(self, parsed):
        num = len(parsed.entries)
        entries = []
        if num > 0:
            for entry in parsed.entries:
                title = getattr(entry, 'title', None)
                link = getattr(entry, 'link', None)
                description = getattr(entry, 'description', None)
                if not description:
                    description = getattr(entry, 'summary', None)

                if title and link and description:
                    description = BeautifulSoup(description).get_text()
                    item, created = FeedItem.objects.get_or_create(
                        title=title, link=link, description=description)

                    pubdate = getattr(entry, 'published', None)
                    if pubdate:
                        item.pubdate = tparser.parse(pubdate, ignoretz=True)

                    udate = getattr(entry, 'updated', None)
                    if udate:
                        item.updated = tparser.parse(udate, ignoretz=True)
                    item.save()
                    entries.append(item)
        return entries

