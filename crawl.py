# encoding=utf-8
from crawler import Crawler
import asyncio
import uvloop


def run():
    base = 'https://tj.lianjia.com/zufang/pg%s'
    roots = [base % i for i in range(1,101)]
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    crawler = Crawler(roots=roots, loop=loop, max_tasks=100)
    loop.run_until_complete(crawler.crawl())
    print('Finish {0} items in {1:.3f} secs'.format(len(crawler.done), crawler.t0 - crawler.t1))


if __name__ == '__main__':
    run()
