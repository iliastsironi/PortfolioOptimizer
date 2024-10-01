import yfinance as yf
import pandas as pd
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_stock_data(stock_symbols, start_date='2020-01-01', end_date=None, save_csv=False, csv_path='data/stock_data.csv'):
    """
    Fetch historical adjusted closing prices for the given stock symbols.

    Parameters:
    - stock_symbols (list of str): List of stock ticker symbols.
    - start_date (str): Start date in 'YYYY-MM-DD' format.
    - end_date (str or None): End date in 'YYYY-MM-DD' format. Defaults to today's date if None.
    - save_csv (bool): Whether to save the fetched data to a CSV file.
    - csv_path (str): Path to save the CSV file.

    Returns:
    - pd.DataFrame: DataFrame containing adjusted closing prices.
    """
    try:
        if end_date is None:
            end_date = datetime.today().strftime('%Y-%m-%d')

        logger.info(f"Fetching data for stocks: {stock_symbols} from {start_date} to {end_date}")

        # Fetch the stock data using yfinance
        data = yf.download(stock_symbols, start=start_date, end=end_date)

        if data.empty:
            logger.error("No data fetched. Please check the stock symbols and date range.")
            return pd.DataFrame()

        # Extract the adjusted closing prices
        closing_prices = data['Adj Close']

        # Handle cases where single stock is fetched; ensure it's a DataFrame
        if isinstance(closing_prices, pd.Series):
            closing_prices = closing_prices.to_frame()

        # Save to CSV if requested
        if save_csv:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            closing_prices.to_csv(csv_path)
            logger.info(f"Stock data saved to {csv_path}")

        logger.info("Stock data fetched successfully.")
        return closing_prices

    except Exception as e:
        logger.exception("An error occurred while fetching stock data.")
        return pd.DataFrame()
