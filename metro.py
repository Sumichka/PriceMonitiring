
from bs4 import BeautifulSoup
import requests
import json
from utils import normalize_volume


# This script scrapes the Metro website for sunflower oil prices and volumes.
def get_metro(need_print=False):
    url = "https://metro.zakaz.ua/uk/categories/sunflower-oil-metro/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    data = []
    for product in soup.find_all(
        "div",
        class_="jsx-b98800c5ccb0b885 ProductsBox__listItem"
    ):
        item_name_obj = product.find(
            "span", 'jsx-12c0bb202e78d6b5 ProductTile__title'
        )
        if not item_name_obj:
            continue
        item_name = item_name_obj.text.strip()

        item_volume_obj = product.find(
            "div", 'jsx-12c0bb202e78d6b5 ProductTile__weight'
        )
        if not item_volume_obj:
            continue
        item_volume = normalize_volume(item_volume_obj.text)

        item_price_obj = product.find(
            "span", "jsx-a1615c42095f26c8 Price__value_caption"
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
    with open("metro.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    get_metro(need_print=True)
    print("Metro data saved to metro.json")
