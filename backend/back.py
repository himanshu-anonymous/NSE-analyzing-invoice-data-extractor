import yfinance as yf
import pandas as pd
from typing import List, Dict

def fetch_multiple_stock_data(stock_symbols: List[str], pe_ratio_limit: float = None) -> pd.DataFrame:
    """
    Fetch stock data for multiple stock symbols and return it as a pandas DataFrame.
    
    :param stock_symbols: List of stock symbols (e.g., ["AAPL", "GOOGL", "MSFT"]).
    :param pe_ratio_limit: Optional PE ratio threshold for filtering (e.g., 30).
    :return: A Pandas DataFrame containing stock data, possibly filtered.
    """
    try:
        # Create an empty list to store stock data
        stock_data = []

        # Loop through each stock symbol and fetch data
        for symbol in stock_symbols:
            print(f"Fetching data for {symbol}...")
            stock = yf.Ticker(symbol)
            # Get stock info and current price
            info = stock.info
            pe_ratio = info.get("trailingPE", None)

            # Apply filter if a PE ratio limit is provided
            if pe_ratio_limit and pe_ratio and pe_ratio > pe_ratio_limit:
                print(f"Skipping {symbol} (PE ratio {pe_ratio} is above {pe_ratio_limit})")
                continue

            stock_data.append({
                "Symbol": symbol,
                "Name": info.get("longName", "N/A"),
                "Sector": info.get("sector", "N/A"),
                "Current Price": info.get("regularMarketPrice", "N/A"),
                "PE Ratio": pe_ratio,
                "Market Cap": info.get("marketCap", "N/A"),
                "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),
                "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),
                "Annual Return (%)": info.get("regularMarketChangePercent", "N/A")
            })

        # Convert the list of dictionaries to a Pandas DataFrame
        stock_table = pd.DataFrame(stock_data)
        return stock_table

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def filter_stocks_for_goal(stock_data_df: pd.DataFrame, target_percentage: float) -> pd.DataFrame:
    """
    Filters stocks based on the goal of achieving a target percentage in returns.
    
    :param stock_data_df: The DataFrame containing stock data.
    :param target_percentage: The target percentage profit.
    :return: A DataFrame of stocks that have the potential to meet the goal.
    """
    # Filter based on the stocks' Annual Return percentages
    filtered_stocks = stock_data_df[stock_data_df["Annual Return (%)"].apply(pd.to_numeric, errors='coerce') >= target_percentage]
    return filtered_stocks
