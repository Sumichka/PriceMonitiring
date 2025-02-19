from bs4 import BeautifulSoup
import requests

url = "https://silpo.ua/category/soniashnykova-oliia-4905"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

data = []
for product in soup.find_all("div", class_="products-list__item"):
    item_name_obj = product.find("div", class_="product-card__title")
    if not item_name_obj:
        continue
    item_name = item_name_obj.text.strip()
    
    item_volume_obj = product.find("span")
    if not item_volume_obj:
        continue
    item_volume = item_volume_obj.text
    item_price_obj = product.find("div", class_="product-card-price__displayPrice")
    if not item_price_obj:
        continue
    item_price = item_price_obj.text.strip().split(" ")[0]



    data.append([item_price, item_name, item_volume])

print("name -> Price")
for i in data:
    print(f"{i[0]} -> {i[1]} -> {i[2]}")