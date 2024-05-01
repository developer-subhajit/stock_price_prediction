import datetime

import yfinance as yf


def download_stock_data(stock_name:list, date_string:list ):
    # Convert date strings to timestamps

    try:
        timestamps = [datetime.datetime.strptime(date_str, "%Y-%m-%d") for date_str in date_string]
        stock_data = yf.download(stock_name, timestamps[0], timestamps[1], progress=False)
    except Exception as e:     
        return None

    return None if stock_data.empty else stock_data