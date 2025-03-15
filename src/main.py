# The main script to run the full pipeline
"""Main module."""
import data_collection as dc
import data_preprocessing as dp
import models 
import os 

def main():

    if not api_key:
        print(f"Error: API key not found")
    else:
        api_key = os.getenv("API_key")
    

    ticker = input("Enter stock ticker (e.g., AAPL): ").strip().upper()
    multiplier = input("Enter multiplier (e.g., 1): ").strip()
    timespan = input("Enter timespan (e.g., day, hour, minute): ").strip().lower()
    from_date = input("Enter start date (YYYY-MM-DD): ").strip()
    to_date = input("Enter end date (YYYY-MM-DD): ").strip()


    ## Fetch stock data
    try:
        multiplier = int(multiplier)
    except ValueError:
        print("Error, multiplier must be an integer value")
        exit()

    try:
        data = dc.fetch_stock_data(api_key, ticker, multiplier, timespan, from_date, to_date)
        if not os.path.exists("data"):
            os.makedirs("data")
        filename = f"data/{ticker}_{from_date}_to_{to_date}.csv"
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
    filename = f"data/{ticker}_predictions.csv"
    data[['t','c','Predicted_Close']].to_csv(filename, index=False)

    print(f"Predictions{filename} saved")
