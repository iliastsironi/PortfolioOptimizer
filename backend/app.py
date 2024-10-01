import os
import logging
from logging.handlers import RotatingFileHandler
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from flask import Flask, request, jsonify
from flask_cors import CORS
from data_fetch import fetch_stock_data
from optimizer import optimize_portfolio
from utils import calculate_daily_returns, calculate_expected_returns, calculate_covariance_matrix
import numpy as np 
from werkzeug.exceptions import BadRequest, InternalServerError

app = Flask(__name__)
CORS(app)  # Initialize CORS

# Ensure the logs directory exists
log_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(log_directory, exist_ok=True)

# Configure Logging
log_file = os.path.join(log_directory, 'app.log')
handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=3)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

@app.route('/')
def home():
    return "Welcome to the Portfolio Optimizer API!"

@app.route('/fetch-data', methods=['POST'])
def fetch_data():
    """
    Endpoint to fetch stock data for given stock symbols.
    Expects JSON payload with 'stocks': list of stock tickers.
    """
    try:
        data = request.get_json()
        if not data or 'stocks' not in data:
            raise BadRequest("Missing 'stocks' in request payload.")

        stock_symbols = data['stocks']
        if not isinstance(stock_symbols, list) or not all(isinstance(symbol, str) for symbol in stock_symbols):
            raise BadRequest("'stocks' must be a list of stock ticker strings.")

        logger.info(f"Fetching data for stocks: {stock_symbols}")
        stock_data = fetch_stock_data(stock_symbols)

        # Check if fetch_stock_data returned an error
        if isinstance(stock_data, dict) and 'error' in stock_data:
            raise InternalServerError(f"Data fetching error: {stock_data['error']}")

        # Convert DataFrame to dictionary with list values
        stock_data_dict = stock_data.to_dict(orient='list')

        return jsonify({
            'status': 'success',
            'data': stock_data_dict
        }), 200

    except BadRequest as e:
        logger.error(f"BadRequest: {e.description}")
        return jsonify({'status': 'error', 'message': e.description}), 400
    except Exception as e:
        logger.exception("An unexpected error occurred in /fetch-data endpoint.")
        return jsonify({'status': 'error', 'message': 'Internal server error.'}), 500

@app.route('/optimize', methods=['POST'])
def optimize():
    """
    Endpoint to optimize the portfolio based on given stock symbols.
    Expects JSON payload with 'stocks': list of stock tickers.
    Optional 'target_return': float (default: 0.1)
    """
    try:
        data = request.get_json()
        if not data or 'stocks' not in data:
            raise BadRequest("Missing 'stocks' in request payload.")

        stock_symbols = data['stocks']
        if not isinstance(stock_symbols, list) or not all(isinstance(symbol, str) for symbol in stock_symbols):
            raise BadRequest("'stocks' must be a list of stock ticker strings.")

        target_return = data.get('target_return', 0.1)  # Default target return of 10%
        if not isinstance(target_return, (int, float)):
            raise BadRequest("'target_return' must be a number.")

        logger.info(f"Optimizing portfolio for stocks: {stock_symbols} with target return: {target_return}")

        # Fetch stock data
        stock_data = fetch_stock_data(stock_symbols)
        if isinstance(stock_data, dict) and 'error' in stock_data:
            raise InternalServerError(f"Data fetching error: {stock_data['error']}")

        # Calculate returns and covariance matrix
        returns = calculate_daily_returns(stock_data)
        expected_returns = calculate_expected_returns(returns)
        cov_matrix = calculate_covariance_matrix(returns)

        # Convert expected_returns and cov_matrix to NumPy arrays
        expected_returns_np = expected_returns.to_numpy()
        cov_matrix_np = cov_matrix.to_numpy()

        # Prepare data for optimization
        optimization_data = {
            'returns': expected_returns_np,
            'cov_matrix': cov_matrix_np,
            'target_return': target_return
        }

        # Optimize the portfolio
        optimized_result = optimize_portfolio(optimization_data)

        if optimized_result is None or 'error' in optimized_result:
            raise InternalServerError("Optimization failed or no solution found.")

        # Extract optimized weights and performance metrics
        optimized_weights = optimized_result['weights']
        portfolio_return = optimized_result['expected_return']
        portfolio_risk = optimized_result['risk']
        sharpe_ratio = optimized_result['sharpe_ratio']

        # Map weights to stock tickers
        weights_dict = dict(zip(stock_symbols, optimized_weights))

        # Structure the response
        response = {
            'status': 'success',
            'optimized_weights': weights_dict,
            'performance': {
                'expected_return': portfolio_return,
                'risk': portfolio_risk,
                'sharpe_ratio': sharpe_ratio
            }
        }

        logger.info("Optimization successful.")
        return jsonify(response), 200

    except BadRequest as e:
        logger.error(f"BadRequest: {e.description}")
        return jsonify({'status': 'error', 'message': e.description}), 400
    except InternalServerError as e:
        logger.error(f"InternalServerError: {e.description}")
        return jsonify({'status': 'error', 'message': e.description}), 500
    except Exception as e:
        logger.exception("An unexpected error occurred in /optimize endpoint.")
        return jsonify({'status': 'error', 'message': 'Internal server error.'}), 500

if __name__ == '__main__':
    # Use environment variable to control debug mode
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)
