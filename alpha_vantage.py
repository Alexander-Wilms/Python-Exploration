import json
from datetime import datetime
from pathlib import Path
from pprint import pprint
from typing import Any

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import requests


class AlphaVantageWrapper:
    """
    Wrapper class that appends the API key and caches results so as to not exceed the limit of 25 free requests per day
    """

    def __init__(self):
        with open("settings.ini") as f:
            lines = f.readlines()
            for line in lines:
                if "alpha_vantage_api_key" in line:
                    self.api_key = line.split("=")[-1].strip()

    def request(self, url: str) -> dict[str, Any]:
        url_with_api_key = f"{url}&apikey={self.api_key}"

        cache_file = Path("alpha_vantage_cache.json")

        if cache_file.exists():
            with open(cache_file) as f:
                cache_dict = json.load(f)
        else:
            cache_dict = {}

        now = datetime.now()
        year_month_date = now.strftime("%Y-%m-%d")

        cache_found = False
        return_value = {}
        if year_month_date in cache_dict.keys():
            if url_with_api_key in cache_dict[year_month_date].keys():
                print("Using cached value")
                return_value = cache_dict[year_month_date][url_with_api_key]
                cache_found = True
        else:
            cache_dict[year_month_date] = {}

        if not cache_found:
            print("Sending request to API")
            cache_dict[year_month_date][url_with_api_key] = requests.get(url_with_api_key).json()

            with open(cache_file, "w") as f:
                json.dump(cache_dict, f, indent="\t")

            return_value = cache_dict[year_month_date][url_with_api_key]

        return return_value


def plot_timeseries(data: dict):
    parsed_data = {}
    for key, val in data["Weekly Time Series"].items():
        date = pd.to_datetime(key, format="ISO8601")
        close_price = val["4. close"]

        parsed_data[date] = close_price

    pprint(parsed_data)

    unique_dates = [date for date, _ in parsed_data.items()]
    unique_prices = [float(price) for _, price in parsed_data.items()]
    unique_prices = [x for _, x in sorted(zip(unique_dates, unique_prices))]
    unique_dates = sorted(unique_dates)

    # Plotting the close prices
    # plt.scatter(unique_dates, unique_prices, marker="o", linestyle="-")
    plt.plot(unique_dates, unique_prices, marker=None, linestyle="-")
    plt.title(f"{symbol} Close Prices")
    plt.xlabel("Date")
    plt.ylabel("Close Price / €")
    plt.grid(True)

    plt.tight_layout()

    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m %Y"))

    plt.xticks(rotation=45)

    # Define a list of y-axis values for grid lines (multiples of 10)
    y_ticks = range(0, int(max(unique_prices)) + 1, 10)
    plt.yticks(y_ticks)

    plt.show()


# Vanguard FTSE All-World UCITS ETF USD Accumulation
symbol = "VWCE"
wkn = "A2PKXG"
isin = "IE00BK5BQT80"

avw = AlphaVantageWrapper()

pprint(avw.request(f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}"))

symbol = "VWCE.FRK"
pprint(avw.request(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}"))

data = avw.request(f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}")

plot_timeseries(data)
