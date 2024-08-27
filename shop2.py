from Data_processing._setting import set_connect
import tkinter as tk
from PIL import Image, ImageTk
import cv2
from ultralytics import YOLO
import threading
import traceback
import time
import numpy as np
# from PIL import ImageDraw, ImageFont
from tkinter import messagebox
import sys 
from Data_processing.python_data_into_influxdb import data2influxdb, data2influxdb_2
import pandas as pd
from datetime import datetime
from collections import Counter


# 設置 Tkinter 視窗
root = tk.Tk()

# 創建影片 Label
video_label = tk.Label(root)
video_label.pack()

# 創建文本 Label
text_label = tk.Label(root, font=('Arial', 16))
text_label.pack()

def index_last_OrderID():
    from influxdb_client import InfluxDBClient

    # 配置
    influx_con = set_connect()
    # token = "2xE_ttHl9rzs0p19VzPwFdnsbVMp-jZwi7W4SKNTyiZXWvmFOPPN-wD9ZpvrLKsKC4YxooBN4o949ZFC6a70PQ=="
    token = influx_con.influxdb_token("custom")
    org = influx_con.influxdb_org
    url = influx_con.influxdb_url
    bucket = influx_con.influxdb_bucket

    # 创建 InfluxDB 客户端
    client = InfluxDBClient(url=url, token=token, org=org)
    query_api = client.query_api()

    query = f'''
    from(bucket: "{bucket}")
      |> range(start: -30d)
      |> filter(fn: (r) => r["_measurement"] == "test01")
      |> filter(fn: (r) => r["_field"] == "Order_ID")
      |> last()  // 獲取最新一筆資料
      |> yield(name: "mean")
    '''
    
    # 执行查询
    result = query_api.query(org=org, query=query)
    for table in result:
        for record in table.records:
            value = record.get_value()
    client.close() # 关闭客户端
    return value


# 創建按鈕
def on_button_click():
    
    # print(index_last_OrderID())
    
    # print(dblist)
    
    # 计算每个商品的数量
    item_counts = Counter(dblist)
    # print(item_counts)

    # 去重并保持顺序
    unique_items = list(dict.fromkeys(dblist))
    
    # 创建数据列表
    data = []
    
    # 遍历去重后的 dblist，并填充数据
    for id, item in enumerate(unique_items, start=index_last_OrderID() + 1):
        # 获取当前时间并转换为微秒
        now = datetime.now()
        micro = int(now.timestamp() * 1_000_000_000)
        # micro = (micro // 1000000000) * 1000000000
        data.append({
            'Order_ID': id,
            'commodity': item,
            'unit_price': price[item],  # 根据项目查找价格
            'quantity': item_counts[item]  # 根据统计的数量设置数量
            ,'time': micro  # 使用当前时间
        })
        time.sleep(1)
    
    # 创建 DataFrame
    df_items = pd.DataFrame(data)
    print(df_items)

    data2influxdb_2(df_items)
    
    
# ======================================================
    
    
button = tk.Button(root, text="確認結帳", state=tk.DISABLED, command=on_button_click)
button.config(state=tk.DISABLED)
button.pack()

# 創建一個文本輸入框
entry = tk.Entry(root)
entry.pack()


def activate_button(event=None):
    """檢查輸入框的內容，如果是 '1'，則啟用按鈕"""
    if entry.get() == '1':
        button.config(state=tk.NORMAL)
    else:
        messagebox.showinfo("警告", "請確認金額")
        button.config(state=tk.DISABLED)


# 創建一個觸發按鈕或用於檢查輸入框的按鈕
check_button = tk.Button(root, text="金額確認", command=activate_button)
check_button.pack()

# 讓輸入框能夠響應 Enter 鍵
entry.bind('<Return>', activate_button)

# 獲取視頻影像
target = 'BVN2.mp4'
model = YOLO('runs/detect/train4/weights/best.pt')
names = model.names
print("Run Program...")
cap = cv2.VideoCapture(target)

# 價格字典
price = {'品客洋芋片': 60, '原萃綠茶': 39, '肉骨湯麵': 15, '益生菌': 150}

# 標記是否應該繼續檢測
keep_detecting = True

def update_image(photo):
    video_label.configure(image=photo)
    video_label.image = photo

def detect_objects():
    global keep_detecting  # 使用 global 關鍵字
    while keep_detecting:
        try:
            st = time.time()
            r, frame = cap.read()
            if not r:
                break  # 如果讀取失敗，則退出循環
            
            # results = model(frame, verbose=False)
            results = model.predict(source=frame, conf=0.7)
            frame = results[0].plot()
            
            productCount = 0
            total = 0
            global dblist ; dblist = []
            items_with_prices = []
            boxes = results[0].boxes.data
            for box in boxes:
                confidence = box[4]  # 获取置信度
                # print(confidence, confidence >= 0.7)
                if confidence >= 0.7:  # 仅处理置信度大于等于 0.7 的框
                    item = names[int(box[5])]
                    if item != '':
                        productCount += 1
                        items_with_prices.append(f"{item}${price[item]}")
                        dblist.append(item)
                        total += price[item]
            
            # 將 OpenCV 圖像轉換為 PIL 圖像
            pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            # draw = ImageDraw.Draw(pil_img)
            
            # 設置字體和大小
            # font = ImageFont.truetype('simsun.ttc', size=32)
            
            # 將項目和價格串成一句話
            formatted_items = []
            item_newline = 6  # 顯示每3的商品後換行
            for i in range(0, len(items_with_prices), item_newline):
                formatted_items.append(", ".join(items_with_prices[i:i+item_newline]))
            text = "\n商品明細：".join(formatted_items) + f"\n銷售個數：{productCount};　合計${total}"
            
            # draw = ImageDraw.Draw(pil_img)

            # if productCount != 0:
            #     draw.text((20, 60), text, font=font, fill=(255, 255, 0))
            # else:
            #     draw.text((20, 60), "無商品", font=font, fill=(255, 255, 0))
            
            # 將 PIL 圖像轉換回 OpenCV 格式
            frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_BGR2RGB)
            
            et = time.time()
            FPStext = 'FPS=' + str(round((1/ (et-st)), 1))
            cv2.putText(frame, FPStext, (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2, cv2.LINE_AA)
            
            # 將 OpenCV 圖像轉換為 Tkinter 格式
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img = img.resize((1080, 500), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image=img)
            
            # 在 Tkinter 的主線程中更新影像
            root.after(0, update_image, photo)
            
            # 在 Tkinter 的主線程中更新文本 Label
            root.after(0, lambda: text_label.configure(text=text))
        
        except Exception:
            traceback.print_exc()
            break

def on_close():
    global keep_detecting
    keep_detecting = False
    cap.release()
    thread.join()
    root.destroy()
    sys.exit()

# 啟動檢測線程
thread = threading.Thread(target=detect_objects)
thread.start()

# 設置關閉窗口的處理函數
root.protocol("WM_DELETE_WINDOW", on_close)

# Tkinter 主循環
root.mainloop()
