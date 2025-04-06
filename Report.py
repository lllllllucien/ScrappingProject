import pandas as pd


def today_filter(df : pd.DataFrame) -> pd.Series:
    today = pd.Timestamp.today().date()
    price = df[df.index.date == today]["lastPr"]
    return price

def metrics(price : pd.Series) -> dict:

    open = price.iloc[0]
    low = price.min()
    high = price.max()
    last = price.iloc[-1]

    variation = ((last - open) / last) * 100
    volatility = price.std()

    res = {
        "Date" : pd.Timestamp.today().strftime("%Y-%m-%d"),
        "Open" : round(open, 2),
        "High" : round(high, 2),
        "Low" : round(low, 2),
        "Current Price" : round(last, 2),
        "Variation" : round(variation, 2),
        "Volatility" : round(volatility, 2)
    }

    return res


def get_report(file_name = "data.csv") :

    df = pd.read_csv(file_name, index_col=0, parse_dates=True)

    price = today_filter(df)

    report = metrics(price)

    return report


if __name__ == "__main__":


    pass