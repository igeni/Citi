from .interface import CrawlerInterface


class S3Crawler(CrawlerInterface):
    name = 'S3'
    data = ''

    def set_source(self, source:str):
        self.source = source


    def get_new_tasks(self):
        page = self.transport.get(self.source)

        if page.status_code == 200:
            self.data = page.text
        else:
            self.data = ''

    def get_result(self):
        try:
            pass
            self.get_new_tasks()

            res = self.data.split('\n')

            if res[0] == 'message\r':
                for line in res[1:]:
                    result = self.analyse_line(line)
                    print(result)
            else:
                exit('Data source is not valid')

        except:
            pass

    def start(self):
        pass
