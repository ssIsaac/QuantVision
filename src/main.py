# The main script to run the full pipeline
"""Main module."""
import data_collection as dc
import data_preprocessing as dp
import models 
import os 
from dotenv import load_dotenv
import visualisation as vi


env_path = os.path.join(os.path.dirname(__file__), "..","stock_env", ".env")
load_dotenv(env_path)
api_key = os.getenv("API_key")

if __name__ == "__main__":

    

    print("running")
    if not api_key:
        print(f"Error: API key not found")
        exit()
    else:
        print(f"api key obtained {api_key}")
    

    # ticker = input("Enter stock ticker (e.g., AAPL): ").strip().upper()
    # multiplier = input("Enter multiplier (e.g., 1): ").strip()
    # timespan = input("Enter timespan (e.g., day, hour, minute): ").strip().lower()
    # from_date = input("Enter start date (YYYY-MM-DD): ").strip()
    # to_date = input("Enter end date (YYYY-MM-DD): ").strip()

    ticker = "HIMS"
    multiplier = "1"
    timespan = "day"
    from_date = "2025-01-01"
    to_date = "2025-03-14"


    ## Fetch stock data
    try:
        multiplier = int(multiplier)
    except ValueError:
        print("Error, multiplier must be an integer value")
        exit()

    try:
        data = dc.fetch_stock_data(api_key, ticker, multiplier, timespan, from_date, to_date)
        root_dir = os.path.join(os.path.dirname(__file__),"..")
        data_dir = os.path.join(os.path.join(root_dir,"data"))

        if not os.path.exists("data_dir"):
            os.makedirs("data_dir")
        filename = os.path.join(data_dir, f"{ticker}_{from_date}_to_{to_date}.csv")
        data.to_csv(filename, index=False)
        print(f"data saved to {filename}")
    except Exception as e:
        print(f"Error fetching stock data: {e}")


    ## Preprocess data(convert timestamp, add lag features, split data into training & testing)
    X_train, X_test, y_train, y_test = dp.pre_processData(data)

    ## Train model 
    model = models.train_models(X_train, y_train)

    ## Evaluate model 
    mse, predictions = models.evaluate_model(model, X_test, y_test)
    print(f"Model MSE: {mse:.2f}")

    # Save prediction 
    data.loc[X_test.index, 'Predicted Close'] = predictions ## Only save predictions of rows of X that are assigned as test data 
    filename = os.path.join(data_dir, f"{ticker}_{from_date}_to_{to_date}.csv")
    data[['t','c','Predicted Close']].to_csv(filename, index=False)
    print(f"Predictions{filename} saved")

    # Display visualisation
    # print("Available columns:", data.columns)
    vi.plot_predictions(ticker,y_test, predictions, data.loc[X_test.index, 't'])
