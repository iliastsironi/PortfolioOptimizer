import numpy as np
import pandas as pd
import logging

# Configure Logger
logger = logging.getLogger(__name__)

def calculate_daily_returns(stock_data):
    """
    Calculate daily returns from stock data.

    Parameters:
    - stock_data (pd.DataFrame): DataFrame containing adjusted closing prices.

    Returns:
    - pd.DataFrame: DataFrame of daily returns.
    """
    try:
        if not isinstance(stock_data, pd.DataFrame):
            logger.error("stock_data must be a pandas DataFrame.")
            raise ValueError("stock_data must be a pandas DataFrame.")

        logger.info("Calculating daily returns.")
        returns = stock_data.pct_change().dropna()

        if returns.empty:
            logger.error("Daily returns calculation resulted in an empty DataFrame.")
            raise ValueError("Daily returns calculation resulted in an empty DataFrame.")

        logger.info("Daily returns calculated successfully.")
        return returns

    except Exception as e:
        logger.exception("An error occurred while calculating daily returns.")
        raise

def calculate_expected_returns(returns):
    """
    Calculate expected annualized returns from daily returns.

    Parameters:
    - returns (pd.DataFrame): DataFrame of daily returns.

    Returns:
    - pd.Series: Expected annualized returns.
    """
    try:
        if not isinstance(returns, pd.DataFrame):
            logger.error("returns must be a pandas DataFrame.")
            raise ValueError("returns must be a pandas DataFrame.")

        logger.info("Calculating expected annualized returns.")
        expected_returns = returns.mean() * 252  # Assuming 252 trading days in a year

        if expected_returns.empty:
            logger.error("Expected returns calculation resulted in an empty Series.")
            raise ValueError("Expected returns calculation resulted in an empty Series.")

        logger.info("Expected annualized returns calculated successfully.")
        return expected_returns

    except Exception as e:
        logger.exception("An error occurred while calculating expected returns.")
        raise

def calculate_covariance_matrix(returns):
    """
    Calculate the annualized covariance matrix from daily returns.

    Parameters:
    - returns (pd.DataFrame): DataFrame of daily returns.

    Returns:
    - pd.DataFrame: Annualized covariance matrix.
    """
    try:
        if not isinstance(returns, pd.DataFrame):
            logger.error("returns must be a pandas DataFrame.")
            raise ValueError("returns must be a pandas DataFrame.")

        logger.info("Calculating covariance matrix.")
        cov_matrix = returns.cov() * 252  # Annualizing the covariance

        if cov_matrix.empty:
            logger.error("Covariance matrix calculation resulted in an empty DataFrame.")
            raise ValueError("Covariance matrix calculation resulted in an empty DataFrame.")

        logger.info("Covariance matrix calculated successfully.")
        return cov_matrix

    except Exception as e:
        logger.exception("An error occurred while calculating the covariance matrix.")
        raise
