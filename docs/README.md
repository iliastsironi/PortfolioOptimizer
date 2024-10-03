# Overview

Portfolio Optimizer is a comprehensive tool designed to help investors and financial analysts optimize their investment portfolios based on historical stock data. Leveraging the power of Python's Flask framework for the backend and JavaFX for the frontend, this application provides a seamless experience for fetching stock data, performing mean-variance optimization, and displaying the optimized portfolio along with key performance metrics.

Features: 

* Stock Data Fetching: Retrieve historical adjusted closing prices for specified stock tickers using the yfinance library.
* Portfolio Optimization: Utilize mean-variance optimization to determine the optimal allocation of assets to maximize returns for a given level of risk.
* User-Friendly Interface: JavaFX-based GUI that allows users to input stock tickers, initiate optimization, and view results in an intuitive format.
* Comprehensive Logging: Detailed logs for monitoring application behavior and debugging.
* Error Handling: Robust error handling mechanisms to ensure smooth user experience and easier troubleshooting.

# Technologies Used

Backend:
* Python 3.12
* Flask
* yfinance
* pandas
* NumPy

Frontend:
* Java 22
* JavaFX 23
* JSON (org.json library)

Others:
* Git for version control
* IntelliJ IDEA for Java development

# Backend Setup (Flask API)

Clone the Repository:

    git clone https://github.com/yourusername/PortfolioOptimizer.git
    cd PortfolioOptimizer/backend

Install Dependencies:
    
    pip install -r requirements.txt

# Frontend Setup (JavaFX Application)

1. Navigate to the Frontend Directory:

        cd ../frontend

2. Add JSON Library:

    Ensure that the json-20240303.jar is present in the lib/ directory. If not, download it from the Maven Repository and place it in the lib/ folder.

3. Configure JavaFX:

    * Download JavaFX SDK from the official website.
    * Extract it to a preferred location (e.g., D:\Apps\JavaFX\javafx-sdk-23\).
    * Ensure that the lib directory path is correctly referenced in your IDE or build scripts.

4. Import the Project:

    Open IntelliJ IDEA and import the PortfolioOptimizer project. Ensure that the JavaFX libraries are correctly linked

# Usage
Running the Backend

1. Activate the Virtual Environment:

        cd backend
        # Windows:
        venv\Scripts\activate
        # macOS/Linux:
        source venv/bin/activate
2. Run the Flask Application:

        python app.py
3. Verify the Server is Running:

    Open your browser and navigate to http://127.0.0.1:5000/. You should see a welcome message.

Running the Frontend

1. Open IntelliJ IDEA:

    Navigate to the frontend directory and open the project.

2. Configure VM Options:

    Ensure that the JavaFX libraries are correctly referenced in your run configurations.
    Example VM options:

        --module-path D:\Apps\JavaFX\javafx-sdk-23\lib --add-modules javafx.controls,javafx.fxml
4. Run the Application:

    Execute the Main.java class. The JavaFX interface should launch, allowing you to input stock tickers and optimize your portfolio.

# Contact

For any questions or suggestions, feel free to reach out:

Name: Ilias Tsironis

Email: hliastsironis@gmial.com

GitHub: https://github.com/iliastsironi

LinkedIn: https://www.linkedin.com/in/ilias-tsironis/
