from crypto_scraping import (
    get_img,
    get_link,
    get_low_high,
    get_market_price,
    get_price,
    get_short_title,
    get_soup,
    save_json,
)


headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}


# list of popular cryptocurrency
currencies = [
    "tether",
    "ethereum",
    "bitcoin",
    "tether",
    "cardano",
    "usd-coin",
    "bnb",
    "solana",
    "dogecoin",
]
# empty list to storage data
crypto_currency = []

for currency in currencies:
    soup = get_soup(currency_name=currency, headers=headers)

    short_title = get_short_title(soup=soup)
    price = get_price(soup=soup)
    market_price = get_market_price(soup=soup)
    low24 = get_low_high(soup=soup)[0]
    high24 = get_low_high(soup=soup)[1]
    website = get_link(soup=soup)
    img = get_img(soup=soup, short_title=short_title)

    crypto = {
        "title": currency,
        "information": {
            "short_title": short_title,
            "price": price,
            "low_high_24h": {
                "low": low24,
                "high": high24,
            },
            "market_price": market_price,
            "website": website,
            "img": img[0],
            "path": img[1],
        },
    }
    crypto_currency.append(crypto)

print(save_json(crypto_currency))
