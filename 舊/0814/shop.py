from ultralytics import YOLO
import cv2, time
import traceback
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import threading

cv2.namedWindow('YOLOv8', cv2.WINDOW_NORMAL)

target = 'BVN.mp4'
model = YOLO('runs/detect/train4/weights/best.pt')

# 標記是否應該繼續檢測
keep_detecting = True

names = model.names
print(names)
cap = cv2.VideoCapture(target)

price = {'品客洋芋片':60, '原萃綠茶':39, '肉骨湯麵':15, '益生菌':150}

def detect_objects():
    while 1:
        try:
            st = time.time()
            r, frame = cap.read()
            results = model(frame, verbose=False)
            frame = results[0].plot()
            # frame_umat = cv2.UMat(frame)
            
            productCount=0; total=0 ;items_with_prices=[]
            boxes = results[0].boxes.data
            for box in boxes:
                # x1,y1,x2,y2 = box[:4].int()
                # r = round(float(box[4]), 2)
                item = names[int(box[5])]
                # print(n)
                if item != '':
                    productCount += 1
                    items_with_prices.append(f"{item}${price[item]}")
                    total += price[item]
            
            # 將 OpenCV 圖像轉換為 PIL 圖像
            pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(pil_img)
    
            # 設置字體和大小
            font = ImageFont.truetype('simsun.ttc', size=32)  # 確保字體文件存在
            # 將項目和價格串成一句話
            formatted_items = []
            for i in range(0, len(items_with_prices), 3):
                formatted_items.append(", ".join(items_with_prices[i:i+3]))
            text = "\n".join(formatted_items) + f"; \n合計${total}"
            # print(text)
            
            
            if productCount != 0:  
                draw.text((20, 60), text, font=font, fill=(255, 255, 0))  # 使用黃色填充
            else:
                draw.text((20, 60), "無商品", font=font, fill=(255, 255, 0))  # 使用黃色填充
            
            # 將 PIL 圖像轉換回 OpenCV 格式
            frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            et = time.time()
            FPStext = 'FPS=' + str(round((1/ (et-st)), 1))
            # draw.text((20, 80), FPStext, font=font, fill=(255, 255, 0))  # 使用黃色填充
            cv2.putText(frame, FPStext, (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow('YOLOv8', frame)
            key = cv2.waitKey(1)
            if key == 27:
                break
        except:
            # print(e)
            traceback.print_exc()
            break
       
       
       
       
       
            
