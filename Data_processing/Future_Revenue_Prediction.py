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
data['revenue'] = data['unit_price'] * data['quantity']
# print(data['revenue'][:20])
# 將時間戳轉換為 datetime 格式
data['time'] = pd.to_datetime(data['time'], unit='ns')
# print(data['time'][:20])

# 按天匯總營業額
daily_revenue = data.groupby(data['time'].dt.date)['revenue'].sum().reset_index()
# print(daily_revenue)
# print("=======daily_revenue======")
# 正規化數據
scaler = MinMaxScaler(feature_range=(0, 1))

scaled_data = scaler.fit_transform(daily_revenue['revenue'].values.reshape(-1, 1))
# print(scaled_data)
# print("=======scaled_data======")
# 準備訓練資料
def create_dataset(data, time_step=1):
    X, Y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i:(i + time_step), 0])
        Y.append(data[i + time_step, 0])
    print(f"Generated {len(X)} sequences.")
    return np.array(X), np.array(Y)

time_step = 20
X, Y = create_dataset(scaled_data, time_step)
print(f"Shape of X: {X.shape}")
print(f"Shape of Y: {Y.shape}")
# print(X)

if X.size == 0 or Y.size == 0:
    raise ValueError("Insufficient data to generate sequences. Consider reducing the time_step.")

X = X.reshape(X.shape[0], X.shape[1], 1)
# print(X)
# print("=======X======")
# 建立 LSTM 模型
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(time_step, 1)))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dense(units=25))
model.add(Dense(units=1))

# 編譯模型
model.compile(optimizer='adam', loss='mean_squared_error')

# 訓練模型
model.fit(X, Y, batch_size=1, epochs=40)

# 保存模型到文件
model.save("revenue_prediction_model.h5")

# 从文件加载模型
model = tf.keras.models.load_model("revenue_prediction_model.h5")

# # 預測未來的營業額
future_steps = 7
last_days = scaled_data[-time_step:]
# print(last_days)
# print("=======last_days======")
pred_input = last_days.reshape(1, time_step, 1)
# print("=======pred_input======")
predictions = []

for _ in range(future_steps):
    pred = model.predict(pred_input)
    predictions.append(pred[0, 0])
    # 重塑 pred 以匹配 pred_input 的尺寸
    pred = pred.reshape(1, 1, 1)
    pred_input = np.append(pred_input[:, 1:, :], pred, axis=1)
# print(pred_input)
print("=======pred_input======")
# print(predictions)
print("=======predictions======")
# 將預測結果轉換回原始範圍
predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

# # 使用pandas.date_range生成日期范围，移除closed参数
future_dates = pd.date_range(start=daily_revenue['time'].iloc[-1], periods=future_steps + 1, freq='D')[1:]

# # 繪製預測結果
plt.plot(daily_revenue['time'], daily_revenue['revenue'], label='Actual Revenue')
plt.plot(future_dates, predictions, label='Predicted Revenue')
plt.title('Future Revenue Prediction (LSTM Model)')
plt.xlabel('Date')
plt.ylabel('Revenue')
plt.legend()
plt.show()



