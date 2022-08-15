from abc import ABCMeta, abstractmethod
import re

from modules.transport.transport import TransportLayer


class CrawlerInterface(metaclass=ABCMeta):
    """
    crawler interface class
    """
    name = ''

    source = ''
    data = ''

    need_proxy = False
    need_change_header = False

    def __init__(self):
        self.transport = TransportLayer([])

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

    @staticmethod
    def analyse_line(line:str):
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
            years = val.group(0).strip()
        except Exception as e:
            pass

        val = re.search('([A-Z]+)', values)
        ticker = 'NONE'
        try:
            ticker = val.group(0).strip()
        except Exception as e:
            pass

        return f'{amount} {ticker} {years}'
