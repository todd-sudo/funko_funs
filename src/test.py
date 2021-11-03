import requests
from bs4 import BeautifulSoup



url = "https://funko.fans/ru/full_catalog/funko-pop/figurki/star_wars_category/figurka-funko-pop-star-wars-battle-at-echo-base-chewbacca-flocked-amazon-exclusive-art-49755"

response = requests.get(url, cookies={"language": "ru"})
soup = BeautifulSoup(response.content, "lxml")
product_info = soup.find("div", class_="product_info")
title = product_info.find("h1").text.strip()

print(title)