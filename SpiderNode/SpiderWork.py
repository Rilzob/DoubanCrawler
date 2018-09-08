# encoding:utf-8
from multiprocess.managers import BaseManager

from SpiderNode.HtmlDownloader import HtmlDownloader
from SpiderNode.HtmlParser import HtmlParser
import config
import time


class SpiderWork(object):
    def __init__(self):
        # 初始化分布式进程中的工作节点的连接工作
        # 实现第一步：使用BaseManager注册获取Queue的方法名称
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        # 实现第二步：连接到服务器
        server_addr = '127.0.0.1'
        print("连接到服务器 %s..." % server_addr)
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
        labels, url_list = self.parser.main_parser(config.page, config.main_url)
        print(url_list)  # url_list里存储的是每个标签的网页地址 eg:https://book.douban.com/tag/小说?start=0%type=T
        print("爬虫结点正在解析主URL：%s" % config.main_url)
        for i in range(3):  # 3代表标签数目，修改为5减少测试时间
        # for i in range(len(url_list)):
            url_list_content = self.downloader.download(url_list[i])
            new_urls = list(self.parser.parser(url_list[i], url_list_content, 0))  # 返回值为set数据类型，为方便后续操作转换为list
            print(new_urls)
            self.result.put({"label": labels[i], "new_urls": new_urls})
            time.sleep(2)
            while(True):
                try:
                    if not self.task.empty():
                        url = self.task.get()  # get到的数据同样为set类型需要进行类型转换
                        if url == 'over':  # over代表该标签下的所有url已全部解析，与end区分一下
                            print('%s标签下所有URL已全部解析' % labels[i])
                            self.result.put({'data': 'over'})
                            break
                        print("爬虫节点正在解析：%s" % url.encode('utf-8'))
                        content = self.downloader.download(url)
                        data = self.parser.parser(url, content, 1)
                        self.result.put({"data": data})
                        time.sleep(2)
                    else:
                        print('任务队列为空！')
                        return
                except EOFError as e:
                    print(e)
                    print("连接工作节点失败！")
                    return
                except Exception as e:
                    print(e)
                    print("爬取失败！")
        url = self.task.get()
        if url == 'end':
            print("控制节点通知其他节点停止工作...")
            self.result.put({'new_urls': 'end', 'data': 'end'})
            print("爬取完成")
            return
        else:
            print(url)
            print("爬取失败")


if __name__ == "__main__":
    spider = SpiderWork()
    spider.crawl()
