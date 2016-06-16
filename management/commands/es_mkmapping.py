# -*- coding:utf-8 -*-
"""

"""
from django.core.management.base import BaseCommand
from news.search import *


class Command(BaseCommand):
    help = 'Collect rss feeds'

    def handle(self, *args, **options):
        """Creates the mapping in elasticsearch

        :param args:
        :param options:
        :return:
        """
        pass

