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

def pre_processData(dt):
    """
    Preprocess stock data by converting timestamps and adding lag add_lag_features
    """
    df['t'] = pda.to_datetime(df['t'], unit='ms')
    df = add_lag_features(df, column=c, lags=[1,2,3])

    features = ["c_Lag1", "c_Lag2", "c_Lag3"]
    X = df(features) # create a new dataframe X with features
    y = df['c'] # Target variable (closing price)

    # Split data: training (80%), testings (20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, shuffle=False) #Ensures that data remains in chronological order (important for time-series forecasting)

    return X_train, X_test, y_train, y_test