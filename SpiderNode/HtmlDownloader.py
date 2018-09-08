# encoding:utf-8
import requests
import config

class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        r = requests.get(url, headers=config.headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        else:
            print('下载网页内容失效！')
            return