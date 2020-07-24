import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# website urls
URL = "https://fssp.gov.ru/osp/"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "accept": "*/*"}

# Firefox session
driver_path = "geckodriver.exe"
driver = webdriver.Firefox(executable_path=driver_path)
driver.get(URL)
driver.implicitly_wait(10)


def open_select(area, option_index):
    # chosen_select = driver.find_element_by_xpath("//div[@id = 'address_" + area + "_chosen']")
    chosen_select = driver.find_element_by_id("address_" + area + "_chosen")
    chosen_select.click()

    option = chosen_select.find_element(
        By.CSS_SELECTOR, "[data-option-array-index='" + option_index + "']")
    option.click()

    time.sleep(1)


def get_options(page_source, area):
    soup = BeautifulSoup(page_source, "html.parser")
    select_item = soup.find("select", id="address_" + area)

    options = select_item.find_all("option")

    regions = []
    index = 0
    for option in options:
        regions.append({
            'name': option.get_text(),
            'index': index
        })
        index += 1

    # удаляем первый элемент со словом Выбрать
    regions.pop(0)

    print(regions)
    print(len(regions))


# TODO вставить после каждого выбора, начиная с города
def get_result(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    result_frame = soup.find("div", class_="results-frame")
    table_result = result_frame.find("tbody")

    if table_result is None:
        info_result = result_frame.find("div")
        return info_result
    else:
        return table_result


result_data = []

# get_options(driver.page_source, "region")
open_select("region", "1")

screen_height = driver.execute_script("return window.screen.height;")
driver.execute_script("window.scrollTo(0, {screen_height});".format(screen_height=screen_height / 2))

# get_options(driver.page_source, "city")
open_select("city", "1")

result = get_result(driver.page_source)

if result == "Введите уточняющие данные":
    open_select("street", "1")

print(get_result(driver.page_source))

# driver.close()
