import matplotlib.pyplot as plt

def plot_predictions(tickr, actual, predicted, dates):
    """Plot actual vs. predicted stock prices"""
    plt.figure(figsize=(10,5))
    plt.plot(dates, actual, label="Actual Price", color="blue")
    plt.plot(dates, predicted, label="Predicted Price", color="red", linestyle="dashed")
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.title(f"Stock Price Prediction for {tickr}")
    plt.legend()
    plt.show()