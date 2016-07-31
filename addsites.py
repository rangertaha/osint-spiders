#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pika
from news import settings

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()

channel.basic_publish(exchange='',
                      routing_key=settings.RABBITMQ_QUEUE_NAME,
                      body='</html>raw html contents<a href="http://twitter.com/roycehaynes">extract url</a></html>')

connection.close()


