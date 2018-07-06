# encoding:utf-8
import requests
import config
from haipproxy.client.py_cli import ProxyFetcher
import time

class HtmlDownloader(object):
    def get_proxies(self, proxy):
        """
        构建格式化的单个proxies
        :param proxy:从redis数据库中得到的http://46.10.157.81:53281形式的ip
        :return:可作requests.get参数的proxies
        """
        ip = proxy.strip('https://')
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
        # print(fetcher.get_proxy())
        string = str(fetcher.get_proxy())
        # 获取可用代理列表
        # print(fetcher.get_proxies()) # or print(fetcher.pool)
        proxies = self.get_proxies(string)
        # print(proxies)
        r = requests.get(url, headers=config.headers, proxies=proxies)
        # r = requests.get(url, headers=config.headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        else:  # 之前的程序没有考虑IP被封的情况，虽然爬虫节点仍在解析，但网页的状态码异常，return none没有获得任何数据
            print('IP地址失效')
            time.sleep(75)  # 因为haipproxy检验器检验最短周期为1分钟
            self.download(url)  # 获取新的有效IP代理，递归调用自身
