# encoding:utf-8
import re
from bs4 import BeautifulSoup
from urllib import parse
from SpiderNode.HtmlDownloader import HtmlDownloader


class HtmlParser(object):
    def main_parser(self, page, url):
        """
        :param page: 每种类别下爬取的页数
        :return:返回的是标签以及完整的url集合
        """
        content = HtmlDownloader().download(url)
        # print(content)
        soup = BeautifulSoup(content, 'html.parser')
        labels = []
        new_urls = []
        label_table_list = soup.find_all('table', {'class': 'tagCol'})
        for label_tabel in label_table_list:
            label_list = label_tabel.find_all('a')
            for label in label_list:
                labels.append(label.get_text())
                new_url = label['href']
                full_url = parse.urljoin('https://book.douban.com/', new_url)
                for i in range(page):
                    full_url = full_url + '?start=' + str(i * 20) + '&type=T'
                    new_urls.append(full_url)
        return labels, new_urls

    def parser(self, page_url, html_cont, option):
        """
        用于解析网页内容抽取url和数据
        :param page_url: 下载页面的url
        :param html_cont: 下载的网页内容
        :return:当option参数为0时解析url，为1时解析data
        """
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser')
        if option == 0:
            new_urls = self._get_new_urls(soup)
            return new_urls
        if option == 1:
            new_data = self._get_new_data(page_url, soup)
            return new_data

    def _get_new_urls(self, soup):
        """
        抽取新的url集合
        :param soup: soup
        :return: 返回新的url集合
        """
        new_urls = set()
        links = soup.find('div', class_='article').find_all('a', href=re.compile(r'https://book.douban.com/subject/\d{7,8}/$'))
        # 更精确的限制了解析区域，之前的则会解析边栏内书籍的url，同时发现书籍url内的图书编号数字不一定有8位
        for link in links:
            # 提取href属性
            new_url = link['href']
            new_urls.add(new_url)
        return new_urls


    def _get_new_data(self, page_url, soup):
        """
        抽取有效数据
        :param page_url: 下载页面的url
        :param soup: soup
        :return:
        """
        data = {}
        data['url'] = page_url
        title = soup.find('div', id='wrapper').find('h1').find('span')
        data['title'] = title.get_text()
        author = soup.find('div', id='info').find('a', class_="")
        data['author'] = author.get_text()
        score = soup.find('div', id='interest_sectl').find('strong')
        data['score'] = score.get_text()
        summary = soup.find('div', class_='intro').find_all('p')
        liststr = []
        for i in range(len(summary)):
            liststr.append(summary[i].get_text())
        data['summary'] = ''.join(liststr)
        # 更改了数据格式，便于存入数据库
        return data
