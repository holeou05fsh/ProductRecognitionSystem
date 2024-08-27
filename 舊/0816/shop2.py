import tkinter as tk
from PIL import Image, ImageTk
import cv2
from ultralytics import YOLO
import threading
import traceback
import time
import numpy as np
from PIL import ImageDraw, ImageFont
from tkinter import messagebox
import sys 

# 設置 Tkinter 視窗
root = tk.Tk()

# 創建影片 Label
video_label = tk.Label(root)
video_label.pack()

# 創建文本 Label
text_label = tk.Label(root, font=('Arial', 16))
text_label.pack()

# 創建按鈕
def on_button_click():
    # pass
    import influxdb_client, os, time
    from influxdb_client import InfluxDBClient, Point, WritePrecision
    from influxdb_client.client.write_api import SYNCHRONOUS
    import random
     
    token = os.environ.get("INFLUXDB_TOKEN")
    org_test = "org100"
    url = "http://localhost:9999"
    bucket_test = "bucket100"
    
    write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org_test)
    write_api = write_client.write_api(write_options=SYNCHRONOUS)
    
    
# ===============找DB中Order_ID的最新的一筆==================
    # 创建 InfluxDB 客户端
    client = InfluxDBClient(url=url, token=token, org=org_test)
    query_api = client.query_api()
    
    # 查询最新的一笔数据
    query = f'''
    from(bucket: "{bucket_test}")
      |> range(start: -1d)  // 查询过去一天的数据
      |> filter(fn: (r) => r["_measurement"] == "your_measurement")  // 根据实际情况替换 measurement
      |> filter(fn: (r) => r["_field"] == "Order_ID")
      |> last()
    '''
    
    # 执行查询
    result = query_api.query(org=org_test, query=query)
    
    # 检查是否有结果
    if not result:
        print("没有找到匹配的数据。")
    else:
        for table in result:
            for record in table.records:
                print(f"Order_ID: {record.get_value()}")
    
    # 关闭客户端
    client.close()

# ======================================================
    
    
    while True:
        Order_ID = random.randint(10, 100)
        commodity = f"commodity_{random.randint(1, 10)}"
        unit_price = round(random.uniform(1.0, 100.0), 2)
        
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
target = 'BVN.mp4'
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
            
            results = model(frame, verbose=False)
            frame = results[0].plot()
            
            productCount = 0
            total = 0
            items_with_prices = []
            boxes = results[0].boxes.data
            for box in boxes:
                item = names[int(box[5])]
                if item != '':
                    productCount += 1
                    items_with_prices.append(f"{item}${price[item]}")
                    total += price[item]
            
            # 將 OpenCV 圖像轉換為 PIL 圖像
            pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            # draw = ImageDraw.Draw(pil_img)
            
            # 設置字體和大小
            # font = ImageFont.truetype('simsun.ttc', size=32)
            
            # 將項目和價格串成一句話
            global formatted_items
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
            img = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=img)
            
            # 在 Tkinter 的主線程中更新影像
            root.after(0, update_image, photo)
            
            # 在 Tkinter 的主線程中更新文本 Label
            root.after(0, lambda: text_label.configure(text=text))
        
        except Exception as e:
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
