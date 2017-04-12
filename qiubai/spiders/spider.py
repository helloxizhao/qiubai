#!/usr/bin/env python
#coding=utf-8
from lxml import etree
from qiubai.items import QiubaiItem
import  scrapy
class qiubai(scrapy.Spider):
    name = 'qiubai'
    start_urls = ['http://www.qiushibaike.com/',]
    def parse(self, response):
        content_list = response.xpath('//div[@class="content"]')
        for list  in content_list:
            item = QiubaiItem()
            item['content'] = list.xpath('span/text()').extract()[0]
            yield item

