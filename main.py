import logging
import logging.handlers
import requests
from bs4 import BeautifulSoup
from urllib import parse
from notify_run import Notify

keyword = '고양이 간식'
flag_mobile = True

options_desktop = {
    'where': 'article',
    'ie': 'utf8',
    'prdtype': '4',
    't': '0',
    'st': 'date',
    'srchby': 'text',
    'dup_remove': '1',
    'sm': 'tap_opt',
    'nso': 'so:dd,p:all,a:all',
    'nso_open': '1',
    'rev': '44',
    'query': ''
}
options_mobile = {
    'abuse': '0',
    'date_option': '0',
    'display': '0',
    'nso_open': '1',
    'prdtype': '4',
    'sm': 'mtb_opt',
    'st': 'date',
    'start': '1',
    'stnm': 'rel',
    'where': 'm_article',
    'opt_tab': '0',
    'nso': 'so:dd,p:all',
    'query': ''
}
options_naver_cafe_api = {
    'useCafeId': 'false',
    'art': ''  # no idea what it is, works with this field left out
    # 'buid': ''  # no idea what it is, works with this field left out
}
link_naver_search_desktop = 'https://search.naver.com/search.naver?'
link_naver_search_mobile = 'https://m.search.naver.com/search.naver?'
link_naver_cafe_api = 'https://apis.naver.com/cafe-web/cafe-articleapi/v2/cafes/{}/articles/'

logger = logging.getLogger("root")

notify = Notify()
# notify.send('asdf')

class MyClass:
    def __init__(self):
        self.itemID = list()  # item ID for browsing naver cafe API
        self.art = list()  # no idea WTF this is
        # self.buid = list()  # no idea WTF this is
        self.cafeName = list()  # used to assemble API link
        self.link = list()  # URL of each item
        self.linkAPI = list()  # URL of naver cafe API for each item
        self.title = list()
        self.price = list()
        self.text = list()

itemData = MyClass()

def main():
    setLogging()

    logger.info('Naver-used-item-notifier')
    logger.debug('Mobile version set as {}'.format(str(flag_mobile)))
    # debug, info, warning, error, critical

    link = ''
    if(flag_mobile == True):
        link = formatSearchLink(link_naver_search_mobile, options_mobile, keyword)
    else:
        link = formatSearchLink(link_naver_search_desktop, options_desktop, keyword)

    logger.info('Link: {}'.format(link))

    getLink(itemData, link)

    updateData(itemData)


def setLogging():
    """logging module setup"""

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

    logger.setLevel(logging.DEBUG)

    # logging.basicConfig(filename='python.log', filemode='w', level=logging.DEBUG)

def formatSearchLink(link_arg, options_arg, keyword_arg):
    """returns URL containing list of items available"""

    url = ''
    options_arg['query'] = keyword_arg
    url_params = parse.urlencode(options_arg, doseq=True)
    url = link_arg + str(url_params)

    return url

def formatAPILink(link_arg, options_arg, item_arg, art_arg, cafeName_arg):
    """returns URL of naver cafe API containing detailed info of each item"""

    link_arg = link_arg.format(cafeName_arg)
    link_arg += item_arg
    link_arg += '?'
    
    url = ''
    options_arg['art'] = art_arg
    # options_arg['buid'] = item_arg

    url_params = parse.urlencode(options_arg, doseq=True)
    url = link_arg + str(url_params)

    return url

def getLink(dataClass, link_arg):
    """browses the given link, saves itemID and link containing details of each item"""
    
    res = requests.get(link_arg)
    logger.debug('HTTP response: {}'.format(str(res)))

    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    res_link = soup.find_all('a', 'thumb_single')

    for i in range(len(res_link)):
        dataClass.itemID.append(res_link[i].get('href').split('/')[-1].split('?')[0])  # 'itemID' for browsing naver cafe API
        dataClass.art.append(res_link[i].get('href').split('/')[-1].split('?')[-1].split('art=')[-1])  # 'art' value requried to access naver cafe API
        dataClass.cafeName.append(res_link[i].get('href').split('/')[3])
        dataClass.linkAPI.append(formatAPILink(link_naver_cafe_api, options_naver_cafe_api, dataClass.itemID[i], dataClass.art[i], dataClass.cafeName[i]))

        flag_strip_url = False  # if True, URL only contains itemID shortening its length, could remove essential fields too
        if flag_strip_url == True:
            dataClass.link.append(res_link[i].get('href').split('?')[0])
        else:
            dataClass.link.append(res_link[i].get('href'))
        
        logger.debug('item {}: {{'.format(i))
        logger.debug('  link: {}'.format(dataClass.link[i]))
        logger.debug('  API link: {}'.format(dataClass.linkAPI[i]))
        logger.debug('  itemID: {}'.format(dataClass.itemID[i]))
        logger.debug('  art: {}'.format(dataClass.art[i]))
        logger.debug('}')
        logger.debug('')

def updateData(dataClass):
    """browses every dataClass.link listed and saves title, price, text of each item"""
    
    for i in range(len(dataClass.link)):
        url = dataClass.linkAPI[i]

        res = requests.get(url)
        logger.debug('item {} - res from {} : {}'.format(i, url, str(res)))
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')

        pass


if __name__ == '__main__':
    main()

# https://search.naver.com/search.naver?where=article&ie=utf8&query=%ED%82%A4%ED%81%AC%EB%A1%A0+K3&prdtype=4&t=0&st=date&srchby=text&dup_remove=1&cafe_url=&without_cafe_url=&sm=tab_opt&nso=so:dd,p:all,a:all&nso_open=1&rev=44

# https://search.naver.com/search.naver?where=article&query=%ED%82%A4%ED%81%AC%EB%A1%A0%20K3&ie=utf8&st=date&date_option=0&date_from=&date_to=&board=&srchby=text&dup_remove=1&cafe_url=&without_cafe_url=&sm=tab_opt&nso=so%3Add%2Cp%3Aall%2Ca%3Aall&nso_open=1&t=0&mson=0&prdtype=4
