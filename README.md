# Image Processing
- Programming language: Python, C++
- QT version: 5.13.2
- OpenCV version: 4.1.1
- 本專案包含多個影像處理相關的專案，涵蓋影像處理、分析與轉換技術
- 結合 OpenCV 與 Qt 等工具，提供了圖形化介面（GUI）以便於操作與展示

**Image-Processing/**     
├── HW1/ &emsp;&emsp;   # Python：影像直方圖與算術運算                
├── HW2/ &emsp;&emsp;   # C++：影像讀取、顯示與基本處理            
├── HW3/ &emsp;&emsp;   # C++：空間濾波與邊緣檢測                
├── HW4/ &emsp;&emsp;   # Python：頻域處理與濾波             
├── HW5/ &emsp;&emsp;   # C++：色彩模型轉換與分割               
├── HW6/ &emsp;&emsp;   # Python：幾何轉換與霍夫變換               
├── Project/ &emsp;   # 專案：基於 YOLOv7 的物件檢測

## 功能說明
1. HW1 (Python)
   - 功能：**計算影像直方圖，進行影像的加法、減法與乘法運算**
   - 檔案：
     - HW1.py: 主程式，包含影像處理邏輯
     - JET.64, LIBERTY.64, LINCOLN.64, LISA.64: 測試用影像資料
   - 技術說明：
      - 使用 NumPy 進行矩陣運算，Matplotlib 繪製直方圖
2. HW2 (C++)
   - 功能：**影像讀取、顯示，灰階轉換，亮度與對比度調整，直方圖均衡化**
   - 檔案：
     - mainwindow.cpp, mainwindow.h: GUI 主邏輯
     - mainwindow.ui: Qt Designer 設計的介面
   - 技術說明：
      - 使用 OpenCV 處理影像，Qt 提供 GUI 支援
3. HW3 (C++)
   - 功能：**空間濾波（卷積）、邊緣檢測（LoG、Marr-Hildreth）、局部增強**
   - 檔案：
     - mainwindow.cpp, mainwindow.h: GUI 主邏輯
     - mainwindow.ui: Qt Designer 設計的介面
   - 技術說明：
      - 使用 OpenCV 實現卷積與邊緣檢測，Qt 提供 GUI 支援
4. HW4 (Python)
   - 功能：**快速傅立葉變換（FFT）、高通與低通濾波、同態濾波、運動模糊處理**
   - 檔案：
     - r11631006_hw4.py: 主程式，包含頻域處理邏輯
   - 技術說明：
      - 使用 NumPy 實現 FFT，Matplotlib 繪製頻譜圖
5. HW5 (C++)
   - 功能：**色彩模型轉換（RGB、CMY、HSI、XYZ、LAB）、偽彩色處理、色彩分割（K-means）**
   - 檔案：
     - mainwindow.cpp, mainwindow.h: GUI 主邏輯
     - mainwindow.ui: Qt Designer 設計的介面
   - 技術說明：
      - 使用 OpenCV 實現色彩模型轉換與 K-means 演算法，Qt 提供 GUI 支援
6. HW6 (Python)
   - 功能：**幾何轉換（旋轉、縮放）、影像融合（小波變換）、霍夫變換**
   - 檔案：
     - r11631006_hw6.py: 主程式，包含幾何與霍夫變換邏輯
   - 技術說明：
      - 使用 OpenCV 實現幾何與霍夫變換，Tkinter 提供 GUI 支援
7. Project (Python)
   - 功能：**基於 YOLOv7 的物件檢測**
   - 檔案：
     - detect.py: 主程式，執行物件檢測
     - custom_data.yaml: 自定義資料集配置
   - 技術說明：
      - 使用 PyTorch 與 YOLOv7 模型進行物件檢測
