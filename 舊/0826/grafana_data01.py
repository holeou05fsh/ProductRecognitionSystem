import influxdb_client
from influxdb_client import InfluxDBClient, Point, WriteOptions, WritePrecision
from datetime import datetime
import pytz
import pandas as pd

# file_path = 'output.csv'
# data = pd.read_csv(file_path)

# data['revenue'] = data['unit_price'] * data['quantity']
# data['time'] = pd.to_datetime(data['time'], unit='ns')

# # 計算每日來客數
# daily_customers = data.groupby(data['time'].dt.date).agg({'Order_ID': 'nunique'}).reset_index()
# daily_customers.columns = ['time', 'customer']
# # print(daily_customers)
# # print(type(daily_customers))

# # 計算每日收入
# daily_revenue = data.groupby(data['time'].dt.date).agg({'revenue': 'sum'}).reset_index()
# daily_revenue.columns = ['time', 'revenue']
# # print(daily_revenue)
# # print(type(daily_revenue))

# # 進行合併
# merged_data = pd.merge(daily_customers, daily_revenue, on='time', suffixes=('_customers', '_revenue'))
# # print(type(merged_data['time']))

# # 将 'time' 列转换为 datetime 对象
# merged_data['time'] = pd.to_datetime(merged_data['time'])

# # 日期為了可以寫入influxdb，將時間轉換為 Unix 時間戳（秒）
# merged_data['time'] = (merged_data['time'].astype('int64') // 10**9)
# # print(merged_data)

# # 配置
# token = "2xE_ttHl9rzs0p19VzPwFdnsbVMp-jZwi7W4SKNTyiZXWvmFOPPN-wD9ZpvrLKsKC4YxooBN4o949ZFC6a70PQ=="
token = "TQNvuqdPZzjcyhJ_DN_Umo3Wyl1nihAaDiXJ23ZK1Tvvl2ao0nzBN_AxyXLeTRUQYXwXf0MaZ2imMoKOcAAZ0g=="
org = "org100"
url = "http://localhost:9999"
bucket = "bucket100"

# 初始化InfluxDB客戶端
client = InfluxDBClient(url=url, token=token)

# 初始化寫入API
write_api = client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=10_000))


# # 用於批量存儲數據點
# points = []

# # 遍历每一行数据并创建数据点
# for index, row in merged_data.iterrows():
#     # 从行中提取数据
#     customer_count = row['customer']
#     revenue = row['revenue']
#     time_s = row['time']  # 转换为 datetime 对象

#     # 创建数据点
#     point = Point("grafana")\
#         .tag("shop_tag01", "tagvalue1")\
#         .field("customer", customer_count)\
#             .field("revenue", revenue)\
#         .time(time_s, WritePrecision.S)    # 设置为纳秒精度
#     # print(customer_count, revenue, time_s)
#     # 將數據點添加到列表
#     points.append(point)

# # 將所有數據點一次性寫入InfluxDB
# write_api.write(bucket=bucket, org=org, record=points)

# # 關閉客戶端
# client.close()

# print("多筆字段數據已成功寫入InfluxDB")

''' grafana
from(bucket: "bucket100")
  |> range(start: -30d)
  |> filter(fn: (r) =>
    r._measurement == "grafana" and
    r._field == "customer"
  )

from(bucket: "bucket100")
  |> range(start: -30d)
  |> filter(fn: (r) =>
    r._measurement == "grafana" and
    r._field == "revenue"
  )

gauge :
    Standard options:
        min: 20 (當日過期品)， max: 500 (庫存)
原萃綠茶 (當日銷量)
from(bucket: "bucket100")
  |> range(start: -30d)
  |> filter(fn: (r) =>
    r._measurement == "grafana" and
    r._field == "原萃綠茶"
  )
  |> last()

品客洋芋片
益生菌
肉骨湯麵
'''

# # 读取 CSV 文件
file_path = 'output.csv'
df = pd.read_csv(file_path)

# 将 'time' 列转换为日期时间格式
df['time'] = pd.to_datetime(df['time'])

# 提取日期部分
df['time'] = df['time'].dt.date

# 按商品和日期分组，并计算每日销量总和
data = df.groupby(['time', 'commodity'])['quantity'].sum().reset_index()


# 将 'time' 列转换为 datetime 对象
data['time'] = pd.to_datetime(data['time'])

# 日期為了可以寫入influxdb，將時間轉換為 Unix 時間戳（秒）
data['time'] = (data['time'].astype('int64') // 10**9)
# print(merged_data)


# 使用 pivot 方法进行数据透视
data = data.pivot(index='time', columns='commodity', values='quantity')

# 可选：填充缺失值为 0
data = data.fillna(0)

# 将列名恢复为普通列
data.reset_index(inplace=True)

# 显示结果
print(data)

# 用於批量存儲數據點
points = []

# 遍历每一行数据并创建数据点
for index, row in data.iterrows():
    # 从行中提取数据
    item1 = row['原萃綠茶']
    item2 = row['品客洋芋片']
    item3 = row['益生菌']
    item4 = row['肉骨湯麵']
    time_s = row['time']  # 转换为 datetime 对象

    # 创建数据点
    point = Point("grafana")\
        .tag("shop_tag01", "tagvalue1")\
        .field("原萃綠茶", item1)\
        .field("品客洋芋片", item2)\
        .field("益生菌", item3)\
        .field("肉骨湯麵", item4)\
        .time(time_s, WritePrecision.S)    # 设置为纳秒精度
    # print(customer_count, revenue, time_s)
    # 將數據點添加到列表
    points.append(point)

# 將所有數據點一次性寫入InfluxDB
write_api.write(bucket=bucket, org=org, record=points)

# 關閉客戶端
client.close()

print("多筆字段數據已成功寫入InfluxDB")