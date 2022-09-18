import os
import json
import requests
from string import ascii_letters
from datetime import datetime

from bs4 import BeautifulSoup


def get_short_title(soup: BeautifulSoup) -> str:
    """
    Return short title of cryptocurrency
    """
    short_title = soup.find("small", class_="nameSymbol").text
    return short_title


def get_price(soup: BeautifulSoup) -> float:
    """
    Return price of cryptocurrency at time of call
    """
    price = soup.find("div", class_="priceValue").text[1::].strip().split(",")

    if len(price) > 1:
        first_price = int(price[0])
        last_price = float(price[1])
        price = first_price * 1000 + last_price
        return price

    return float(price[0])


def get_low_high(soup: BeautifulSoup):
    """
    Return lowest and highest price in 24h of cryptocurrency
    """
    slider_price = soup.find("div", class_="sliderSection").text.strip()

    for i in ascii_letters:
        slider_price = slider_price.replace(i, "")

    slider_price = slider_price.replace(":", "").split("$")

    if len(slider_price) > 2:
        del slider_price[0]

    low24 = slider_price[0].replace(",", "")
    high24 = slider_price[1].replace(",", "")

    low24 = float(low24)
    high24 = float(high24)

    return low24, high24


def get_market_price(soup: BeautifulSoup) -> float:
    """
    Return market capitalization which is calculated by multiplaying reference price of the cryptoasset by the current circulating supply.
    """
    price = soup.find("div", class_="statsValue").text[1::].strip().split(",")

    result = ""
    for p in price:
        result += p

    return float(result)


def get_link(soup: BeautifulSoup) -> str:
    """
    Return link to official website of cryptocurrency
    """
    link = soup.find("div", class_="buttonName").text
    return f"http://{link}"


def get_img(soup: BeautifulSoup, short_title: str) -> str:
    """
    Save image to file and return link with path to file
    """
    # short_title = short_title.lower()
    if not os.path.exists("images"):
        try:
            os.makedirs("images")
        except OSError:
            print("Folder created.")

    img = soup.find("div", class_="nameHeader").img["src"]
    response = requests.get(img)

    with open(f"images/{short_title}.png", "wb") as f:
        image = f.write(response.content)

    return img, f".images/{short_title}.png"


def get_soup(currency_name: str, headers: str):
    """
    Return html from url which will be scrapping
    """
    URL = f"https://coinmarketcap.com/currencies/{currency_name}/"
    req = requests.get(URL, headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")
    return soup


def save_json(data: list):
    """
    Save all data to folder with current date and file with current time.
    """
    day = datetime.now().strftime("%d.%m.%Y")

    time = datetime.now().strftime("%H-%M-%S")
    if not os.path.exists(f"data/{day}"):
        try:
            os.makedirs(f"data/{day}")
        except OSError:
            print("Folder created.")
    with open(f"data/{day}/{time}.json", "w") as write_file:
        json.dump(data, write_file, indent=4)

    return {"message": f"Created file with path(data/{day}/{time}.json)"}
