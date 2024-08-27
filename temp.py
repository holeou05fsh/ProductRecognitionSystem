import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import random
    

def on_button_click():
    # pass

    token = "2xE_ttHl9rzs0p19VzPwFdnsbVMp-jZwi7W4SKNTyiZXWvmFOPPN-wD9ZpvrLKsKC4YxooBN4o949ZFC6a70PQ==" #os.environ.get("INFLUXDB_TOKEN")
    org_test = "org100"
    url = "http://localhost:9999"
    bucket_test = "bucket100"
    
    
    write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org_test)
    write_api = write_client.write_api(write_options=SYNCHRONOUS)

    Order_ID = random.randint(10, 100)
    commodity = f"commodity_{random.randint(1, 10)}"
    unit_price = round(random.uniform(1.0, 100.0), 2)
    print(Order_ID, commodity, unit_price)
    
    # 生成數據點並寫入資料庫
    record_test = (
        Point("shop_measurement01")
        .tag("shop_tag01", "tagvalue1")  # 使用tag來進行分類（例如商店名稱或地點）
        .field("Order_ID", Order_ID)      # 訂單編號
        .field("commodity", commodity)    # 商品名稱
        .field("unit_price", unit_price)  # 單價
        .time(time.time_ns(), WritePrecision.NS)  # 設定當前時間為納秒精度
    )
    write_api.write(bucket=bucket_test, org=org_test, record=record_test)
    time.sleep(1)

# on_button_click()


# from influxdb_client import InfluxDBClient

# # 创建 InfluxDB 客户端
# token = "2xE_ttHl9rzs0p19VzPwFdnsbVMp-jZwi7W4SKNTyiZXWvmFOPPN-wD9ZpvrLKsKC4YxooBN4o949ZFC6a70PQ==" #os.environ.get("INFLUXDB_TOKEN")
# org_test = "org100"
# url = "http://localhost:9999"
# bucket_test = "bucket100"
# client = InfluxDBClient(url=url, token=token, org=org_test)
# print(token)
# # 测试连接
# try:
#     health = client.health()
#     print(f"InfluxDB health status: {health.status}")
# except Exception as e:
#     print(f"Error: {e}")
# from influxdb_client import InfluxDBClient, Point, Dialect
# from influxdb_client.client.query_api import QueryApi
# import os

# 读取环境变量
token = "2xE_ttHl9rzs0p19VzPwFdnsbVMp-jZwi7W4SKNTyiZXWvmFOPPN-wD9ZpvrLKsKC4YxooBN4o949ZFC6a70PQ==" #os.environ.get("INFLUXDB_TOKEN")
org_test = "org100"
url = "http://localhost:9999"
bucket_test = "bucket100"

# 创建 InfluxDB 客户端
client = InfluxDBClient(url=url, token=token, org=org_test)
query_api = client.query_api()


# 创建 InfluxDB 客户端
client = InfluxDBClient(url=url, token=token, org=org_test)
query_api = client.query_api()

# 查询 Order_ID 数据
query = f'''
from(bucket: "{bucket_test}")
  |> range(start: -1d)  // 查询过去一天的数据，调整为适当的时间范围
  |> filter(fn: (r) => r["_measurement"] == "shop_measurement01")  // 根据实际 measurement 替换
  |> filter(fn: (r) => r["shop_tag01"] == "tagvalue1")  // 根据实际 tag 替换
  |> filter(fn: (r) => r["_field"] == "Order_ID")  // 过滤字段
'''

# 执行查询
result = query_api.query(org=org_test, query=query)

# 处理结果
for table in result:
    for record in table.records:
        print(f"Order_ID: {record.get_value()}")

# 关闭客户端
client.close()