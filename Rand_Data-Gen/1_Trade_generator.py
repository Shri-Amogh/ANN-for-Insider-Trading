import yfinance as yf
import pandas as pd
from yahoo_fin import stock_info as si
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to fetch stock data for one ticker
def fetch_single_ticker(ticker, start_date, end_date):
    try:
        # Download stock data
        stock_data = yf.download(ticker, start=start_date, end=end_date, progress=False)

        if stock_data.empty:
            print(f"⚠️ No data for {ticker}")
            return None

        # Reset index to get Date as a column
        stock_data = stock_data.reset_index()

        # Fetch industry info
        try:
            info = si.get_quote_table(ticker)
            industry = info.get('Industry', 'Unknown')
        except Exception as e:
            print(f"⚠️ Error fetching industry for {ticker}: {e}")
            industry = 'Unknown'

        # Ensure 'Adj Close' exists
        if 'Adj Close' not in stock_data.columns:
            print(f"⚠️ No 'Adj Close' for {ticker}, using 'Close' instead.")
            stock_data['Adj Close'] = stock_data['Close']

        # Fill missing Open/High/Low/Close with Adj Close if NaN
        for col in ['Open', 'High', 'Low', 'Close']:
            if col in stock_data.columns:
                stock_data[col] = stock_data[col].fillna(stock_data['Adj Close'])
            else:
                # In case the column itself doesn't exist (edge case)
                stock_data[col] = stock_data['Adj Close']

        # Add Ticker and Industry columns
        stock_data['Ticker'] = ticker
        stock_data['Industry'] = industry

        # Reorder columns exactly as desired
        stock_data = stock_data[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Date', 'Ticker', 'Industry']]

        return stock_data

    except Exception as e:
        print(f"❌ Error processing {ticker}: {e}")
        return None

# Function to fetch data for all tickers using multithreading
def fetch_trade_data_parallel(tickers, start_date, end_date):
    all_data = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_ticker = {executor.submit(fetch_single_ticker, ticker, start_date, end_date): ticker for ticker in tickers}

        for future in as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            try:
                data = future.result()
                if data is not None:
                    all_data.append(data)
            except Exception as e:
                print(f"❌ Error processing {ticker}: {e}")

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        return pd.DataFrame()

# Function to save the data to a CSV file
def save_to_csv(data, filename):
    # Data is already in the correct order
    data.to_csv(filename, index=False)
    print(f"✅ Data saved to {filename}")

# List of major company tickers
tickers = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "NVDA", "META", "BRK.B", "V", "JPM",
           "UNH", "LLY", "XOM", "JNJ", "WMT", "MA", "PG", "CVX", "ORCL", "AVGO",
           "HD", "MRK", "ABBV", "COST", "PEP", "ADBE", "KO", "BAC", "PFE", "CRM",
           "NFLX", "TMO", "DIS", "AMD", "MCD", "LIN", "NKE", "VZ", "BMY", "WFC",
           "DHR", "ACN", "INTC", "TXN", "UPS", "CAT", "AMAT", "LOW", "SPGI", "NEE",
           "PM", "QCOM", "MS", "SCHW", "INTU", "IBM", "RTX", "NOW", "GE", "LMT",
           "ELV", "HON", "AMGN", "MDT", "GS", "BLK", "ISRG", "CVS", "T", "BKNG",
           "ADI", "REGN", "PGR", "DE", "SYK", "SBUX", "MMC", "MO", "ZTS", "C",
           "ADP", "PLD", "TGT", "CI", "MU", "FDX", "PANW", "VRTX", "USB", "ADSK",
           "CSCO", "GILD", "SO", "COP", "APD", "CHTR", "EQIX", "AON", "FISV", "CL",
           "PSX", "EOG", "HUM", "ROST", "KMB", "ETN"]

# Dates for fetching data
start_date = "2025-03-01"
end_date = "2025-04-01"

# Fetch data for all tickers
trade_data = fetch_trade_data_parallel(tickers, start_date, end_date)

# Save the data to a CSV file
if not trade_data.empty:
    save_to_csv(trade_data, 'Data/Trade_Logs.csv')
else:
    print("❌ No trade data to save.")
