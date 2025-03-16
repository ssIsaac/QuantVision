# Code for cleaning and preparing your data (e.g., adding lag features)
import pandas as pda 
from sklearn.model_selection import train_test_split

def add_lag_features(df, column='c', lags=[1,2,3]):
    """
    Add lag features (previous closing prices) to the dataset.
    """
    for lag in lags:
        df[f"{column}_Lag{lag}"] = df[column].shift(lag)
    df.dropna(inplace=True)
    return df

def pre_processData(df):
    """
    Preprocess stock data by converting timestamps and adding lag add_lag_features
    """
    df['t'] = pda.to_datetime(df['t'], unit='ms')
    df = add_lag_features(df, column='c', lags=[1,2,3])
    df.reset_index(drop=True, inplace=True)

    features = ["c_Lag1", "c_Lag2", "c_Lag3"]
    X = df[features] # create a new dataframe X with features
    y = df['c'] # Target variable (closing price)

    # Split data: training (90%), testings (10%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.9, shuffle=False) #Ensures that data remains in chronological order (important for time-series forecasting)

    return X_train, X_test, y_train, y_test


def predict_future_price(model, last_known_data, lags=[1,2,3]):
    """
    Predict the closing price for a future date using past closing prices.

    Parameters:
        model: Trained machine learning model
        last_known_data (pd.DataFrame): Latest available stock data (with lag features)
        lags (list): List of lag days used in training

    Returns:
        float: Predicted closing price for the next time step
    """
    # Extract last available values for each lag freature 
    future_features = {}
    lag_values = {}
    for lag in lags:
        lag_values[f"c_Lag{lag}"] = last_known_data.iloc[-lag]["c"]
        future_features[f"c_Lag{lag}"] = lag_values[f"c_Lag{lag}"]

    # Convert dictionary to DataFrame for model input
    future_df = pda.DataFrame([future_features])

    # Predict the next closing price 
    predicted_price = model.predict(future_df)[0]
    

    return predicted_price, lag_values