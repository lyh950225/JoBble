# -*- coding: utf-8 -*-
import scrapy
from JoBble.items import ArticleItemLoader, JobbleItem
from JoBble.utils.common import get_ma5
from scrapy.http import Request
from urllib.parse import urljoin

class JobblearticleSpider(scrapy.Spider):
    name = 'JoBbleArticle'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            image_url = post_node.css('img::attr(src)').extract_first("")
            post_url = post_node.css('::attr(href)').extract_first("")
            yield Request(url=urljoin(response.url, post_url),meta={"front_image_url": image_url}, callback=self.parse_detail)
        next_urls = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_urls:
            yield Request(url=urljoin(response.url, next_urls), callback=self.parse)



    def parse_detail(self, response):
        # 文章详情页进行解析，提取字段
        front_image_url = response.meta.get('front_image_url')
        item_loader = ArticleItemLoader(item=JobbleItem(), response=response)
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_ma5(response.url))
        item_loader.add_css('title', '.entry-header h1::text')
        item_loader.add_css('creat_time', '.entry-meta-hide-on-mobile::text')
        item_loader.add_css('praise_nums', '.post-adds h10::text')
        item_loader.add_value('front_image_url', [front_image_url])
        item_loader.add_css('faves_nums', '.post-adds span:nth-child(2)::text')
        item_loader.add_css('comment_nums', '.post-adds a[href="#article-comment"] span::text')
        item_loader.add_css('tag_list', '.entry-meta-hide-on-mobile a::text')
        item_loader.add_css('contens', 'div.entry')

        article_item = item_loader.load_item()
        return article_item

