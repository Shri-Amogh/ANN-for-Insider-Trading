import pandas as pd

# Function to shift misplaced data to the correct position
def shift_row_values(row):
    # Identifying columns for Open, High, Low, Close, Volume
    open_col = 'Open'
    high_col = 'High'
    low_col = 'Low'
    close_col = 'Close'
    volume_col = 'Volume'

    # List of the expected columns to hold price-related data
    price_columns = [open_col, high_col, low_col, close_col, volume_col]
    
    # Convert the row into a list of values
    values = row.tolist()
    
    # Start shifting values from left to right if missing
    shifted = [None] * len(values)
    
    for i, value in enumerate(values):
        if pd.notna(value):  # If there's a valid value
            if not shifted[0]:  # If Open is not yet filled, assign to Open
                shifted[0] = value
            elif not shifted[1]:  # If High is not yet filled, assign to High
                shifted[1] = value
            elif not shifted[2]:  # If Low is not yet filled, assign to Low
                shifted[2] = value
            elif not shifted[3]:  # If Close is not yet filled, assign to Close
                shifted[3] = value
            elif not shifted[4]:  # If Volume is not yet filled, assign to Volume
                shifted[4] = value
            else:
                shifted.append(value)  # Any extra values are just appended
    
    # Convert the shifted list back to a row (dictionary)
    shifted_row = {price_columns[i]: shifted[i] for i in range(5)}
    
    # Also include Date, Ticker, and Industry if they are present in the row
    shifted_row['Date'] = row['Date']
    shifted_row['Ticker'] = row['Ticker']
    shifted_row['Industry'] = row['Industry']
    
    return pd.Series(shifted_row)

# Load the data from the CSV file
df = pd.read_csv("Data/Trade_Logs.csv")

# Apply the shift function to each row in the dataframe
df_cleaned = df.apply(shift_row_values, axis=1)

# Define relevant columns: Open, High, Low, Close, Volume, Date, Ticker, Industry
relevant_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Date', 'Ticker', 'Industry']

# Keep only relevant columns and drop rows with missing values
df_cleaned = df_cleaned[relevant_columns]

# Save the cleaned data to a new CSV file
df_cleaned.to_csv('Data/Trade_Logs.csv', index=False)

print("Data has been successfully cleaned and saved to 'Trade_Logs.csv'.")
