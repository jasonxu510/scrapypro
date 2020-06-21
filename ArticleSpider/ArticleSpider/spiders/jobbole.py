# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse

from ArticleSpider.ArticleSpider.items import JobBoleArticleItem

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
        post_nodes = response.css(".zhicheng_news_list a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            #new_url = response.url + post_url
            #parse.urljoin(response.url,post_url) 拼接url
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url" : image_url}, callback=self.parse_detail)
            #print(post_url)

        #提取下一页并交给scrapy进行下载
        next_url = "http://blog.jobbole.com/kaifadou/snews-getajax.php?next="
        next_page = 1
        for next_page in 10:
            yield Request(url=parse.urljoin(next_url, next_page))
            next_page = next_page+1

    def parse_detail(self, response):
        article_item = JobBoleArticleItem()
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
        front_image_url = response.meta.get["front_image_url", ""]
        title = response.css(".ship_wrap h2::text").extract()[0]
        create_date = response.css(".meta span::text").extract()[0]
        content = response.css(".wen_article p::text").extract()
        content = "".join(content)
        #print(re_selector)

        article_item["title"] = title
        article_item["create_date"] = create_date
        article_item["url"] = response.url
        article_item["front_image_url"] = front_image_url
        article_item["content"] = content

        yield article_item
