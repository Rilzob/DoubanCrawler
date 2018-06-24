# encoding:utf-8
import re
from bs4 import BeautifulSoup


class HtmlParser(object):
    def parser(self, page_url, html_cont):
        """
        用于解析网页内容抽取url和数据
        :param page_url: 下载页面的url
        :param html_cont: 下载的网页内容
        :return:
        """
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser')
        new_urls = self._get_new_urls(soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def _get_new_urls(self, soup):
        """
        抽取新的url集合
        :param soup: soup
        :return: 返回新的url集合
        """
        new_urls = set()
        links = soup.find_all('a', href=re.compile(r'https://book.douban.com/subject/[0-9]{8}/$'))
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
        :return: 返回有效数据
        """
        data = {}
        data['url'] = page_url
        title = soup.find('div', id='wrapper').find('h1').find('span')
        data['title'] = title.get_text()
        summary = soup.find('div', class_='intro').find_all('p')
        liststr = []
        for i in range(len(summary)):
            liststr.append(summary[i].get_text())
        data['summary'] = ''.join(liststr)
        # 更改了数据格式，便于存入数据库
        return data