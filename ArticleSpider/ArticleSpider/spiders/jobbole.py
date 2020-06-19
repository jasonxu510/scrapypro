# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com']
    #start_urls = ['http://blog.jobbole.com/licai/zq/164942.html']

    def parse(self, response):
        """
        1、获取文章列表页中的文章url并交给scrapy，下载后并进行解析
        2、获取下一页的url并交给scrapy进行下载，下载完成后交给parse

        """
        #解析列表页中的所有文章url并交给scrapy下载后并进行解析
        post_urls = response.css(".zhicheng_news_list a::attr(href)").extract()
        for post_url in post_urls:
            #new_url = response.url + post_url
            #parse.urljoin(response.url,post_url) 拼接url
            yield Request(url=parse.urljoin(response.url,post_url), callback=self.parse_detail)
            #print(post_url)

        #提取下一页并交给scrapy进行下载
        #next_url =

    def parse_detail(self, response):
        #提取文章的具体字段
        #xpath语法
        # title = response.xpath('/html/body/div[3]/div[2]/div[1]/h2[1]/text()').extract()[0]
        # creatdate = response.xpath('/html/body/div[3]/div[2]/div[1]/div[1]/span[1]/text()').extract()[0]
        # #方法一：
        # content = response.xpath("//div[@class='wen_article']").extract_first("")
        # content = re.findall(r">(.*?)<", content)
        # content = ''.join(content)
        # #方法二：
        # #content = response.xpath("//div[@class='wen_article']/p/text()").extract()
        # #content = ''.join(content)
        # #方法三：
        # #content = response.xpath("//div[@class='wen_article']").extract().replace("<p>", "").replace("</p>", "")

        #css选择器语法
        title = response.css(".ship_wrap h2::text").extract()[0]
        createDate = response.css(".meta span::text").extract()[0]
        content = response.css(".wen_article p::text").extract()
        content = "".join(content)
        #print(re_selector)
        pass
