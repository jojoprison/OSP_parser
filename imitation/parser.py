import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# Website urls
DRIVER_PATH = "../imitation/geckodriver.exe"
URL = "https://fssp.gov.ru/osp/"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "accept": "*/*"}
driver = webdriver.Firefox(executable_path=DRIVER_PATH)
driver.get(URL)
driver.implicitly_wait(10)

# Start data
departments = set()
department_data = []
index_result = 1


def open_select(area, option_index):
    chosen_select = driver.find_element_by_id("address_" + area + "_chosen")
    chosen_select.click()

    option = chosen_select.find_element(
        By.CSS_SELECTOR, "[data-option-array-index='" + option_index + "']")
    option.click()

    time.sleep(1)

    # print("Option area: " + area + ", option index: " + option_index)


def get_options(page_source, area):
    soup = BeautifulSoup(page_source, "html.parser")
    select_item = soup.find("select", id="address_" + area)

    options = select_item.find_all("option")

    regions = []
    index_elem = 0
    for option in options:
        regions.append({
            'index': index_elem,
            'name': option.get_text(),
        })
        index_elem += 1

    data = [regions, len(regions)]

    print(area + " elements len: " + str(data[1]))

    return data


def get_result(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    result_frame = soup.find("div", class_="results-frame")
    table_result = result_frame.find("tbody")

    if table_result is None:
        info_result = result_frame.find("div")
        return info_result
    else:
        return table_result


def search(area, index_area):
    open_select(area, str(index_area))
    return get_result(driver.page_source)


def increase_index():
    # TODO сделать класс ИЛИ возвращать значения индекса
    global index_result
    index_result += 1


def fill_list(data, index, region, city, street=None):
    if data.get_text(strip=True).startswith("Территориальный"):
        tds = data.find_all("td")

        department_name = tds[0].text

        if department_name not in departments:
            department_data.append({
                'index': index,
                'region': region,
                'city': city,
                'street': street,
                'department': department_name,
                'address': tds[1].text,
                'bailiff': tds[2].text,
                'phone_number': tds[3].text,
                'fax': tds[4].text,
                'business hours': tds[5].text,
                'support_phone_numbers': tds[6].text,
                'service_areas': tds[7].text
            })
            increase_index()

            departments.add(department_name)


def search_by_city(region_name, city_index, city_name):
    try:
        search_result = search("city", city_index)
    except AttributeError:
        time.sleep(1)
        search_result = search("city", city_index)

    if search_result.text == "Введите уточняющие данные":
        streets = get_options(driver.page_source, "street")
        street_names = streets[0]
        street_len = streets[1]
        street_index = 1
        # TODO test street_len
        while street_index < street_len:
            search_result = search("street", street_index)
            street_name = street_names[street_index].get("name")

            if search_result.text == "Введите уточняющие данные":
                houses = get_options(driver.page_source, "house")
                houses_len = houses[1]
                for house in range(1, houses_len + 1):
                    search_result = search("house", street_index)
                    fill_list(search_result, index_result, region_name,
                              city_name, street_name)
            else:
                fill_list(search_result, index_result, region_name,
                          city_name, street_name)

            street_index += 1
    else:
        fill_list(search_result, index_result, region_name, city_name)


def search_by_region(region_index, region_name):
    open_select("region", str(region_index))

    cities = get_options(driver.page_source, "city")
    cities_len = cities[1]
    city_index = 1

    # TODO test cities_len
    while city_index < cities_len:
        city_name = cities[0][city_index].get("name")
        search_by_city(region_name, city_index, city_name)
        city_index += 1


def run(region_index):
    try:
        screen_height = driver.execute_script("return window.screen.height;")
        driver.execute_script("window.scrollTo(0, {screen_height});".format(screen_height=screen_height / 2))

        regions_data = get_options(driver.page_source, "region")
        regions = regions_data[0]
        regions_len = regions_data[1]

        print("Search of region: " + str(regions[region_index]))

        search_by_region(region_index, regions[region_index].get("name"))
    except Exception as ex:
        print("GET ERROR:\n", ex)

    print(department_data)
    print(departments)

    with open("results_" + str(region_index) + ".txt", "w") as file:
        print(department_data, file=file)

    driver.close()


run(5)
