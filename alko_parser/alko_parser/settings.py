BOT_NAME = "alko_parser"

SPIDER_MODULES = ["alko_parser.spiders"]
NEWSPIDER_MODULE = "alko_parser.spiders"

ADDONS = {}
ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 200
CONCURRENT_REQUESTS_PER_DOMAIN = 200
CONCURRENT_REQUESTS_PER_IP = 200

DOWNLOAD_DELAY = 0.5
RANDOMIZE_DELAY = True

DEFAULT_REQUEST_HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
    "Priority": "u=1, i",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"
}

DOWNLOADER_MIDDLEWARES = {
   "scrapy.downloadermiddlewares.retry.RetryMiddleware": 90,
   "scrapy_proxies.RandomProxy": 100,
   "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 110,
}

RETRY_TIMES = 5
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408, 429]

PROXY_LIST = 'proxies.txt'
PROXY_MODE = 0

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.5
AUTOTHROTTLE_MAX_DELAY = 5
AUTOTHROTTLE_TARGET_CONCURRENCY = 4.0

FEED_EXPORT_ENCODING = "utf-8"
