from abc import ABCMeta, abstractmethod

from modules.transport.transport import TransportLayer
from modules.config.config import Config
from modules.log_layer.logger_tool import LoggingLayer
from modules.storages.storage import Storage
from modules.common import StorageType
from modules.crawlers.cache import Cache
from modules.crawlers.tasks import Tasks

import re

class CrawlerInterface(metaclass=ABCMeta):
    """
    storage interface class
    """
    name = ''
    tasks = Tasks()

    source = ''
    data = ''

    need_proxy = False
    need_change_header = False

    def __init__(self, db_file=''):
        self.transport = TransportLayer([])
        self.cfg = Config('settings.cfg')
        self.log = LoggingLayer(self.cfg)

        if not db_file:
            db_file = self.cfg.get_param('DATABASES.SQLite', 'Filename')

        timezone = self.cfg.get_param('DEFAULT', 'SystemTimezone')
        self.storage = Storage(storage_type=StorageType.SQLITE, path_to_db=db_file, timezone=timezone)

        ua_file = self.cfg.get_param('DEFAULT', 'UserAgentsFilename')
        with open(ua_file, 'r') as f:
            lines = f.readlines()
        user_agents = [{"User-Agent":item.strip()} for item in lines if item]
        self.transport.set_headers(user_agents)

        proxies_file = self.cfg.get_param('DEFAULT', 'ProxiesFilename')
        with open(proxies_file, 'r') as f:
            lines = f.readlines()
        proxies = [item for item in lines if item]
        self.transport.set_proxies(proxies)

        self.cache = Cache()
        cache_depth = self.cfg.get_param('DEFAULT', 'CacheDepth')
        already_saved = self.storage.get_all_by_depth(hours=int(cache_depth))
        for url in already_saved:
            self.cache.add(url)

    @abstractmethod
    def start(self):
        """
        start crawler
        """
        raise NotImplementedError

    @abstractmethod
    def get_new_tasks(self):
        """
        collect tasks from website
        """
        raise NotImplementedError

    @abstractmethod
    def get_result(self):
        raise NotImplementedError


    def analyse_line(self, line:str):
        typeOp = 'BUY'
        values = ''

        buy_mark = 'Please buy'
        put_mark = 'Please put us in for'

        if buy_mark in line:
            values = line[len(buy_mark):]
        elif put_mark in line:
            typeOp = 'PUT'
            values = line[len(put_mark):]

        values = values.replace('MM', '000000')
        values = values.replace(' years', 'yr')
        values = values[:-1]

        val = re.search('\s\d+\s', values)
        amount = 0
        try:
            amount = int(val.group(0))
        except Exception as e:
            pass

        val = re.search('\s\d+yr', values)
        years = 0
        try:
            years = val.group(0)
        except Exception as e:
            pass


        val = re.search('\s([A-Z]{3})\s', values)
        ticker = 'NONE'
        try:
            ticker = val.group(0)
        except Exception as e:
            pass


        return f'{amount} {ticker} {years}'








        # raise NotImplementedError

