# encoding:utf-8
import requests
import config
from XiciIPProxyPool.SpiderIPProxy import SpiderIPProxy


if __name__ == '__main__':
    IPProxy = SpiderIPProxy()
    proxies = IPProxy.get_proxy('192.116.142.153:8080')
    print(proxies)
    r = requests.get('https://book.douban.com/tag/?view=type&icn=index-sorttags-all', headers=config.headers, proxies=proxies)
    # r = requests.get('https://book.douban.com/subject/30170099/', headers=config.headers, proxies=proxies)
    if r.status_code == 200:
        r.encoding = 'utf-9'
        print(r.text)
        print('访问成功！')
    else:
        print('访问失败！')