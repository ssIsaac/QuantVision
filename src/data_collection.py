# Folder to store raw or processed data (e.g., CSV files)
import requests
import pandas as pda
import os 
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("API_key")

def fetch_stock_data(API_key, ticker, multipler, timespan, from_date, to_date):
    string_query = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multipler}/{timespan}/{from_date}/{to_date}?apiKey={API_key}"

    response = requests.get(string_query)

    if response.status_code == 200:
        data = response.json()
        df = pda.DataFrame(data.get('results',[]))
        return df
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")
    
if __name__ == "__main__":
    if not api_key:
        print(f"Error: API key not found")
    
    ticker = input("Please enter ticker symbol: ").strip().upper()
    multiplier = input("Please enter multipler value: ").strip()
    timespan = input("Please enter timespan value: ").strip().lower()
    from_date = input("Please enter starting time value: ").strip()
    to_date = input("Please enter end time value: ").strip()

    # ticker = input("Enter stock ticker (e.g., AAPL): ").strip().upper()
    # multiplier = input("Enter multiplier (e.g., 1): ").strip()
    # timespan = input("Enter timespan (e.g., day, hour, minute): ").strip().lower()
    # from_date = input("Enter start date (YYYY-MM-DD): ").strip()
    # to_date = input("Enter end date (YYYY-MM-DD): ").strip()

    # ticker = 'AAPL'
    # multiplier = 1
    # timespan = 'day'
    # from_date = '2024-01-01'
    # to_date = '2024-01-31'

    
    try:
        multiplier = int(multiplier)
    except ValueError:
        print("Error, multiplier must be an integer value")
        exit()

    data = fetch_stock_data(api_key, ticker, multiplier, timespan, from_date, to_date)

    filename = f"data/{ticker}_{from_date}_to_{to_date}.csv"
    data.to_csv(filename, index=False)
    print(f"data saved to {filename}")