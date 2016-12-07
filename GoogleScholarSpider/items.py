# -*- coding: utf-8 -*-

from scrapy.item import Item, Field

class GooglescholarspiderItem(Item):
    name = Field()
    position = Field()
    verified = Field()
    cited = Field()
    field = Field()
    google_homepage = Field()
    university = Field()
    photo = Field()
