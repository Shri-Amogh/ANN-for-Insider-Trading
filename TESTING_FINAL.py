import pandas as pd
import numpy as np
import os
import pickle
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model









def Test_From_data():
    # File paths
    model_path = 'Model/insider_trading_model.h5'
    scaler_path = 'Model/scaler.pkl'

    # Load the new data files
    new_email_features = pd.read_csv('New_Emails.csv', encoding='ISO-8859-1')
    new_text_features = pd.read_csv('New_Text.csv', encoding='ISO-8859-1')
    new_call_features = pd.read_csv('New_Call.csv', encoding='ISO-8859-1')
    new_badge_features = pd.read_csv('New_Badge.csv', encoding='ISO-8859-1')
    new_file_features = pd.read_csv('New_Files.csv', encoding='ISO-8859-1')
    df_trades = pd.read_csv('Trade_Logs.csv', encoding='ISO-8859-1')

    # Preprocessing function (as previously defined)
    def preprocess(df, time_column, user_column, prefix):
        df[time_column] = pd.to_datetime(df[time_column])
        features = df.groupby(user_column).agg({
            time_column: ['count', lambda x: (x.max() - x.min()).total_seconds()]  # number of events, activity spread
        })
        features.columns = [f'{prefix}_count', f'{prefix}_activity_duration']
        return features

    # Extract features (as previously done)
    email_features = preprocess(new_email_features, 'Timestamp', 'Sender', 'email')
    text_features = preprocess(new_text_features, 'Timestamp', 'Sender Number', 'text')
    call_features = preprocess(new_call_features, 'Timestamp', 'Caller Number', 'call')
    badge_features = preprocess(new_badge_features, 'timestamp', 'user_id', 'badge')
    file_features = preprocess(new_file_features, 'timestamp', 'user_id', 'file')

    # Trade features
    trade_features = df_trades.groupby('Ticker').agg({
        'Volume': 'sum'
    })

    # Combine all features
    features = email_features.join(text_features, how='outer')\
                            .join(call_features, how='outer')\
                            .join(badge_features, how='outer')\
                            .join(file_features, how='outer')\
                            .join(trade_features, how='outer')

    features = features.fillna(0)

    # Ensure 'Volume' column is numeric (ignore errors if non-numeric values are present)
    features['Volume'] = pd.to_numeric(features['Volume'], errors='coerce')

    # Create labels (Assume large profit/loss means suspicious activity)
    features['label'] = (features['Volume'] > 100000).astype(int)  # example condition for suspicious activity

    # Define X (features) and y (labels)
    X = features.drop(columns=['label'])
    y = features['label']

    # Load pre-trained model and scaler
    if os.path.exists(model_path) and os.path.exists(scaler_path):
        # Load pre-trained model and scaler
        from tensorflow.keras.models import load_model
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        
        model = load_model(model_path)

        # Preprocess the data (scale it)
        X_scaled = scaler.transform(X)

        # Make predictions
        y_pred = model.predict(X_scaled)
        y_pred_classes = (y_pred > 0.000031).astype(int)

        # Flatten y_pred_classes to 1D if it's 2D
        y_pred_classes = y_pred_classes.flatten()

        # Filter suspicious activity predictions (label = 1)
        suspicious_activity = features[y_pred_classes == 1]

        # Generate explanations for suspicious activities
        explanations = []
        for idx, row in suspicious_activity.iterrows():
            explanation = ""
            if row['email_count'] > 15:
                explanation += f" High email activity at unusual times and unusual subjects{idx}({row['email_count']} emails)."
            if row['text_count'] > 27:
                explanation += f" Frequent text messages near Market time {idx}({row['text_count']} texts)."
            if row['call_count'] > 10:
                explanation += f" High call frequency near Market time {idx}({row['call_count']} calls)."
            if row['badge_count'] > 7:
                explanation += f" High badge swipe activity Before / During Market time{idx}({row['badge_count']} badge swipes)."
            if row['file_count'] > 7:
                explanation += f" Excessive file access {idx}({row['file_count']} files accessed)."
            if row['Volume'] > 10000:
                explanation += f" Extremely high trading volume {idx}({row['Volume']})."
            
            if explanation == "":
                continue
            else:
                explanations.append(explanation)

        # Output suspicious activity and explanations
        print(f"Total Suspicious Activities: {len(explanations)}")
        string = ""
        for explanation in explanations:
            string  += explanation + "\n"
        return (string)

    else:
        return ("Model or scaler not found. Please ensure they are saved in the correct paths.")
