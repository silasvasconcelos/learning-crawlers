# -*- coding: utf-8 -*-
import scrapy
from crawler.items import PostItem


class BlogScrapinghubSpider(scrapy.Spider):
    name = 'blog_scrapinghub'
    allowed_domains = ['blog.scrapinghub.com']
    start_urls = ['https://blog.scrapinghub.com/']

    def parse(self, response):
        posts = response.css(
            'div.post-listing a.more-link::attr(href)').getall()
        for post in posts:
            yield response.follow(post, self.parse_post)

        next_page = response.css('a.next-posts-link::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_post(self, response):
        yield PostItem({
            'title': response.css('div.post-page-content div.post-header h1 span::text').get(),
            'posted_at': response.css('div.post-page-content div.post-header div.byline span a::text').get(),
            'posted_by_name': response.css('div.post-page-content div.post-header div.byline span.author a::text').get(),
            'posted_by_profile_url': response.css('div.post-page-content div.post-header div.byline span.author a::attr(href)').get(),
            'body': response.css('div.post-page-content div.post-body span').get(),
        })
