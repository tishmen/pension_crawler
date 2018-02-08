'''settings.py'''

import os


# Scrapy settings

BOT_NAME = 'pension_crawler'
SPIDER_MODULES = ['pension_crawler.google', 'pension_crawler.bing']

LOG_LEVEL = 'INFO'
COOKIES_ENABLED = False
RETRY_ENABLED = False
DOWNLOAD_TIMEOUT = 90
DOWNLOAD_DELAY = 0.5

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 604800

DOWNLOADER_MIDDLEWARES = {
    'pension_crawler.middlewares.RequestBlacklistMiddleware': 400
}
ITEM_PIPELINES = {
    'scrapy.pipelines.files.FilesPipeline': 1,
    'pension_crawler.pipelines.ResultItemCSVExportPipeline': 900
}
FIELDS_TO_EXPORT = ['keyword', 'url', 'title', 'path']

# Custom settings

DATA_DIR = os.path.join(os.getcwd(), 'data')
INPUT_FILE = os.path.join(DATA_DIR, 'input.csv')
BLACKLIST_FILE = os.path.join(DATA_DIR, 'blacklist.csv')

RESULT_DEPTH = 0
