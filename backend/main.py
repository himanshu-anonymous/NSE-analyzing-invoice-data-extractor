from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import sys
from fastapi.middleware.cors import CORSMiddleware
import random

# Add the path to the 'backend' folder where 'back.py' is located
sys.path.append('C:/Users/Priyanshu Patil/Documents/code/backend')
from back import fetch_multiple_stock_data, fetch_stock_data

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow frontend requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, adjust in production for security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Serve static files (HTML, JS, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the main HTML file at the root URL
@app.get("/", response_class=HTMLResponse)
async def serve_html():
    with open("static/main.html", "r") as f:
        return f.read()

# Define the request model for fetching stock data
class StockRequest(BaseModel):
    stocks: list[str]  # List of stock symbols (e.g., ["AAPL", "MSFT"])
    pe_ratio_limit: float = None  # Optional PE ratio limit

# Function to initialize Selenium WebDriver
def initialize_driver():
    """
    Initializes the Selenium WebDriver with necessary options.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to fetch stock data using Selenium scraping
def fetch_stock_data(stock_symbol: str):
    """
    Scrapes stock data for a given symbol from Yahoo Finance.
    :param stock_symbol: The stock symbol to fetch data for.
    :return: Dictionary containing stock price and PE ratio.
    """
    url = f"https://finance.yahoo.com/quote/{stock_symbol}/"
    driver = initialize_driver()
    stock_data = {}

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        # Extract the stock price
        price_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//fin-streamer[@data-field='regularMarketPrice']"))
        )
        stock_data["price"] = price_element.text

        # Extract the PE ratio
        pe_ratio_element = driver.find_element(
            By.XPATH, "//td[contains(text(), 'PE Ratio (TTM)')]/following-sibling::td"
        )
        stock_data["pe_ratio"] = pe_ratio_element.text
    except Exception as e:
        stock_data["error"] = str(e)
    finally:
        driver.quit()

    return stock_data

# Root endpoint
@app.get("/api")
def read_root():
    return {"message": "Welcome to the Stock Data API!"}

# Endpoint to fetch stock data for multiple symbols using 'fetch_multiple_stock_data' from back.py
@app.post("/fetch-stocks")
async def fetch_stocks(data: StockRequest):
    """
    API endpoint to fetch stock data for multiple symbols.
    :param data: List of stock symbols and optional PE ratio limit.
    :return: JSON response with stock data.
    """
    response_data = []

    # Fetch data for the list of stock symbols provided using 'fetch_multiple_stock_data'
    stock_data_df = fetch_multiple_stock_data(data.stocks, data.pe_ratio_limit)
    
    if stock_data_df is None:
        return {"error": "There was an issue fetching the stock data."}

    # Convert the DataFrame to a JSON-friendly format
    stock_data_json = stock_data_df.to_dict(orient="records")
    
    for stock in stock_data_json:
        response_data.append(stock)

    return {"data": response_data}

# Endpoint to fetch stock data for a single symbol using Selenium scraping
@app.post("/fetch-single-stock")
async def fetch_single_stock(symbol: str):
    """
    API endpoint to fetch stock data for a single symbol.
    :param symbol: The stock symbol (e.g., "AAPL")
    :return: JSON response with stock data.
    """
    stock_info = fetch_stock_data(symbol)
    return {"data": stock_info}

# New Endpoint to fetch stock data and serve it for the frontend
@app.get("/get-stock-data/{symbol}")
async def get_stock_data(symbol: str):
    """
    API endpoint to fetch and return stock data for a single symbol in a format suitable for the frontend.
    :param symbol: The stock symbol (e.g., "AAPL")
    :return: JSON response with stock data for frontend usage.
    """
    stock_info = fetch_stock_data(symbol)
    if "error" in stock_info:
        return {"error": stock_info["error"]}

    return {"stock": stock_info}

# New endpoint to fetch suggested stock data for frontend
@app.get("/get-suggested-stocks")
async def get_suggested_stocks():
    """
    API endpoint to fetch a list of suggested stock data.
    :return: JSON response with suggested stock data for frontend.
    """
    # Example of suggested stock symbols
    suggested_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    response_data = []

    for symbol in suggested_stocks:
        stock_info = fetch_stock_data(symbol)
        if "error" in stock_info:
            response_data.append({"symbol": symbol, "error": stock_info["error"]})
        else:
            response_data.append({
                "symbol": symbol,
                "price": stock_info.get("price"),
                "pe_ratio": stock_info.get("pe_ratio")
            })

    return {"data": response_data}
