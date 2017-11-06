# encoding=utf-8
# aiohttp+asyncio+uvloop脚手架
import asyncio
import cgi
import re
import ujson
import arrow
import aiohttp
from lxml import etree
from urllib.parse import urlparse, urljoin, splitport
import csv
import time
from asyncio import Queue
from settings import USER_AGENTS, INTINTERVAL
from parser import Parser


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(USER_AGENTS)
}


class Crawler:
    def __init__(self, roots, loop, max_tries=5, max_tasks=10):
        self.loop = loop
        self.roots = roots
        self.max_tries = max_tries
        self.max_tasks = max_tasks
        self.q = Queue(loop=self.loop)
        self.done = []
        self.seen_urls = set()
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.t0 = time.time()
        self.t1 = None
        self.root_domains = []
        for root in roots:
            self.add_url(root)
            parts = urlparse(root)
            host, port = splitport(parts.netloc)
            if not host:
                continue
            else:
                self.root_domains.append(host)

    def close(self):
        self.session.close()

    def add_url(self, url):
        """
        """
        print('url added to queue: %s' % url)
        self.seen_urls.add(url)
        self.q.put_nowait(url)

    async def fetch_etree(response):
        if response.status == 200:
            content_type = response.headers.get('content-type')
            if content_type:
                cotnent_type, _ = cgi.parse_header(content_type)
            if content_type in ('text/html', 'application/xml'):
                text = await response.text()
                return etree.HTML(text.encode('utf-8'))

    async def crawl(self):
        workers = [asyncio.Task(self.work(), loop=self.loop) for _ in range(self.max_tasks)]
        self.t0 = time.time()
        await self.q.join()
        self.t1 = time.time()
        for w in workers:
            w.cancel()

    async def work(self):
        try:
            while True:
                url = await self.q.get()
                assert url in self.seen_urls
                await self.fetch(url)
                self.q.task_done()
        except asyncio.CancelledError as e:
            print(e)

    async def fetch(self, url):
        tries = 0
        exception = None
        while tries < self.max_tries:
            try:
                response = await self.session.get(url, headers=headers, allow_redirects=False)
                break
            except aiohttp.ClientError as client_error:
                exception = client_error
                print(exception)
            tries += 1
        else:
            print('Max tries exceed: %s' % url)
            return

        try:
            tree = await self.fetch_etree(response)
            parser = Parser()
            result, links = parser.parse(tree, url)
            for link in links.difference(self.seen_urls):
                self.add_url(link)
            self.seen_urls.update(links)
        finally:
            await response.release()
            await asyncio.sleep(INTERVAL)

    def record_result(self, result):
        pass
