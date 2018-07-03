# encoding:utf-8
from multiprocess.managers import BaseManager
import time
from multiprocessing import Process, Queue
import config

from ControlNode.DataOutput import DataOutput
from ControlNode.UrlManager import UrlManager


class NodeManager(object):
    def start_Manager(self, url_q, result_q):
        """
        创建一个分布式管理器
        :param url_q: url队列
        :param result_q: 结果队列
        :return:
        """
        # 把创建的两个队列注册在网络上，利用register方法，callable参数关联了Queue对象，
        # 将Queue对象在网络中暴露
        BaseManager.register('get_task_queue', callable=lambda: url_q)
        BaseManager.register('get_result_queue', callable=lambda: result_q)
        # 绑定端口8001，设置验证口令'douban',这个相当于对象的初始化
        manager = BaseManager(address=('', 8002), authkey='douban'.encode('utf-8'))
        # 返回manager对象
        return manager

    def url_manager_proc(self, url_q, conn_q):
        url_manager = UrlManager()
        while True:
            while(url_manager.has_new_url()):
                # 从url管理器中获取新的url
                new_url = url_manager.get_new_url()
                print(new_url)
                # 将新的url发给工作节点
                url_q.put(new_url)
                print('old_url=', url_manager.old_url_size())
                # 加一个判断条件，当爬取2000个链接后就关闭，并保存进度
                if(url_manager.old_url_size() == 2024):  # 这个200只是粗略的给定，实际的url个数远超200
                    # 通知爬虫结点工作结束
                    url_q.put('end')
                    print('控制节点发起结束通知！')
                    # 关闭管理节点，同时存储set状态
                    url_manager.save_progress('new_urls.txt', url_manager.new_urls)
                    url_manager.save_progress('old_urls.txt', url_manager.old_urls)
                    return
            # 将从result_solve_proc获取到的urls添加到URL管理器之间
            try:
                urls = conn_q.get()
                url_manager.add_new_urls(urls)
            except BaseException as e:
                print(e)
                time.sleep(0.1)  # 延时休息
                # 最初延时休息0.1s开始时会出现任务队列为空的状况，猜测原因是解析出来的url还没有传入任务队列中所以加长了延时休息时间
                # 事实证明并不是这个问题，这个问题还没有解决

    def result_solve_proc(self, result_q, conn_q, store_q):
        while(True):
            try:
                if not result_q.empty():
                    # Queue.get(block=True, timeout=None)
                    content = result_q.get(True)
                    if content['new_urls'] == 'end':
                        # 结果分析进程接受通知然后结束
                        print("结果分析进程接受通知然后结束！")
                        store_q.put('end')
                        return
                    conn_q.put(content['new_urls'])  # url为set类型
                    store_q.put(content['data'])  # 解析出来的数据为dict类型
                else:
                    time.sleep(0.5)  # 延时休息
            except BaseException as e:
                time.sleep(0.5)  # 延时休息


    def store_proc(self, store_q):
        output = DataOutput()
        output.output_head(output.filepath)
        while True:
            if not store_q.empty():
                data = store_q.get()
                if data == 'end':
                    print("存储进程然后结束！")
                    output.output_end(output.filepath)
                    output.output_dbend()
                    return
                output.store_data(data)
                new_data = tuple(data.values())
                # 数据的存储需要以元组的形式，所以将数据从原来的dict转换为tuple
                output.store_data_todb(new_data)
            else:
                time.sleep(0.5)
        pass

if __name__ == '__main__':
    # 初始化4个队列
    url_q = Queue()
    result_q = Queue()
    store_q = Queue()
    conn_q = Queue()
    # 创建分布式管理器
    node = NodeManager()
    manager = node.start_Manager(url_q, result_q)
    # 创建url管理进程，数据提取进程和数据存储进程
    url_manager_proc = Process(target=node.url_manager_proc, args=(url_q, conn_q,))
    result_solve_proc = Process(target=node.result_solve_proc, args=(result_q, conn_q, store_q,))
    store_proc = Process(target=node.store_proc, args=(store_q,))
    # 启动三个进程和分布式管理器
    url_manager_proc.start()
    result_solve_proc.start()
    store_proc.start()
    manager.get_server().serve_forever()