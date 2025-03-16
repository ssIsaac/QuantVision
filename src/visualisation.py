import matplotlib.pyplot as plt

def plot_predictions(tickr, actual, predicted, dates, future_date=None, future_price=None):
    """Plot actual vs. predicted stock prices"""
    plt.figure(figsize=(10,5))
    plt.plot(dates, actual, label="Actual Price", color="blue")
    plt.plot(dates, predicted, label="Predicted Price", color="red", linestyle="dashed")
    if future_date is not None and future_price is not None:
        plt.scatter(future_date, future_price, color="green", marker="x")

    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.title(f"Stock Price Prediction for {tickr}")
    plt.legend()
    plt.grid()
    plt.show()