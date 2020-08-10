import scrapy
import re
import json
import os

class baomoiCollectSpider(scrapy.Spider):

    name = 'baomoi_collect'
    start_urls = [
        'https://baomoi.com/a/c/33871156.epi',
    ]

    def parse(self, response):

        # URL
        # self.logger.info('===> %s', response.url)
        url = response.url
        # print(url)

        #ID
        id = re.compile(".*/(\d+).epi").match(url).groups()[0]
        # print(id)

        # header
        header = response.css('h1.article__header::text').get()

        # datetime
        datetime = response.xpath('//time[@class="time"]/@datetime').get()

        # summary
        summary = response.css('div.article__sapo::text').get()

        # content
        content = ''
        body = response.css('div.article__body')
        for text in body:
            text_content = text.css('p.body-text::text').getall()
            if type(text_content) == list:
                text_content = u''.join(text_content)
            content += text_content + ' '

        # topic
        topic = response.css('a.cate::text').get()

        # tag
        tag = response.css('div.article__tag a.keyword::text').getall()
        for i in range(0, len(tag)):
            tag[i] = tag[i].strip()

        # link
        link = response.css('p.bm-source a::attr(href)').get()
        # Save page
        dirpath = os.path.dirname(__file__)
        save_file = './baomoi/spiders/data/' + id + '.json'
        if (os.path.isfile(save_file) == False) and (header != None):
            # print('Not found')
            data = {
                'id': id,
                'header': header,
                'datetime': datetime,
                'summary': summary,
                'content': content,
                'topic': topic,
                'tag': tag,
                'link': link,
            }
            with open(save_file, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False)

            yield {
                'id': id,
                'header': header,
                'datetime': datetime,
                'summary': summary,
                'content': content,
                'topic': topic,
                'tag': tag,
                'link': link,
            }