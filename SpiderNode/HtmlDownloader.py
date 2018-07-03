# encoding:utf-8
import requests
import config
from haipproxy.client.py_cli import ProxyFetcher

class HtmlDownloader(object):
    def get_proxies(self, proxy):
        """
        构建格式化的单个proxies
        :param proxy:从redis数据库中得到的http://46.10.157.81:53281形式的ip
        :return:可作requests.get参数的proxies
        """
        ip = proxy.strip('http://')
        proxy_http_ip = "http://"+ ip
        proxy_https_ip ="https://" +ip
        proxies = {'http': proxy_http_ip, 'https': proxy_https_ip, }
        return proxies

    def download(self, url):
        if url is None:
            return None
        args = dict(host='138.68.46.196', port=6380, password='Watermirrorsir', db=0)
        fetcher = ProxyFetcher('douban', strategy='greedy', redis_args=args)
        # 获取一个可用代理
        print(fetcher.get_proxy())
        string = str(fetcher.get_proxy())
        # 获取可用代理列表
        # print(fetcher.get_proxies()) # or print(fetcher.pool)
        proxies = self.get_proxies(string)
        print(proxies)
        r = requests.get(url, headers=config.headers, proxies=proxies)
        #r = requests.get(url, headers=config.headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        return None
