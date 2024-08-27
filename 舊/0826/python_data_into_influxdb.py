import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WriteOptions, WritePrecision
from datetime import datetime
import pandas as pd

def data2influxdb(data):
    # 配置
    token = "2xE_ttHl9rzs0p19VzPwFdnsbVMp-jZwi7W4SKNTyiZXWvmFOPPN-wD9ZpvrLKsKC4YxooBN4o949ZFC6a70PQ=="
    org = "org100"
    url = "http://localhost:9999"
    bucket = "bucket100"
    
    # 初始化InfluxDB客戶端
    client = InfluxDBClient(url=url, token=token)
    
    # 初始化寫入API
    write_api = client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=10_000))
    
    # 读取 CSV 文件
    # csv_file_path = "output.csv"  # CSV 文件的路径
    # data = pd.read_csv(csv_file_path)
    
    # 用於批量存儲數據點
    points = []
    
    # 遍历每一行数据并创建数据点
    for index, row in data.iterrows():
        # 从行中提取数据
        Order_ID = row['Order_ID']
        commodity = row['commodity']
        unit_price = float(row['unit_price'])  # 確保字段類型正確
        quantity = int(row['quantity'])  # 確保字段類型正確
        time_ns = pd.to_datetime(row['time']).to_pydatetime()  # 转换为 datetime 对象
    
        # 创建数据点
        point = Point("test01")\
            .tag("shop_tag04", "tagvalue4")\
            .field("Order_ID", Order_ID)\
            .field("commodity", commodity)\
            .field("unit_price", unit_price)\
            .field("quantity", quantity)\
            .time(time_ns, WritePrecision.NS)    # 设置为纳秒精度
    
        # 將數據點添加到列表
        points.append(point)
    
    # 將所有數據點一次性寫入InfluxDB
    write_api.write(bucket=bucket, org=org, record=points)
    
    # 關閉客戶端
    client.close()
    
    print("多筆字段數據已成功寫入InfluxDB")
