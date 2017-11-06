# encoding=utf-8
from crawler import Crawler, create_csv
import asyncio
import uvloop


def run():
    create_csv()
    base = 'https://tj.lianjia.com/zufang/pg%s/'
    roots = [base % i for i in range(1,101)]
    # roots = ['https://tj.lianjia.com/zufang/pg1/']
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    crawler = Crawler(roots=roots, loop=loop, max_tasks=100)
    loop.run_until_complete(crawler.crawl())
    print('Finish {0} items in {1:.3f} secs'.format(len(crawler.done), crawler.t1 - crawler.t0))
    crawler.close()

if __name__ == '__main__':
    run()
