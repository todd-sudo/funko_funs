from uuid import uuid4
import os
import time

from bs4 import BeautifulSoup
import requests

from logger import logger


def dowload_image(url: str) -> str:
    """ Скачивает изображение
    """

    index = 1
    path = "media"
    if len(os.listdir(path)) > 900:
        index += 1
        path = path.strip(str(index - 1)) + str(index)
        os.mkdir(path)
    filename = path + f"/{uuid4()}.jpg"
    response = requests.request("GET", url)
    with open(f"{filename}", "wb") as file:
        file.write(response.content)

    return filename


def get_urls(
    exclusive: bool = False, 
    max_page: int = 1
):
    """ Собирает ссылки на товары
    """
    domain = "https://funko.fans/"
    data = list()
    index = 1
    url = "full_catalog/funko-pop/"
    if exclusive:
        url += "figurki-chase/"
    
    for _ in range(max_page):
        if index == 1:
            url = f"full_catalog/funko-pop/"
        else: 
            url = f"full_catalog/funko-pop/?page={index}"

        response = requests.get(url=domain + url)
        soup = BeautifulSoup(response.content, "lxml")

        urls = soup.find_all("a", class_="title")
        for item in urls:
            link = item.get("href")
            data.append(link)

        pagination_list = soup.find("ul", id="pagination_list")
        final_iter = pagination_list.find_all("li")[-1].text.strip()
        logger.info(f"Страниц спаршено: {index}")
        index += 1

        if index == int(final_iter):
            break
        time.sleep(3)
        
    return data


def check_folder():
    if not os.path.exists("results"):
        os.mkdir("results")

    if not os.path.exists("media"):
        os.mkdir("media")

    if not os.path.exists("results/urls"):
        os.mkdir("results/urls")
    
    if not os.path.exists("results/detail"):
        os.mkdir("results/detail")

    if not os.path.exists("results/urls/exclusive"):
        os.mkdir("results/urls/exclusive")
    
    if not os.path.exists("results/detail/exclusive"):
        os.mkdir("results/detail/exclusive")
