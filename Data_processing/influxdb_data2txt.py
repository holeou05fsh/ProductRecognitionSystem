# import influxdb_client
# from influxdb_client import InfluxDBClient
# from datetime import datetime

# # 配置
# token = "2xE_ttHl9rzs0p19VzPwFdnsbVMp-jZwi7W4SKNTyiZXWvmFOPPN-wD9ZpvrLKsKC4YxooBN4o949ZFC6a70PQ=="
# org_test = "org100"
# url = "http://localhost:9999"
# bucket_test = "bucket100"

# # 创建 InfluxDB 客户端
# client = InfluxDBClient(url=url, token=token, org=org_test)
# query_api = client.query_api()

# # 查询 unit_price 和 quantity 的平均值
# query = f'''
# from(bucket: "{bucket_test}")
#   |> range(start: -30d)
#   |> filter(fn: (r) => r["_measurement"] == "test01")
#   |> filter(fn: (r) => r["_field"] == "unit_price" or 
#                       r["_field"] == "quantity" or 
#                       r["_field"] == "commodity" or 
#                       r["_field"] == "Order_ID")
#   |> last()
#   |> yield(name: "mean")
# '''


# # 处理结果
# result = query_api.query(org=org_test, query=query)

# for table in result:
#     for record in table.records:
#         field_name = record['_field']
#         value = record.get_value()
#         timestamp = record.get_time()
#         dt = datetime.fromisoformat(str(timestamp))
#         timestamp = int(dt.timestamp() * 1_000_000_000)
#         print(field_name, value, timestamp)

# with open("output.txt", "w", encoding='utf-8') as file:
#     if result:
#         for table in result:
#             for record in table.records:
#                 field_name = record['_field']
#                 value = record.get_value()
#                 timestamp = record.get_time()
#                 # 写入数据到文件
#                 file.write(f"Field: {field_name}, Value: {value}, Time: {timestamp.isoformat()}\n")
#                 # print(value)
#         print("成功")      
#     else:
#         file.write("没有查询到结果。\n")

# # 关闭客户端
# client.close()




# ====================要用2csv檔 未用====================


# import csv
# import influxdb_client
# from influxdb_client import InfluxDBClient
# from datetime import datetime

# # 配置
# token = "2xE_ttHl9rzs0p19VzPwFdnsbVMp-jZwi7W4SKNTyiZXWvmFOPPN-wD9ZpvrLKsKC4YxooBN4o949ZFC6a70PQ=="
# org_test = "org100"
# url = "http://localhost:9999"
# bucket_test = "bucket100"

# # 创建 InfluxDB 客户端
# client = InfluxDBClient(url=url, token=token, org=org_test)
# query_api = client.query_api()

# # 查询 unit_price 和 quantity 的平均值
# query = f'''
# from(bucket: "{bucket_test}")
#   |> range(start: -30d)
#   |> filter(fn: (r) => r["_measurement"] == "test01")
#   |> filter(fn: (r) => r["_field"] == "unit_price" or 
#                       r["_field"] == "quantity" or 
#                       r["_field"] == "commodity" or 
#                       r["_field"] == "Order_ID")
#   |> last()
#   |> yield(name: "mean")
# '''

# # 处理结果
# result = query_api.query(org=org_test, query=query)

# # CSV 文件名
# csv_filename = "influxdb_data.csv"

# # 检查是否有结果
# if result:
#     # 打开CSV文件用于写入
#     with open(csv_filename, "w", newline='', encoding='utf-8') as csvfile:
#         # 定义CSV的字段名
#         fieldnames = ['Order_ID', 'commodity', 'unit_price', 'quantity', 'Time']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#         # 写入CSV的表头
#         writer.writeheader()

#         # 用来存储每个字段的值
#         record_data = {'Order_ID': None, 'commodity': None, 'unit_price': None, 'quantity': None, 'Time': None}

#         # 遍历结果并写入CSV
#         for table in result:
#             for record in table.records:
#                 field_name = record['_field']
#                 value = record.get_value()
#                 timestamp = record.get_time()
#                 dt = datetime.fromisoformat(str(timestamp))
#                 nanoseconds = int(dt.timestamp() * 1_000_000_000)
                
#                 # 根据字段名填充记录
#                 if field_name == "Order_ID":
#                     record_data['Order_ID'] = value
#                 elif field_name == "commodity":
#                     record_data['commodity'] = value
#                 elif field_name == "unit_price":
#                     record_data['unit_price'] = value
#                 elif field_name == "quantity":
#                     record_data['quantity'] = value

#                 # 更新时间戳
#                 record_data['Time'] = nanoseconds

#             # 写入数据到CSV文件
#             writer.writerow(record_data)

#         print("数据成功写入", csv_filename)
# else:
#     print("没有查询到结果。")
