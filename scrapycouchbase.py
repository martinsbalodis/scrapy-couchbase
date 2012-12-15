from time import time
from w3lib.http import headers_dict_to_raw, headers_raw_to_dict
from scrapy.http import Headers
from scrapy.responsetypes import responsetypes
from urlparse import urlparse
from couchbase.client import Couchbase
import couchbase.exception
import json

class CouchBaseCacheStorage(object):

    def __init__(self, settings):

        server = settings['COUCHBASE_SERVER']
        bucket = settings['COUCHBASE_BUCKET']
        password = settings['COUCHBASE_PASSWORD']
        couchbase = Couchbase(server, bucket, password)
        self.bucket = couchbase[bucket]

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def retrieve_response(self, spider, request):
        """Return response if present in cache, or None otherwise."""
        try:
            doc = json.loads(self.bucket.get(self._inverse_url(request.url))[2])
        except couchbase.exception.MemcachedError:
            return
            # @TODO expiration
        body = doc['response_body']
        url = doc['response_url']
        status = doc['status']
        headers = Headers(headers_raw_to_dict(doc['response_headers']))
        encoding = doc['encoding']
        respcls = responsetypes.from_args(headers=headers, url=url)
        response = respcls(url=url, headers=headers, status=status, body=body,
            encoding=encoding)
        return response

    def store_response(self, spider, request, response):
        """Store the given response in the cache."""
        data = {
            '_id': self._inverse_url(request.url),
            'url': request.url,
            'method': request.method,
            'status': response.status,
            'response_url': response.url,
            'timestamp': time(),
            'response_body': response.body_as_unicode(),
            'response_headers': headers_dict_to_raw(response.headers),
            'request_headers': headers_dict_to_raw(request.headers),
            'request_body': request.body,
            'encoding': response.encoding
        }
        _id = self._inverse_url(request.url)
        self.bucket.add(_id, 0, 0, json.dumps(data))

    def _inverse_url(self, url):
        elements = urlparse(url)
        return ".".join(elements.netloc.split('.')[::-1])+':'+elements.scheme\
               +elements.path+elements.query