from bs4 import BeautifulSoup
import requests
import json
from utils import normalize_volume


# This script scrapes the Silpo website for sunflower oil prices and volumes.
def get_silpo(need_print=False):
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
        item_volume = normalize_volume(item_volume_obj.text)

        item_price_obj = product.find(
            "div",
            class_="product-card-price__displayPrice"
        )

        if not item_price_obj:
            continue
        item_price = item_price_obj.text.strip().split(" ")[0]

        data.append(
            {
                'price': item_price,
                'name': item_name,
                'volume': item_volume
            }
        )
    if need_print:
        print("name -> Price")
        for i in data:
            print(f"{i['price']} -> {i['name']} -> {i['volume']}")

    # Save the data to a JSON file
    with open("silpo.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    get_silpo(need_print=True)
    print("Silpo data saved to silpo.json")
