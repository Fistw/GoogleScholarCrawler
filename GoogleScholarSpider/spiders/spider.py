# -*- coding: utf-8 -*- #

import scrapy
import re
import string
from scrapy.spiders import CrawlSpider, Rule  
from scrapy.linkextractors import LinkExtractor  
from scrapy.selector import Selector
from scrapy.http import Request
from GoogleScholarSpider.items import GooglescholarspiderItem 
from GoogleScholarSpider.start_urls import getStart_urls

class GoogleScholar(CrawlSpider):
	name = "GoogleScholarSpider"
	allowed_domains = ['google.com']

	start_urls = getStart_urls()
	# start_urls = [
	# 	'https://scholar.google.com/citations?view_op=view_org&hl=en&org=1896398670060433590&after_author=GcmGAP3___8J&astart=5650',
	# 	'https://scholar.google.com/citations?view_op=view_org&hl=en&org=2173967239881328522',
	# ]

	def parse(self, response):
		self.log('Hi, this is an item page! %s' % response.url)

		item = GooglescholarspiderItem()
		sel = Selector(response)

		person = sel.xpath('//*[@id="gsc_ccl"]/div[1<position() and position()<12]')
		
		for each in person:
			name = each.xpath('div[@class = "gsc_1usr_text"]/h3/a/text()')
			if name:
				item['name'] = name.extract()[0]
			else:
				return 
			item['photo'] = 'https://scholar.google.com' + each.xpath('div[@class="gsc_1usr_photo"]/a/img/@src').extract()[0]
			item['position'] = each.xpath('div[@class = "gsc_1usr_text"]/div[@class="gsc_1usr_aff"]/text()').extract()[0]
			item['verified'] = each.xpath('div[@class = "gsc_1usr_text"]/div[@class="gsc_1usr_eml"]/text()').extract()[0]
			cited= each.xpath('div[@class = "gsc_1usr_text"]/div[@class = "gsc_1usr_cby"]/text()')
			if cited :
				item['cited'] = cited.re('Cited by (.*)')[0]
			else:
				item['cited'] = 0
			item['field'] = each.xpath('div[@class = "gsc_1usr_text"]/div[@class="gsc_1usr_int"]/a/text()').extract()
			item['google_homepage'] = 'https://scholar.google.com' + each.xpath('div[@class = "gsc_1usr_text"]/h3/a/@href').extract()[0]
			item['university'] = each.xpath('//*[@id="gsc_ccl"]/h2/text()').re('(.*)\s')[0]
			yield item

		stra = sel.xpath('//*[@id="gsc_authors_bottom_pag"]/span/button[2]/@onclick').re('after_author\\\\x3d(.*?)\\\\x26astart')[0]
		strb = sel.xpath('//*[@id="gsc_authors_bottom_pag"]/span/button[2]/@onclick').re('\\\\x26astart\\\\x3d(.*?)\'')[0]

		response_url = re.findall('(.*?)&after_author=', response.url)
		if response_url:
			res = response_url[0]
		else:
			res = response.url
		next_link = res + '&after_author=' + stra + '&astart=' + strb
		yield Request(next_link, callback = self.parse)