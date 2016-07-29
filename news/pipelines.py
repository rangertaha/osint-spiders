# -*- coding: utf-8 -*-
import json


class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        print line
        self.file.write(line)
        return item
