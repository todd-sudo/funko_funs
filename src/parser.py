import json
import time

from bs4 import BeautifulSoup
from loguru import logger
import requests

from utils import dowload_image
from config import headers, proxies, ru_cookies, ua_cookies


def get_figure(input_filename: str, ru: bool = False, exclusive: bool = False) -> list:
    """ Парсит товары
    """
    domain = "https://funko.fans"
    results = list()
    path = f"results/urls/{input_filename}.json"
    if exclusive:
        path = f"results/urls/exclusive/{input_filename}.json"

    with open(path, "r", encoding='utf-8') as file:
        index = 1
        urls = json.load(file)

        for url in urls:
            specs = list()
            if ru:
                if not "ru/" in url:
                    url = domain + "/ru" + url.split("https://funko.fans")[1]
                    response = requests.get(url, headers=headers, cookies=ru_cookies)
            else:
                response = requests.get(url, headers=headers, cookies=ua_cookies)

            soup = BeautifulSoup(response.content, "lxml")
            product_info = soup.find("div", class_="product_info")
            title = product_info.find("h1").text.strip()
            vendor_code = soup.find("p", class_="art").text.split(":")[-1].strip()
            barcode = soup.find("p", class_="sku").text.split(":")[-1].strip()
            try:
                description = soup.find("div", id="tab_1").find("p").text.strip()
            except Exception:
                description = ""

            tabs_content = soup.find("div", class_="tabs_content")
            specifications = tabs_content.find("div", id="tab_2")
            tags = specifications.find_all("tr")

            for tag in tags:
                td = tag.find_all("td")
                key = td[0].text
                value = td[1].text

                specs.append({key: value})

            image_url = soup.find(class_="swiper-slide").get("href")

            image_name = dowload_image(image_url)


            data_object = {
                "title": title,
                "vendor_code": vendor_code,
                "barcode": barcode,
                "description": description,
                "image": image_name,
                "specifications": specs
            }

            results.append(data_object)
            time.sleep(2)
            logger.info(f"Спаршено страниц: {index}")
            index += 1

    return results
