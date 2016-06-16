
import scrapy

from news.items import *


class FeedSpider( scrapy.Spider ):
    name = 'feeds'

    def start_requests( self ):
        while( True ):
            yield self.make_requests_from_url(
                self._pop_queue()
            )

    def _pop_queue( self ):
        while( True ):
            yield self.queue.read()
