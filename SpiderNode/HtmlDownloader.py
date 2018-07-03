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
        # proxies = self.IPProxy.get_proxy('192.116.142.153:8080')
        # print(proxies)
        #r = requests.get(url, headers=config.headers, proxies=proxies)
        r = requests.get(url, headers=config.headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        return None
