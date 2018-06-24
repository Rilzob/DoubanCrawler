# encoding:utf-8
from multiprocess.managers import BaseManager

from SpiderNode.HtmlDownloader import HtmlDownloader
from SpiderNode.HtmlParser import HtmlParser
# from ControlNode.DataOutput import DataOutput


class SpiderWork(object):
    def __init__(self):
        # 初始化分布式进程中的工作节点的连接工作
        # 实现第一步：使用BaseManager注册获取Queue的方法名称
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        # 实现第二步：连接到服务器
        server_addr = '127.0.0.1'
        print("Connect to server %s..." % server_addr)
        # 端口和验证口令注意保持与服务器进程设置的完全一致
        self.m = BaseManager(address=(server_addr, 8002), authkey='douban'.encode('utf-8'))
        # 从网络连接
        self.m.connect()
        # 实现第三步：获取Queue的对象：
        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()
        # 初始化网页下载器和解析器
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        print("初始化成功")

    def crawl(self):
        while(True):
            try:
                if not self.task.empty():
                    url = self.task.get()
                    if url == 'end':
                        print("控制节点通知爬虫节点停止工作...")
                        # 接着通知其他节点停止工作
                        self.result.put({'new_urls': 'end', 'data': 'end'})
                        return
                    print("爬虫节点正在解析：%s" % url.encode('utf-8'))
                    content = self.downloader.download(url)
                    new_urls, data = self.parser.parser(url, content)
                    self.result.put({"new_urls": new_urls, "data": data})
                else:
                    print('Task queue is empty.')
            except EOFError as e:
                print(e)
                print("连接工作节点失败")
                return
            except Exception as e:
                print(e)
                print("Crawl fail.")
        print("Crawl finish.")


if __name__ == "__main__":
    spider = SpiderWork()
    spider.crawl()