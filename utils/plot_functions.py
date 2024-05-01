import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator


def plot_stock_data(
    data: pd.Series,
    stock_name: str,
    figsize: tuple = (15, 6),
    xlabel: str = "Date",
    ylabel: str = None,
    title: str = None,
    grid: bool = True,
    color: str = "blue",
    linestyle: str = "-",
    xlabel_fontsize: int = 18,
    ylabel_fontsize: int = 18,
    title_fontsize: int = 24,
    tick_label_fontsize: int = 14,
    x_timestamps: bool = True,
    **kwargs,
):
    """
    Plots the graph of the stock data.

    Parameters:
        data (pd.Series): The stock data to be plotted.
        stock_name (str): The name of the stock.
        figsize (tuple, optional): The size of the figure (width, height) in inches. Default is (15, 6).
        xlabel (str, optional): The label for the x-axis. Default is "Date".
        ylabel (str, optional): The label for the y-axis. If None, it will use the name of the data series.
        title (str, optional): The title of the plot. If None, it will generate a default title.
        grid (bool, optional): Whether to show grid lines. Default is True.
        color (str, optional): The color of the line plot. Default is 'blue'.
        linestyle (str, optional): The line style of the plot. Default is '-'.
        xlabel_fontsize (int, optional): Font size of x-axis label. Default is 12.
        ylabel_fontsize (int, optional): Font size of y-axis label. Default is 12.
        title_fontsize (int, optional): Font size of plot title. Default is 14.
        tick_label_fontsize (int, optional): Font size of tick labels. Default is 10.
        x_timestamps (bool, optional): Whether to display x-axis as timestamps. Default is False.
        **kwargs: Arbitrary keyword arguments to be passed to the matplotlib plot function.

    Returns:
        fig (matplotlib.figure.Figure): The matplotlib Figure object.
    """

    fig, ax = plt.subplots(figsize=figsize)
    if isinstance(data, list):
        for d in data:
            ax.plot(d, color=color, linestyle=linestyle, **kwargs)
    else:
        ax.plot(data, color=color, linestyle=linestyle, **kwargs)

    if x_timestamps:
        ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))  # Format x-axis as timestamps

    ax.set_xlabel(xlabel, fontsize=xlabel_fontsize)

    if ylabel is None:
        ax.set_ylabel(data.name, fontsize=ylabel_fontsize)
        title = f"{data.name} of {stock_name} Data"
    else:
        ax.set_ylabel(ylabel, fontsize=ylabel_fontsize)
        title = f"{ylabel} of {stock_name} Data"

    ax.set_title(title, fontsize=title_fontsize)
    ax.tick_params(axis="both", which="major", labelsize=tick_label_fontsize)
    ax.grid(grid)
    # Limit x ticks to 7
    ax.xaxis.set_major_locator(MaxNLocator(7))

    return fig
