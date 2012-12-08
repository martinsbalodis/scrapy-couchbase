#!/usr/bin/env python

from distutils.core import setup

setup(name='scrapy-couchbase',
    version='0.1',
    description='Scrapy downloader middleware for caching crawled data in \
                couchbase',
    author='Martins Balodis',
    author_email='martins256@gmail.com',
    url='https://github.com/martinsbalodis/scrapy-couchbase',
    py_modules=['scrapycouchbase'],
)