from datetime import datetime
import time

import pandas as pd
import requests
from lxml import html

from database import ExchangeRate, session

URL = "https://www.google.com/finance/quote/USD-UAH"


def get_and_save_exchange_rates():
    """
    Fetches the current exchange rate from a website, saves it to a file,
    and adds it to the database.
    """

    url = "https://www.google.com/finance/quote/USD-UAH"
    response = requests.get(url)
    tree = html.fromstring(response.content)

    xpath_expression = (
        '//*[@id="yDmH0d"]/c-wiz[2]/div/div[4]/div/main/div[2]/div[1]/c-wiz/div/div[1]/div/div['
        "1]/div/div[1]/div/span/div/div"
    )

    rate_element = tree.xpath(xpath_expression)
    if rate_element:
        rate = rate_element[0].text_content().strip()
        print(f"Current exchange rate: {rate}")

        current_time = datetime.now()
        date = current_time.strftime("%Y-%m-%d")
        hour = current_time.strftime("%H")
        time_str = current_time.strftime("%H:%M:%S")

        file_name = f"exchange_rates_{date}.xlsx"
        try:
            data = pd.read_excel(file_name, engine="openpyxl")
        except FileNotFoundError:
            data = pd.DataFrame(columns=["Time", "Rate"])

        if data.empty or data.iloc[-1]["Time"][:2] != hour:
            data.loc[len(data)] = [time_str, rate]
            data.to_excel(file_name, index=False, engine="openpyxl")

        exchange_rate = ExchangeRate(rate=rate)
        session.add(exchange_rate)
        session.commit()
    else:
        print("Failed to extract exchange rate.")


while True:
    """
    Continuously fetches and saves exchange rates every hour.
    """

    current_time = datetime.now()
    next_hour = current_time.replace(hour=current_time.hour + 1, minute=0, second=0, microsecond=0)
    time_to_sleep = (next_hour - current_time).total_seconds()
    time.sleep(time_to_sleep)

    get_and_save_exchange_rates()