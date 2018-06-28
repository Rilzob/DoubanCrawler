# encoding:utf-8
from bs4 import BeautifulSoup
import requests
import config
import pymongo
import time
import random


class SpiderIPProxy(object):
    def __init__(self):
        self.url = 'http://www.xicidaili.com/wt/'
        # 爬取代理的URL地址，选择的是西刺代理
        self.timeout = 1  # 设定等待时间
        self.num = 2  # 爬取代理的页数，2表示爬取2页的ip地址
        self.url_for_test = 'http://httpbin.org/ip'  # 测试ip的URL

    def download(self, url):
        if url is None:
            return None
        r = requests.get(url, headers=config.headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        return None

    def get_ip_list(self):
        """
        从西刺网站爬取代理
        :return:
        """
        ip_list = []
        for num_page in range(1, self.num):
            url = self.url + str(num_page)
            html_doc = self.download(url)
            soup = BeautifulSoup(html_doc, 'html.parser')
            iplist = soup.find_all('tr', class_='odd')
            for i in range(len(iplist)):
                line = iplist[i].find_all('td')
                ip = line[1].get_text()
                port = line[2].get_text()
                address = ip + ':' + port
                ip_list.append(address)
            time.sleep(self.timeout)
        ip_set = set(ip_list)  # 去掉可能重复的ip
        ip_list = list(ip_set)
        return ip_list

    def get_proxy(self, ip):
        """
        构建格式化的单个proxies
        :param ip:
        :return:
        """
        proxy_http_ip = 'http://' + ip
        proxy_https_ip = 'https://' + ip
        proxies = {'http': proxy_http_ip, 'https': proxy_https_ip}
        return proxies

    def ip_test(self, ip_list):
        for ip_for_test in ip_list:
            proxy_http_ip_test = 'http://' + ip_for_test
            proxy_https_ip_test = 'https://' + ip_for_test
            proxies = {'http': proxy_http_ip_test, 'https': proxy_https_ip_test}
            # 构建格式化的单个proxies
            try:
                response = requests.get(self.url_for_test, headers=config.headers, proxies=proxies, timeout=1)
                if response.status_code == 200:
                    ip = {'ip': ip_for_test}
                    print(response.text)
                    print('测试通过')
                    # 使用下面的Telnet方法，速度可能会更快些
                    # 这里假设有ip_list中某一ip
                    # hd, port = ip.split(':')
                    # try:
                    #     telnetlib.Telnet(hd, port=port, timeout=20)
                    # except:
                    #     print '失败'
                    # else:
                    #     print '成功'
                    self.write_to_MongoDB(ip)
            except Exception as e:
                print(e)
                continue

    def write_to_MongoDB(self, proxies):
        """
        将测试通过的ip存入MongoDB
        :param proxies:
        """
        client = pymongo.MongoClient()
        # 因为是连接在本地电脑，所以不需要任何参数
        # 等价于pymongo.MongoClient('localhost', 27017)
        db = client['PROXY']
        collection = db['proxies']
        result = collection.insert(proxies)
        print(result)
        print('存储MongoDB成功')

    def get_random_ip(self):
        '''
        随机取出一个ip
        '''
        client = pymongo.MongoClient()
        db = client.PROXY
        collection = db.proxies
        items = collection.find()
        length = items.count()
        ind = random.randint(0, length - 1)
        useful_proxy = items[ind]['ip'].replace('\n', '')
        proxy = {
            'http': 'http://' + useful_proxy,
            'https': 'http://' + useful_proxy,
        }
        response = requests.get(self.url_for_test, headers=config.headers, proxies=proxy, timeout=10)
        if response.status_code == 200:
            return useful_proxy
        else:
            print('此{}已失效'.format(useful_proxy))
            collection.remove(useful_proxy)
            print('已经从MongoDB移除')
            self.get_random_ip()


if __name__ == '__main__':
    IPProxyPool = SpiderIPProxy()
    ip_info = IPProxyPool.get_ip_list()
    print(ip_info)
    IPProxyPool.ip_test(ip_info)
    finally_ip = IPProxyPool.get_random_ip()
    print('取出的ip为：' + finally_ip)