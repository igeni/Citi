"""
    crawlers's test
"""

import pytest

from modules.crawlers.crawler import Crawler
from modules.crawlers.pastebin_com import S3Crawler
from modules.common import CrawlerType


def test_crawler():
    with pytest.raises(Exception) as e_info:
        _ = Crawler()

    with pytest.raises(Exception) as e_info:
        _ = Crawler(crawler_type=CrawlerType.UNKNOWN)

    crawler = Crawler(crawler_type=CrawlerType.S3)
    assert crawler.crawler.name == 'S3'


    # crawler.crawler.do_work()
    # assert len(crawler.crawler.cache.cache) != 0
    #
    # pb_crawler = S3Crawler(db_file='tests/db_test.sqlite')
    # pb_crawler.cache.cache = {}
    # pb_crawler.do_work()
    #
    # _ = pb_crawler.tasks.all_tasks_keys()
    #
    # assert not pb_crawler.tasks.check('--- abracadabra ---')
    #
    # pb_crawler.cache.init_cache(['my_test_key'])
    # pb_crawler.cache.add("my_other_test_key")
    # assert pb_crawler.cache.check("my_other_test_key")
    # pb_crawler.cache.remove("my_other_test_key")
    # assert not pb_crawler.cache.check("my_other_test_key")
    #


