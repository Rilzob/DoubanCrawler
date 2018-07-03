# encoding:utf-8
import requests
import config
from XiciIPProxyPool.SpiderIPProxy import SpiderIPProxy


class HtmlDownloader(object):
    def __init__(self):
        self.IPProxy = SpiderIPProxy()

    def download(self, url):
        if url is None:
            return None
        proxies = self.IPProxy.get_proxy('118.24.157.22:3128')
        print(proxies)
        r = requests.get(url, proxies=proxies)
        #r = requests.get(url)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        return None


if __name__ == '__main__':
    HtmlDownloader = HtmlDownloader()
    content = HtmlDownloader.download('https://book.douban.com/subject/4908885/')
    print(content)