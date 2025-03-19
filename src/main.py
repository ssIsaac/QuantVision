# The main script to run the full pipeline
"""Main module."""
import pandas as pda
import numpy as np
import data_collection as dc
import data_preprocessing as dp
import models 
import os 
from dotenv import load_dotenv
import visualisation as vi
import data_storage as ds


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
    to_date = "2025-03-18"


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

    # Save prediction locally
    data.loc[X_test.index, 'Predicted Close'] = predictions ## Only save predictions of rows of X that are assigned as test data 
    filename = os.path.join(data_dir, f"{ticker}_{from_date}_to_{to_date}.csv")
    data[['t','c','Predicted Close']].to_csv(filename, index=False)
    print(f"Predictions{filename} saved")

    # Save prediction to s3
    ds.upload_to_s3(filename, s3_key=f"datasets/{ticker}_predictions.csv")


################################################################

    ## Predict future prices
    future_price, lag_values = dp.predict_future_price(model, data)

    # Get the last date
    last_date = data["t"].iloc[-1]

    # Calculate next date
    next_date = last_date + pda.Timedelta(days=1)

    # Skip weekends
    if next_date.weekday() == 5:  # Saturday → Move to Monday
        next_date += pda.Timedelta(days=2)
    elif next_date.weekday() == 6:  # Sunday → Move to Monday
        next_date += pda.Timedelta(days=1)
    
    # Append new row into df
    new_row = pda.DataFrame({
        "t": [next_date],
        "c": [np.nan],
        "Predicted Close": [future_price],
        "c_Lag1": [lag_values["c_Lag1"]],
        "c_Lag2": [lag_values["c_Lag2"]],
        "c_Lag3": [lag_values["c_Lag3"]]
    })
    data = pda.concat([data, new_row], ignore_index=True)
    



###############



    test_dates = data.loc[data.index.intersection(X_test.index),'t']
    vi.plot_predictions(ticker,y_test, predictions, test_dates, future_date=next_date, future_price=future_price)
    # Display visualisation
    # print("Available columns:", data.columns)
    
