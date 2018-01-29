'''settings.py'''

import os


# scrapy settings

BOT_NAME = 'pension_crawler'
SPIDER_MODULES = ['pension_crawler.spiders']


# custom settings

SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
API_KEY = os.getenv('API_KEY')
SEARCH_DEPTH = int(os.getenv('SEARCH_DEPTH', 1))