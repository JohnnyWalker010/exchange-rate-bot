import time
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup

from constants import URL
from database import ExchangeRate, session


def get_and_save_exchange_rates():
    """
    Fetches the current exchange rate from a website, saves it to a file,
    and adds it to the database.
    """

    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")

    path = (
        "div.VfPpkd-WsjYwc.VfPpkd-WsjYwc-OWXEXe-INsAgc.KC1dQ.Usd1Ac.AaN0Dd.QZMA8b > c-wiz > div > "
        "div:nth-child(1) > div > div.rPF6Lc > div > div:nth-child(1) > div > span > div > div"
    )

    rate_element = soup.select_one(path)
    if rate_element:
        rate = float(rate_element.get_text(strip=True))
        print(f"Current exchange rate: {rate}")

        time_now = datetime.now()
        date = time_now.strftime("%Y-%m-%d")
        hour = time_now.strftime("%H")
        time_str = time_now.strftime("%H:%M:%S")

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
