# -*- coding: utf-8 -*-
import scrapy


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/licai/zq/164942.html']

    def parse(self, response):
        re_selector = response.xpath('/html/body/div[3]/div[2]/div[1]/h2[1]/text()')
        re2_selector = response.xpath('/html/body/div[3]/div[2]/div[1]/div[1]/span[1]/text()')
        #print(re_selector)
        pass
