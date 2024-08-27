'''生成規則:
生成現在時間往前推一年，從一年到現在的時間點
以下時間段中來店的範圍隨機消費人數，返回值:Time (ns)，
隨機的銷售商品，數量則取1-20大多集中在1-6
最後轉成csv檔

      開始時間   結束時間  人數
    # 09:00:00, 12:00:00, 1-12
    # 12:01:00, 15:00:00, 10-25
    # 15:01:00, 18:00:00, 5-15
    # 18:01:00, 21:00:00, 1-25
'''

import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def generate_random_times(start_time, end_time, num_times):
    """在给定的时间范围内生成随机时间点。"""
    random_times = []
    for _ in range(num_times):
        random_seconds = random.randint(0, int((end_time - start_time).total_seconds()))
        random_time = start_time + timedelta(seconds=random_seconds)
        random_times.append(random_time)
    return random_times

def datetime_to_ns(dt):
    """将 datetime 对象转换为纳秒级时间戳。"""
    epoch = datetime(1970, 1, 1)
    delta = dt - epoch
    return int(delta.total_seconds() * 1e9)

def return_random_times_ns(days, time_ranges):
    """在指定的天数内生成随机时间点并打印，支持不同时间段和生成数量。"""
    current_date = datetime.now()
    now = current_date - relativedelta(years=1)
    one_week_later = now + timedelta(days=days)
    
    times = []
    
    # 遍历指定的天数中的每一天
    current_date = now.date()
    while current_date <= one_week_later.date():
        for start_hour, end_hour, num_times_range in time_ranges:
            start_time = datetime.combine(current_date, datetime.strptime(start_hour, "%H:%M:%S").time())
            end_time = datetime.combine(current_date, datetime.strptime(end_hour, "%H:%M:%S").time())
            
            if start_time > now:
                num_times_per_day = random.randint(*num_times_range)  # 随机生成数量
                # 在每天的时间范围内生成随机时间点
                daily_random_times = generate_random_times(start_time, end_time, num_times_per_day)
                times.extend(daily_random_times)
        
        current_date += timedelta(days=1)
    
    # 打印生成的时间点及其纳秒级时间戳
    time_ns_list = []
    for time_point in sorted(times):
        time_ns = datetime_to_ns(time_point)  # 获取时间点的纳秒级时间戳
        # print(f"{time_point.strftime('%Y-%m-%d %H:%M:%S')} | Time (ns): {time_ns}")
        time_ns_list.append(time_ns)
        
    return time_ns_list

# if __name__ == "__main__":
# 时间范围和生成数量设置
time_ranges = [
    ("09:00:00", "12:00:00", (1, 12)),
    ("12:01:00", "15:00:00", (10, 25)),
    ("15:01:00", "18:00:00", (5, 15)),
    ("18:01:00", "21:00:00", (1, 25))
]

days = 364 # 未来多少天364 

    
timelist = return_random_times_ns(days, time_ranges)

import csv



# 生成數據點並寫入資料庫
price = {'品客洋芋片': 60, '原萃綠茶': 39, '肉骨湯麵': 15, '益生菌': 150}
commoditylist = ['品客洋芋片', '原萃綠茶', '肉骨湯麵', '益生菌']

def weighted_random_int():
    # random int 1-20 但大多集中在 1-6
    # 定义权重
    weights = [10] * 6 + [1] * 14  # 1-6的权重较高，7-20的权重较低
    choices = list(range(1, 21))  # 1到20的数字
    return random.choices(choices, weights=weights, k=1)[0]

Order_ID = 1

data = [["Order_ID", "commodity", "unit_price", "quantity", "time"]]
for timens in timelist:
    loopnum = random.randint(2, 5)
    unique_num = random.sample(range(0, 4), 4)

    for j in range(1, loopnum):
        # print(unique_num[j])
        data_two = []
        commodity = commoditylist[unique_num[j-1]]
        
        data_two.append(Order_ID)# "Order_ID"
        data_two.append(commodity)# "commodity"
        data_two.append(price[commodity])# "unit_price"
        data_two.append(weighted_random_int())# "quantity"
        data_two.append(timens)
        
        data.append(data_two)
    Order_ID += 1
    
# print(data)
# 写入 CSV 文件
with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

print("CSV 文件已成功导出。")
    
