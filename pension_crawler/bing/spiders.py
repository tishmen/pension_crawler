'''spiders.py'''

import json

from datetime import datetime
from urllib.parse import quote_plus

from scrapy import Spider, Request
from scrapy.exceptions import NotConfigured

from pension_crawler.items import ResultItemLoader
from pension_crawler.utils import SpiderMixin

from .settings import SETTINGS


class BingSpider(Spider, SpiderMixin):

    '''Parse Bing Search API results.'''

    name = 'bing'
    custom_settings = SETTINGS

    def __init__(self, crawler, keywords, api_key, depth, modifier, *args,
                 **kwargs):
        '''Set api key, search depth and keywords.'''
        super(BingSpider, self).__init__(*args, **kwargs)
        self.crawler = crawler
        self.keywords = keywords
        self.api_key = api_key
        self.depth = depth
        self.modifier = modifier

    @staticmethod
    def parse_spider_settings(settings):
        '''Parse custom spider settings.'''
        api_key = settings.get('API_KEY')
        if not api_key:
            raise NotConfigured('Google API key not set.')
        return api_key

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        '''Pass settings to constructor.'''
        input_file, depth, modifier = BingSpider.parse_settings(
            crawler.settings
        )
        api_key = BingSpider.parse_spider_settings(crawler.settings)
        keywords = BingSpider.parse_keywords(input_file)
        return cls(crawler, keywords, api_key, depth, modifier, *args, **kwargs)

    def start_requests(self):
        '''Dispatch requests per keyword.'''
        base = 'https://api.cognitive.microsoft.com/bing/v7.0/search?q={}'
        headers = {"Ocp-Apim-Subscription-Key" : self.api_key}
        for keyword in self.keywords:
            query = '{} {} filetype:pdf'.format(keyword, self.modifier)
            yield Request(base.format(quote_plus(query)), headers=headers)

    def process_item(self, node):
        '''Load single result item.'''
        loader = ResultItemLoader()
        loader.add_value('url', node['url'])
        loader.add_value('title', node['name'])
        loader.add_value('snippet', node['snippet'])
        loader.add_value('timestamp', datetime.now().isoformat())
        return loader.load_item()

    def parse(self, response):
        '''Parse search results.'''
        data = json.loads(response.body_as_unicode())
        for node in data.get('webPages', {}).get('value', []):
            item = self.process_item(node)
            item['keyword'] = data['queryContext']['originalQuery']
            item['total'] = data['webPages']['totalEstimatedMatches']
            item['file_urls'] = [item['url']]
            yield item

        # go to next results page

        if self.depth:
            start = data['rankingResponse']['mainline']['items'][-1]
            yield Request('{}&offset={}'.format(response.request.url, start))
            self.depth -= 1
