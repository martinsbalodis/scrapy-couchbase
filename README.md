scrapy-couchbase
================

Scrapy downloader middleware for caching crawled data in couchbase

Configuration
=============
configure scrapy settings.py

```python
# stora data in couchDB
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 543,
    }
HTTPCACHE_ENABLED=True
HTTPCACHE_STORAGE='scrapycouchbase.CouchBaseCacheStorage'
COUCHBASE_SERVER = 'couchbase:8091'
COUCHBASE_BUCKET = 'scrapy'
COUCHBASE_PASSWORD = ''
```