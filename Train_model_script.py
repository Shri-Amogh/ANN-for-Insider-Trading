import pandas as pd
import numpy as np
import os
import pickle
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping


model_path = 'Model/insider_trading_model.h5'
scaler_path = 'Model/scaler.pkl'


df_emails = pd.read_csv('Data/Emails_Logs_Week.csv', encoding='ISO-8859-1')
df_texts = pd.read_csv('Data/Text_Logs_Week.csv', encoding='ISO-8859-1')
df_calls = pd.read_csv('Data/Call_Logs_Week.csv', encoding='ISO-8859-1')
df_badges = pd.read_csv('Data/Swipe_Logs_week.csv', encoding='ISO-8859-1')
df_files = pd.read_csv('Data/FIle_Logs_Week.csv', encoding='ISO-8859-1')
df_trades = pd.read_csv('Trade_Logs.csv', encoding='ISO-8859-1')

def preprocess(df, time_column, user_column, prefix):
    df[time_column] = pd.to_datetime(df[time_column])
    features = df.groupby(user_column).agg({
        time_column: ['count', lambda x: (x.max() - x.min()).total_seconds()]  # number of events, activity spread
    })
    features.columns = [f'{prefix}_count', f'{prefix}_activity_duration']
    return features


email_features = preprocess(df_emails, 'Timestamp', 'Sender', 'email')
text_features = preprocess(df_texts, 'Timestamp', 'Sender Number', 'text')
call_features = preprocess(df_calls, 'Timestamp', 'Caller Number', 'call')
badge_features = preprocess(df_badges, 'timestamp', 'user_id', 'badge')
file_features = preprocess(df_files, 'timestamp', 'user_id', 'file')


trade_features = df_trades.groupby('Ticker').agg({
    'Volume': 'sum'
})


features = email_features.join(text_features, how='outer')\
                        .join(call_features, how='outer')\
                        .join(badge_features, how='outer')\
                        .join(file_features, how='outer')\
                        .join(trade_features, how='outer')

features = features.fillna(0)

features['Volume'] = pd.to_numeric(features['Volume'], errors='coerce')

features['label'] = (features['Volume'] > 100000).astype(int)  


X = features.drop(columns=['label'])
y = features['label']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)


model = Sequential()
model.add(Dense(128, input_dim=X_train.shape[1], activation='relu'))
model.add(Dropout(0.4))
model.add(BatchNormalization())
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(1, activation='sigmoid'))


model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.0005), metrics=['accuracy'])


early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)


model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2, callbacks=[early_stopping])


model.save(model_path)
with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)


loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy * 100:.2f}%")


y_pred = model.predict(X_test)
y_pred_classes = (y_pred > 0.5).astype(int)
print("Predictions:", y_pred_classes)
