# Code for cleaning and preparing your data (e.g., adding lag features)
import pandas as pda 

def add_lag_features(df, column='c', lags=[1,2,3]):
    """
    Add lag features (previous closing prices) to the dataset.
    """
    for lag in lags:
        df[f"{column}_Lag{lag}"] = df[column].shift(lag)
    df.dropna(inplace=True)
    return df