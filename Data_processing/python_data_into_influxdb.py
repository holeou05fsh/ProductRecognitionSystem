from influxdb_client import InfluxDBClient, Point, WriteOptions, WritePrecision
import pandas as pd
from Data_processing._setting import set_connect
import time

influx_con = set_connect()

def data2influxdb(data):
    "一次寫入多筆"
    # 配置
    token = "2xE_ttHl9rzs0p19VzPwFdnsbVMp-jZwi7W4SKNTyiZXWvmFOPPN-wD9ZpvrLKsKC4YxooBN4o949ZFC6a70PQ=="
    token = influx_con.influxdb_token("custom")
    org = influx_con.influxdb_org
    url = influx_con.influxdb_url
    bucket = influx_con.influxdb_bucket
    
    # 初始化InfluxDB客戶端
    client = InfluxDBClient(url=url, token=token)
    
    # 初始化寫入API
    write_api = client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=10_000))
    
    
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
        print(Order_ID, commodity, unit_price, time_ns)

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
    
    # print(len(points))
    # 將所有數據點一次性寫入InfluxDB
    write_api.write(bucket=bucket, org=org, record=points)
    
    # 關閉客戶端
    client.close()
    
    print("多筆字段數據已成功寫入InfluxDB")



def data2influxdb_2(data):
    "一筆一筆寫入"

    # 配置
    token = influx_con.influxdb_token("custom")
    org = influx_con.influxdb_org
    url = influx_con.influxdb_url
    bucket = influx_con.influxdb_bucket
    
    # 初始化InfluxDB客戶端
    client = InfluxDBClient(url=url, token=token)
    
    # 初始化寫入API
    write_api = client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=10_000))
        
    # 遍历每一行数据并创建数据点
    for index, row in data.iterrows():
        # 从行中提取数据
        Order_ID = row['Order_ID']
        commodity = row['commodity']
        unit_price = float(row['unit_price'])  # 確保字段類型正確
        quantity = int(row['quantity'])  # 確保字段類型正確
        time_ns = pd.to_datetime(row['time']).to_pydatetime()  # 转换为 datetime 对象
        print(Order_ID, commodity, unit_price, quantity, time_ns)

        # 创建数据点
        point = Point("test02")\
            .tag("shop_tag", "tagvalue")\
            .field("Order_ID", Order_ID)\
            .field("commodity", commodity)\
            .field("unit_price", unit_price)\
            .field("quantity", quantity)\
            .time(time_ns, WritePrecision.NS)    # 设置为纳秒精度
    
        # 將所有數據點一次性寫入InfluxDB
        write_api.write(bucket=bucket, org=org, record=point)
        time.sleep(0.5)
    
    # 關閉客戶端
    client.close()
    
    print("已成功寫入InfluxDB")


if __name__ == "__main__":
    # 读取 CSV 文件
    csv_file_path = "output.csv"  # CSV 文件的路径
    data = pd.read_csv(csv_file_path)
    data2influxdb(data)