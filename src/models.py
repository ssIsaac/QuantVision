# Code for building, training, and evaluating your model
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def train_models(X_train, y_train):
    """"
    train a Linear Regression model on historical stock data "
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model 

def evaluate_model (model, X_test, y_test):
    """"
    Evaluate model performance using mean squared error"
    """

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    return mse, predictions

    
