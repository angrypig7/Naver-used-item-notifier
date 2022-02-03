import logging
import requests
from bs4 import BeautifulSoup
from urllib import parse

keyword = "고양이 간식"
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

    logging.basicConfig(filename="python.log", filemode="w", level=logging.DEBUG)
    # debug, info, warning, error, critical

    link = formatLink(link_naver_search, keyword)
    logging.info("link to parse: {}".format(link))

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
    logging.info("req: {}\n".format(str(req)))

    html = req.text
    # logging.debug("html: {}\n".format(str(html)))

    soup = BeautifulSoup(html, 'html.parser')
    # logging.debug("soup: {}\n".format(str(soup)))

    res_list = soup.select(
        '#_view_review_body_html > div > more-contents > div > ul'
    )
    # logging.debug("res_list: {}\n".format(str(res_list).encode("utf-8")))

    for item in res_list:
        print(item.text)
        print("\nPRINT\n")
        # logging.debug(str(item.text).encode("utf-8"))


if __name__ == "__main__":
    main()

# https://search.naver.com/search.naver?where=article&ie=utf8&query=%ED%82%A4%ED%81%AC%EB%A1%A0+K3&prdtype=4&t=0&st=date&srchby=text&dup_remove=1&cafe_url=&without_cafe_url=&sm=tab_opt&nso=so:dd,p:all,a:all&nso_open=1&rev=44

# https://search.naver.com/search.naver?where=article&query=%ED%82%A4%ED%81%AC%EB%A1%A0%20K3&ie=utf8&st=date&date_option=0&date_from=&date_to=&board=&srchby=text&dup_remove=1&cafe_url=&without_cafe_url=&sm=tab_opt&nso=so%3Add%2Cp%3Aall%2Ca%3Aall&nso_open=1&t=0&mson=0&prdtype=4
