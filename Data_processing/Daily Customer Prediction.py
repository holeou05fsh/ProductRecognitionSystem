import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import EarlyStopping
from datetime import timedelta

# 讀取資料
file_path = 'output.csv'
data = pd.read_csv(file_path)

# 計算每個訂單的營業額
data['time'] = pd.to_datetime(data['time'], unit='ns')

# 計算每日來客數（每個Order_ID代表一個顧客）
daily_customers = data.groupby(data['time'].dt.date)['Order_ID'].nunique().reset_index()

# 正規化數據
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(daily_customers['Order_ID'].values.reshape(-1, 1))

def create_dataset(data, time_step=1):
    X, Y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i:(i + time_step), 0])
        Y.append(data[i + time_step, 0])
    print(f"Generated {len(X)} sequences.")
    return np.array(X), np.array(Y)

# 準備訓練資料
time_step = 5
X, Y = create_dataset(scaled_data, time_step)
X = X.reshape(X.shape[0], X.shape[1], 1)

# 建立 LSTM 模型
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(time_step, 1)))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dense(units=25))
model.add(Dense(units=1))

# 編譯模型
model.compile(optimizer='adam', loss='mean_squared_error')

# 訓練模型
model.fit(X, Y, batch_size=1, epochs=50)

# 保存模型到文件
model.save("Daily_Customer_Prediction.h5")

# 預測未來的來客數
future_steps = 7
last_days = scaled_data[-time_step:]
pred_input = last_days.reshape(1, time_step, 1)
predictions = []

for _ in range(future_steps):
    pred = model.predict(pred_input)
    predictions.append(pred[0, 0])
    # 將 pred 重塑為 (1, 1, 1) 的 3D 数组
    pred = pred.reshape(1, 1, 1)
    # 更新 pred_input 的數據
    pred_input = np.append(pred_input[:, 1:, :], pred, axis=1)

# 將預測結果轉換回原始範圍
predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

# 生成未來7天的日期範圍
future_dates = pd.date_range(start=daily_customers['time'].iloc[-1], periods=future_steps + 1, freq='D')[1:]

# 確定要顯示的日期範圍：最后两个月的数据
two_months_ago = daily_customers['time'].max() - timedelta(days=60)
recent_data = daily_customers[daily_customers['time'] >= two_months_ago]

# 繪製預測結果
plt.figure(figsize=(12, 6))
plt.plot(recent_data['time'], recent_data['Order_ID'], label='Actual Customers')
plt.plot(future_dates, predictions, label='Predicted Customers')
plt.title('Daily Customer Prediction (Last 2 Months and Next 7 Days)')
plt.xlabel('Date')
plt.ylabel('Number of Customers')
plt.legend()
plt.show()