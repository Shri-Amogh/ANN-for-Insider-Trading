import pandas as pd


def shift_row_values(row):

    open_col = 'Open'
    high_col = 'High'
    low_col = 'Low'
    close_col = 'Close'
    volume_col = 'Volume'


    price_columns = [open_col, high_col, low_col, close_col, volume_col]

    values = row.tolist()

    shifted = [None] * len(values)
    
    for i, value in enumerate(values):
        if pd.notna(value):  
            if not shifted[0]:  
                shifted[0] = value
            elif not shifted[1]:  
                shifted[1] = value
            elif not shifted[2]: 
                shifted[2] = value
            elif not shifted[3]: 
                shifted[3] = value
            elif not shifted[4]: 
                shifted[4] = value
            else:
                shifted.append(value)  
    

    shifted_row = {price_columns[i]: shifted[i] for i in range(5)}
    
  
    shifted_row['Date'] = row['Date']
    shifted_row['Ticker'] = row['Ticker']
    shifted_row['Industry'] = row['Industry']
    
    return pd.Series(shifted_row)


df = pd.read_csv("Data/Trade_Logs.csv")

df_cleaned = df.apply(shift_row_values, axis=1)

relevant_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Date', 'Ticker', 'Industry']


df_cleaned = df_cleaned[relevant_columns]


df_cleaned.to_csv('Data/Trade_Logs.csv', index=False)

print("Data has been successfully cleaned and saved to 'Trade_Logs.csv'.")
