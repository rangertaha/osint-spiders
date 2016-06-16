# -*- coding:utf-8 -*-
"""

"""
import os

from django.core.management.base import BaseCommand
from news.models import NewsSite

SITES_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sites.txt')


class Command(BaseCommand):
    help = 'Collect rss feeds'

    def handle(self, *args, **options):
        with open(SITES_FILE) as f:
            sites = f.readlines()
            for site in sites:
                site = site.strip()
                obj, created = NewsSite.objects.get_or_create(domain=site)
                if created:
                    print site
