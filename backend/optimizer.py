import cvxpy as cp
import numpy as np
import logging

# Configure Logger
logger = logging.getLogger(__name__)

def optimize_portfolio(data):
    """
    Optimize the portfolio using mean-variance optimization.

    Parameters:
    - data (dict): Contains 'returns' (np.array), 'cov_matrix' (np.array), and 'target_return' (float).

    Returns:
    - dict: Optimized weights and performance metrics, or an error message if optimization fails.
    """
    try:
        returns = data['returns']
        cov_matrix = data['cov_matrix']
        target_return = data['target_return']

        # Number of assets
        n = len(returns)
        logger.info(f"Number of assets to optimize: {n}")

        # Define the optimization variables
        weights = cp.Variable(n)

        # Define the expected portfolio return
        portfolio_return = returns @ weights

        # Define the portfolio risk (variance)
        portfolio_risk = cp.quad_form(weights, cov_matrix)

        # Define the optimization problem
        problem = cp.Problem(cp.Minimize(portfolio_risk),
                             [cp.sum(weights) == 1,  # Full investment
                              portfolio_return >= target_return,  # Target return
                              weights >= 0])  # No short selling

        # Solve the problem
        problem.solve()

        # Logging optimization status
        logger.info(f"Optimization Status: {problem.status}")
        logger.info(f"Optimal Portfolio Variance: {problem.value}")

        if weights.value is None:
            logger.error("Optimization failed or no solution found.")
            return {"error": "Optimization failed or no solution found."}

        optimized_weights = weights.value
        optimized_weights = np.array(optimized_weights).flatten()

        # Calculate portfolio metrics
        optimized_return = np.dot(returns, optimized_weights)
        optimized_risk = np.sqrt(np.dot(optimized_weights.T, np.dot(cov_matrix, optimized_weights)))
        sharpe_ratio = optimized_return / optimized_risk if optimized_risk != 0 else 0

        logger.info(f"Optimized Portfolio Return: {optimized_return}")
        logger.info(f"Optimized Portfolio Risk: {optimized_risk}")
        logger.info(f"Optimized Portfolio Sharpe Ratio: {sharpe_ratio}")

        return {
            'weights': optimized_weights.tolist(),
            'expected_return': optimized_return,
            'risk': optimized_risk,
            'sharpe_ratio': sharpe_ratio
        }

    except cp.error.SolverError as e:
        logger.exception("SolverError during portfolio optimization.")
        return {"error": f"Solver error: {str(e)}"}
    except Exception as e:
        logger.exception("An unexpected error occurred during portfolio optimization.")
        return {"error": "An unexpected error occurred during portfolio optimization."}
