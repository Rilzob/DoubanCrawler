# encoding:utf-8

from haipproxy.client.py_cli import ProxyFetcher
#args = dict(host='138.68.46.196', port=6380, password='Watermirrorsir', db=0)
#fetcher = ProxyFetcher('zhihu', strategy='greedy', redis_args=args)
# 获取一个可用代理
#print(fetcher.get_proxy())
# 获取可用代理列表
# print(fetcher.get_proxies()) # or print(fetcher.pool)


"""
Test Douban
"""
def get_proxies(proxy):
    """
    构建格式化的单个proxies
    :param proxy:从redis数据库中得到的http://46.10.157.81:53281形式的ip
    :return:可作requests.get参数的proxies
    """
    ip = proxy.strip('https://')
    proxy_http_ip = "http://" + ip
    proxy_https_ip = "https://" + ip
    proxies = {'http': proxy_http_ip, 'https': proxy_https_ip, }
    return proxies

args = dict(host='138.68.46.196', port=6380, password='Watermirrorsir', db=0)
fetcher = ProxyFetcher('douban', strategy='greedy', redis_args=args)
# 获取一个可用代理
print(fetcher.get_proxy())
string = str(fetcher.get_proxy())
# 获取可用代理列表
# print(fetcher.get_proxies()) # or print(fetcher.pool)
print(get_proxies(string))