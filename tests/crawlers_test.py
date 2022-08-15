"""
    crawlers's test
"""

import pytest

from modules.crawlers.crawler import Crawler
from modules.crawlers.s3_crawler import S3Crawler
from modules.common import CrawlerType


def test_crawler():
    with pytest.raises(Exception) as e_info:
        _ = Crawler()

    with pytest.raises(Exception) as e_info:
        _ = Crawler(crawler_type=CrawlerType.UNKNOWN)

    crawler = Crawler(crawler_type=CrawlerType.S3)
    assert crawler.crawler.name == 'S3'

    res = crawler.crawler.analyse_line('Please put us in for 5000008 CAT 5 years?')
    assert res == '5000008 CAT 5yr'

    res = crawler.crawler.analyse_line('Please put us in for 5MM CAT 5 years?')
    assert res == '5000000 CAT 5yr'

    res = crawler.crawler.analyse_line('Please put us in for 5MM CAT 5 years?')
    assert res == '5000000 CAT 5yr'

    res = crawler.crawler.analyse_line('Please put us in for 5000008a CAT 5 years?')
    assert res == '0 CAT 5yr'

    res = crawler.crawler.analyse_line('Please put us in for 5000008a CAT 5yr?')
    assert res == '0 CAT 5yr'

