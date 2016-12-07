# -*- coding: utf-8 -*- #

import json

def getStart_urls():
	start_urls = []
	f = open('University.json', 'r')
	for each_line in f:
		js = json.loads(each_line)
		start_urls.append(js['url'])
	return start_urls

