import requests
import lxml.html
import urllib
from bs4 import BeautifulSoup

URL = "https://fssp.gov.ru/osp/"
HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
           "accept": "*/*"}
SESSION = requests.Session()


def get_page(url):
    response = urllib.request.urlopen(url)
    return response.read()

def main(url):

    html = get_page(URL)

    data = {
        "code": "7800000000000"
    }

    r = SESSION.post(url, data=data, headers=HEADERS)

    return r


def test_1():
    data = SESSION.get(URL, headers=HEADERS).content
    page = lxml.html.fromstring(data)
    form = page.forms[4] # форма с поиском

    form.fields["region"] = "7800000000000"

    r = SESSION.post("{}{}".format(URL, form.action), data=form.form_values(), headers=HEADERS)

    return r


def test_2():
    res = SESSION.get(URL, headers=HEADERS)
    cookies = dict(res.cookies)

    data = {
        "code": "7800000000000"
    }

    r = SESSION.post("{}{}".format(URL, "/action/get_city_list/"), data=data,
                     headers=HEADERS, cookies=cookies)

    return r


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("form")

    print(items)


def get_city_list():

    html = get_html(URL)

    url = "https://fssp.gov.ru/osp/action/get_city_list/"
    code = 7700000000000

    r = requests.post(url, data={"code": code}, headers=HEADERS)

    soup = BeautifulSoup(r.text, "html.parser")
    items = soup.find("main")

    print(items)

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print("Error")


r = test_2()
print(r.status_code)
print(r.text)

# print(main("https://fssp.gov.ru/osp/action/get_city_list/"))

# soup = BeautifulSoup(r, "html.parser")
# items = soup.find_all("select", name_="city")
#
# print(items)


# print(test_2())
# parse()
# get_city_list()