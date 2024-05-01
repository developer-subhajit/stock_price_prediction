import datetime
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from streamlit_date_picker import PickerType, Unit, date_range_picker

from utils import download_stock_data, plot_stock_data


def main():
    st.title("Stock Price Predictor Web Application")
    st.markdown("---")

    # Set font size for both stock symbol input and subheader

    st.subheader("Please enter the stock symbol")
    stock_name = st.text_input(
        "",
        "GOOG",
        key="stock_input",
        help="Please enter the stock symbol here.",
    )
    st.subheader("Please select the date range")

    date_range_string = date_range_picker(
        picker_type=PickerType.date.string_value,
        start=-1000,
        end=0,
        unit=Unit.days.string_value,
        key="range_picker",
    )

    stock_data = download_stock_data(stock_name, date_range_string)

    if stock_data is None:
        st.write("Please check the Symbol name")
        return None

    # st.write(stock_data)
    fig = plot_stock_data(
        data=stock_data["Adj Close"],
        stock_name=stock_name,
        ylabel="Adj Close",
        color="k",
        grid=False,
        linewidth=1.5,
    )
    st.pyplot(fig)

    model = load_model("Latest_stock_price_model.keras")
    splitting_len = int(len(stock_data) * 0.7)

    x_test = pd.DataFrame(stock_data.Close[splitting_len:])
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(x_test[["Close"]])

    x_data = []
    y_data = []

    for i in range(100, len(scaled_data)):
        x_data.append(scaled_data[i - 100 : i])
        y_data.append(scaled_data[i])

    x_data, y_data = np.array(x_data), np.array(y_data)

    predictions = model.predict(x_data)

    inv_pre = scaler.inverse_transform(predictions)
    inv_y_test = scaler.inverse_transform(y_data)

    ploting_data = pd.DataFrame(
        {"original_test_data": inv_y_test.reshape(-1), "predictions": inv_pre.reshape(-1)},
        index=stock_data.index[splitting_len + 100 :],
    )
    st.subheader("Original values vs Predicted values")
    st.write(ploting_data)

    st.subheader("Original Close Price vs Predicted Close price")

    fig, ax = plt.subplots(figsize=(15, 6))
    plt.plot(pd.concat([stock_data.Close[: splitting_len + 100], ploting_data], axis=0))
    plt.legend(["Train Data", "Original Test data", "Predicted Test data"])
    plt.xlabel("Date", fontsize=18)
    plt.ylabel("Close Price", fontsize=18)
    plt.title("Original Close Price vs Predicted Close price", fontsize=24)
    ax.tick_params(axis="both", which="major", labelsize=14)
    st.pyplot(fig)


if __name__ == "__main__":
    main()
