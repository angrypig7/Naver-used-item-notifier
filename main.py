import requests
# import bs4
from bs4 import BeautifulSoup
from urllib import parse

keyword = "키크론 K3"
options = {
    "where": "article",
    "ie": "utf8",
    "prdtype": 4,
    "t": 0,
    "st": "date",
    "srchby": "text",
    "dup_remove": 1,
    "sm": "tap_opt",
    "nso": "so:dd,p:all,a:all",
    "nso_open": 1,
    "rev": 44
}
link_naver_search = "https://search.naver.com/search.naver?"

def main():
    print("Naver-used-item-notifier")

    link = formatLink(link_naver_search, keyword)
    print("LOG: link to parse: {}".format(link))

    webGet(link)


def formatLink(link_arg, keyword_arg):
    url = ""
    # query = {"query": keyword_arg}
    options["query"] = keyword_arg
    # url_params = parse.urlparse(url)
    url_params = parse.urlencode(options, doseq=True)
    url = link_arg + str(url_params)

    return url

def webGet(link_arg):
    req = requests.get(link_arg)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    print("LOG: req: {}".format(req))
    # print("LOG: html: {}".format(html))
    print("LOG: soup: {}".format(soup))


if __name__ == "__main__":
    main()

# https://search.naver.com/search.naver?where=article&ie=utf8&query=%ED%82%A4%ED%81%AC%EB%A1%A0+K3&prdtype=4&t=0&st=date&srchby=text&dup_remove=1&cafe_url=&without_cafe_url=&sm=tab_opt&nso=so:dd,p:all,a:all&nso_open=1&rev=44

# https://search.naver.com/search.naver?where=article&query=%ED%82%A4%ED%81%AC%EB%A1%A0%20K3&ie=utf8&st=date&date_option=0&date_from=&date_to=&board=&srchby=text&dup_remove=1&cafe_url=&without_cafe_url=&sm=tab_opt&nso=so%3Add%2Cp%3Aall%2Ca%3Aall&nso_open=1&t=0&mson=0&prdtype=4
