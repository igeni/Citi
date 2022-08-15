from .s3_crawler import S3Crawler
from modules.common import CrawlerType
from modules.exceptions import WrongCrawlerTypeError


class Crawler:
    crawler = None

    def __init__(self, **params):
        self.crawler_type = params.get('crawler_type', False)

        fail = False
        if self.crawler_type:
            if self.crawler_type == CrawlerType.S3:
                self.crawler = S3Crawler()
                self.crawler.set_source('https://s3.amazonaws.com/aie.interview/input.csv')
                self.crawler.get_result()
            else:
                fail = True
        else:
            fail = True

        if fail:
            raise WrongCrawlerTypeError("you have to define crawler's type correctly ")

    def start(self):
        self.crawler.start()
