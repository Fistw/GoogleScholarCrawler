# -*- coding: utf-8 -*-

import os
import codecs
import json
from scrapy.exceptions import DropItem

class GooglescholarspiderPipeline(object):
    def __init__(self):
        self.file = codecs.open('PersonInfo.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close()

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['google_homepage'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['google_homepage'])
            return item