## 商品辨識
▼ "金額確認"為結帳完成與否的確認(未有設備以輸入1取代確認)，結帳完成後點擊"確認結帳"把資料匯入InfluxDB內
註:辨識率大於0.7才判定商品
![image](https://github.com/user-attachments/assets/d54cc5d8-e1ba-4650-8a8c-ea7fc068715f)
▼ 結帳完成的資料匯入InfluxDB中
![image](https://github.com/user-attachments/assets/540afb55-ac05-45ee-af4e-1011ebd2f39b)
▼ 統計出個各種資料，並在Grafana中呈現
![image](https://github.com/user-attachments/assets/9cf9cce0-22ca-418b-bafd-f9b203a15388)



## 預測未來7日的來客人數 & 營業額

▼ 每日銷售資料(資料為一年)
![image](https://github.com/user-attachments/assets/e9eca5ca-8853-4c90-a706-4d62e87cca32)

▼ 依照Order_ID為來客消費的依據，並依每日日期為單位合計，統計出每日來客人數

![image](https://github.com/user-attachments/assets/a58690c9-a8b0-47bd-a7be-0a04d986c479)

▼ 單價X數量，並依每日日期為單位合計，統計出每日營業額

![image](https://github.com/user-attachments/assets/1dc1ade7-beb6-4dfd-b142-5415c5ecaf73)

▼ 建立LSTM模型，進行訓練(time_step:5天)

![image](https://github.com/user-attachments/assets/1ebcbd10-41ab-4383-bd48-668ceb35b03c)

▼ 未來7日來客量的預測結果:

![image](https://github.com/user-attachments/assets/4cdbb594-ba80-4672-9b26-cbea059b9e0f)

▼ 未來7日營業額的預測結果:

![image](https://github.com/user-attachments/assets/54ba1f04-15fd-4604-89e9-43f1a2f32a03)



