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
        ip = self.IPProxy.get_random_ip()
        # print(proxies)
        proxies = self.IPProxy.get_proxy(ip)
        r = requests.get(url, headers=config.headers, proxies=proxies)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        return None
