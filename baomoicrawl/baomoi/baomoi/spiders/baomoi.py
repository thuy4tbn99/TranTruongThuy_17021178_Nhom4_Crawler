import re
import scrapy
import os

from .baomoi_collect import baomoiCollectSpider

class baomoiSpider(scrapy.Spider):

    name = 'baomoi'
    start_urls = [
        'https://www.baomoi.com/tin-moi/xa-hoi.epi',
        'https://www.baomoi.com/tin-moi/the-gioi.epi',
        'https://www.baomoi.com/tin-moi/van-hoa.epi',
        'https://www.baomoi.com/tin-moi/kinh-te.epi',
        'https://www.baomoi.com/tin-moi/giao-duc.epi',
        'https://www.baomoi.com/tin-moi/the-thao.epi',
        'https://www.baomoi.com/tin-moi/giai-tri.epi',
        'https://www.baomoi.com/tin-moi/phap-luat.epi',
        'https://www.baomoi.com/tin-moi/khoa-hoc.epi',
        'https://www.baomoi.com/tin-moi/khoa-hoc-cong-nghe.epi',
        'https://www.baomoi.com/tin-moi/doi-song.epi',
        'https://www.baomoi.com/tin-moi/xe-co.epi',
        'https://www.baomoi.com/tin-moi/nha-dat.epi',
    ]
    collect_parser = baomoiCollectSpider()

    def parse(self, response):
        collect_pages = response.css('h4.story__heading a::attr(href)').getall()
        for next_page in collect_pages:
            id = re.compile(".*/(\d+).epi").match(next_page).groups()[0]
            # print(id)
            url = 'http://www.baomoi.com/a/c/' + id + '.epi'
            yield scrapy.Request(url, callback=self.collect_parser.parse)

        next_page = response.css('div.pagination__controls a::attr(href)').getall()[1]
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
