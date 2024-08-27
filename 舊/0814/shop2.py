import tkinter as tk
from PIL import Image, ImageTk
import cv2
from ultralytics import YOLO
import threading
import traceback ,time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

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
    print("Button clicked!")

button = tk.Button(root, text="Click Me", command=on_button_click)
button.pack()

# 獲取視頻影像
target = 'BVN.mp4'
model = YOLO('runs/detect/train4/weights/best.pt')
names = model.names
print(names)
cap = cv2.VideoCapture(target)

# 價格字典
price = {'品客洋芋片': 60, '原萃綠茶': 39, '肉骨湯麵': 15, '益生菌': 150}

# 標記是否應該繼續檢測
keep_detecting = True

def update_image(photo):
    video_label.configure(image=photo)
    video_label.image = photo

def detect_objects():
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
            draw = ImageDraw.Draw(pil_img)
            
            # 設置字體和大小
            font = ImageFont.truetype('simsun.ttc', size=32)
            
            # 將項目和價格串成一句話
            formatted_items = []
            for i in range(0, len(items_with_prices), 3):
                formatted_items.append(", ".join(items_with_prices[i:i+3]))
            text = "\n".join(formatted_items) + f"; \n合計${total}"
            
            if productCount != 0:
                draw.text((20, 60), text, font=font, fill=(255, 255, 0))
            else:
                draw.text((20, 60), "無商品", font=font, fill=(255, 255, 0))
            
            # 將 PIL 圖像轉換回 OpenCV 格式
            frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            
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

# 啟動檢測線程
thread = threading.Thread(target=detect_objects)
thread.start()

# Tkinter 主循環
root.mainloop()

# 退出時停止檢測
keep_detecting = False
thread.join()
cap.release()