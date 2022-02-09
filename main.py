import logging
import logging.handlers
import requests
from bs4 import BeautifulSoup
from urllib import parse
from notify_run import Notify

keyword = '고양이 간식'
options = {
    'where': 'article',
    'ie': 'utf8',
    'prdtype': 4,
    't': 0,
    'st': 'date',
    'srchby': 'text',
    'dup_remove': 1,
    'sm': 'tap_opt',
    'nso': 'so:dd,p:all,a:all',
    'nso_open': 1,
    'rev': 44
}
link_naver_search = 'https://search.naver.com/search.naver?'

logger = logging.getLogger("root")

notify = Notify()
# notify.send('asdf')

class MyClass:
    def __init__(self):
        self.link = list()
        self.title = list()
        self.text = list()

parseData = MyClass()

def main():
    setLogging()

    logger.info('Naver-used-item-notifier')
    # debug, info, warning, error, critical

    link = formatLink(link_naver_search, keyword)
    logger.info('link: {}'.format(link))

    getLink(parseData, link)


def setLogging():
    # formatter = logging.Formatter('[%(levelname)8s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
    # formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(funcName)s:%(lineno)s] %(asctime)s.%(msecs)d > %(message)s', '%H:%M:%S')
    formatter = logging.Formatter('[%(levelname)s|%(funcName)s] %(asctime)s.%(msecs)d > %(message)s', '%H:%M:%S')

    # fileMaxByte = 1024 * 1024 * 100 #100MB
    # fileHandler = logging.handlers.RotatingFileHandler(filename='./python.log', maxBytes=fileMaxByte, backupCount=10, encoding='utf-8')
    # RotatingFileHandler only takes 'append' mode
    fileHandler = logging.FileHandler("python.log", mode='w', encoding='utf-8')
    streamHandler = logging.StreamHandler()

    fileHandler.setFormatter(formatter)
    streamHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    logger.setLevel(logging.INFO)

    # logging.basicConfig(filename='python.log', filemode='w', level=logging.DEBUG)


def formatLink(link_arg, keyword_arg):
    url = ''
    # query = {'query': keyword_arg}
    options['query'] = keyword_arg
    # url_params = parse.urlparse(url)
    url_params = parse.urlencode(options, doseq=True)
    url = link_arg + str(url_params)

    return url

def getLink(dataClass, link_arg):
    req = requests.get(link_arg)
    logger.info('req: {}\n'.format(str(req)))

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    res_link = soup.find_all('a', 'thumb_single')

    for count in range(len(res_link)):
        dataClass.link.append(res_link[count].get('href').split('?')[0])
        logger.info('{}:{}'.format(count, dataClass.link[count]))


if __name__ == '__main__':
    main()

# https://search.naver.com/search.naver?where=article&ie=utf8&query=%ED%82%A4%ED%81%AC%EB%A1%A0+K3&prdtype=4&t=0&st=date&srchby=text&dup_remove=1&cafe_url=&without_cafe_url=&sm=tab_opt&nso=so:dd,p:all,a:all&nso_open=1&rev=44

# https://search.naver.com/search.naver?where=article&query=%ED%82%A4%ED%81%AC%EB%A1%A0%20K3&ie=utf8&st=date&date_option=0&date_from=&date_to=&board=&srchby=text&dup_remove=1&cafe_url=&without_cafe_url=&sm=tab_opt&nso=so%3Add%2Cp%3Aall%2Ca%3Aall&nso_open=1&t=0&mson=0&prdtype=4
