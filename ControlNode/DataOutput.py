# coding:utf-8
import codecs
import time


class DataOutput(object):
    def __init__(self):
        self.filepath = 'Douban_%s.html' % (time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))
        # self.output_head(self.filepath) 将这条语句的位置改为在函数store_proc中，否则会在SpiderNode文件夹中产生多余的HTML文件
        self.datasHTML = []  # 用来存取HTML数据

    def store_data(self, data):
        if data is None:
            return
        self.datasHTML.append(data)
        if len(self.datasHTML) > 10:
            self.output_html(self.filepath)

    def output_head(self, path):
        """
        将HTML头写进去
        :return:
        """
        fout = codecs.open(path, 'w', encoding='utf-8')
        fout.write("<html>")
        fout.write(r'''<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />''')
        fout.write("<body>")
        fout.write("<table>")
        fout.close()

    def output_html(self, path):
        """
        将数据写入HTML文件中
        :param path: 文件路径
        :return:
        """
        fout = codecs.open(path, 'a', encoding='utf-8')
        for data in self.datasHTML:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data['url'])
            fout.write("<td>%s</td>" % data['title'])
            fout.write("<td>")
            fout.write("%s" % data['summary'])
            fout.write("</td>")
            fout.write("</tr>")
        self.datasHTML = []
        fout.close()

    def output_end(self, path):
        """
        输出HTML结束
        :param path: 文件存储路径
        :return:
        """
        fout = codecs.open(path, 'a', encoding='utf-8')
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()
