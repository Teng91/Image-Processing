import math
import cv2
import pywt
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

### Problem 1 ###
def Trapezoidal_Transformation():
    path = filedialog.askopenfilename()
    img = cv2.imread(path)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rows, cols = imgGray.shape[:2]
    pts1 = np.float32([[0, 0], [cols, 0], [0, rows], [cols, rows]])
    pts2 = np.float32([[0, 0], [cols, 0], [0.25*cols, 0.75*rows], [0.75*cols, 0.75*rows]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(imgGray, matrix, (cols, rows))

    # Show images
    plt.figure(figsize=(6, 4))
    original_image = plt.subplot(1, 2, 1)
    original_image.imshow(imgGray, cmap='gray')
    plt.title('Original Image')
    Trapezoidal_image = plt.subplot(1, 2, 2)
    Trapezoidal_image.imshow(result, cmap='gray')
    plt.title('Trapezoidal Transformation')
    plt.show()

def Wavy_Transformation():
    path = filedialog.askopenfilename()
    img = cv2.imread(path)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rows, cols = imgGray.shape[:2]
    Trans_ = np.zeros((rows, cols), dtype=np.uint8)
    for row in range(rows):
        for col in range(cols):
            pts1 = row + int(50*np.sin(col*np.pi/180))
            pts2 = col + int(50*np.sin(row*np.pi/180))
            if pts1 > 0 and pts2 > 0:
                if pts1 < rows and pts2 < cols:
                    Trans_[row][col] = imgGray[pts1][pts2]

    # Show images
    plt.figure(figsize=(6, 4))
    original_image = plt.subplot(1, 2, 1)
    original_image.imshow(imgGray, cmap='gray')
    plt.title('Original Image')
    Wavy_image = plt.subplot(1, 2, 2)
    Wavy_image.imshow(Trans_, cmap='gray')
    plt.title('Wavy Transformation')
    plt.show()

def Circular_Transformation():
    path = filedialog.askopenfilename()
    img = cv2.imread(path)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rows, cols = imgGray.shape[:2]
    Trans_ = np.zeros((rows, cols), dtype=np.uint8)
    center_x = rows/2
    center_y = cols/2
    for row in range(rows):
        for col in range(cols):
            row_ratio = (row - center_x)/center_x
            col_ratio = (col - center_y)/center_y
            row_mod = row_ratio * np.sqrt(1 - col_ratio ** 2 / 2) * center_x + center_x
            col_mod = col_ratio * np.sqrt(1 - row_ratio ** 2 / 2) * center_y + center_y
            Trans_[int(row_mod)][int(col_mod)] = imgGray[row][col]

    # Show images
    plt.figure(figsize=(6, 4))
    original_image = plt.subplot(1, 2, 1)
    original_image.imshow(imgGray, cmap='gray')
    plt.title('Original Image')
    Circular_image = plt.subplot(1, 2, 2)
    Circular_image.imshow(Trans_, cmap='gray')
    plt.title('Circular Transformation')
    plt.show()

### Problem 2 ###
def wavelet():
    # Set up variables
    path = filedialog.askopenfilename()
    imgRGB_part2   = cv2.imread(path)
    imgGray_part2  = cv2.cvtColor(imgRGB_part2, cv2.COLOR_BGR2GRAY)

    # Wavelet Transform
    cA, (cH, cV, cD) = pywt.dwt2(imgGray_part2, 'haar')  

    # Show images
    plt.figure(figsize = (12,4))
    approximation = plt.subplot(1, 4, 1)
    approximation.imshow(cA, cmap='gray')
    plt.title('Approximation')

    horizontal = plt.subplot(1, 4, 2)
    horizontal.imshow(cH, cmap='gray')
    plt.title('Horizontal Detail')

    vertical = plt.subplot(1, 4, 3)
    vertical.imshow(cV, cmap='gray')
    plt.title('Vertical Detail')

    diagonal = plt.subplot(1, 4, 4)
    diagonal.imshow(cD, cmap='gray')
    plt.title('Diagonal Detail')
    plt.show()

def fuseImg():
    # Set up variables
    fuseNum = int(fuseNum_.get())
    coeffsList = []
    fuseList   = []

    # Show text
    show_text.insert('insert',"Fuse " + str(fuseNum) + ' images\n\n')

    for i in range (fuseNum):
        path = filedialog.askopenfilename()
        imgRGB_part2   = cv2.imread(path)
        imgGray_part2  = cv2.cvtColor(imgRGB_part2, cv2.COLOR_BGR2GRAY)

        # Wavelet Transform
        coeffs  = pywt.wavedec2(imgGray_part2[:,:], 'haar')
        coeffsList.append(coeffs)

    # Fuse
    if fuseNum == 2:
        for i in range(len(coeffsList[0])-1):
            if(i == 0):
                c = np.maximum(coeffsList[0][0], coeffsList[1][0])
                fuseList.append(c)
                continue
            c1 = np.maximum(coeffsList[0][i][0], coeffsList[1][i][0])
            c2 = np.maximum(coeffsList[0][i][1], coeffsList[1][i][1])
            c3 = np.maximum(coeffsList[0][i][2], coeffsList[1][i][2])
            c  = (c1, c2, c3)
            fuseList.append(c)
    elif fuseNum == 3:
        for i in range(len(coeffsList[0])-1):
            if(i == 0):
                c = np.maximum(coeffsList[0][0], coeffsList[1][0])
                c = np.maximum(coeffsList[2][0], c)
                fuseList.append(c)
                continue
            c1 = np.maximum(coeffsList[0][i][0], coeffsList[1][i][0])
            c1 = np.maximum(coeffsList[2][i][0], c1)
            c2 = np.maximum(coeffsList[0][i][1], coeffsList[1][i][1])
            c2 = np.maximum(coeffsList[2][i][1], c2)
            c3 = np.maximum(coeffsList[0][i][2], coeffsList[1][i][2])
            c3 = np.maximum(coeffsList[2][i][2], c3)
            c  = (c1, c2, c3)
            fuseList.append(c)

    fuseImg = pywt.waverec2(fuseList, 'haar')
    
    # Show images
    plt.figure(figsize = (6,4))
    fuseImgShow = plt.subplot(1, 1, 1)
    fuseImgShow.imshow(fuseImg, cmap ='gray')
    plt.title('Fusion Result')
    plt.show()

### Problem 3 ###
def cannyHough():
    # Set up variables
    path = filedialog.askopenfilename()
    imgRGB_part3  = cv2.imread(path)
    imgGray_part3 = cv2.cvtColor(imgRGB_part3, cv2.COLOR_BGR2GRAY)
    imgGray_part3_line = cv2.cvtColor(imgRGB_part3, cv2.COLOR_BGR2GRAY)
    threshold = int(threshold_.get())

    # Show text
    show_text.insert('insert',"Do hough transform, threshold is " + str(threshold) + '\n\n')

    # Hough transform
    imgEdge_part3 = cv2.Canny(imgGray_part3, threshold1 = 50, threshold2 = 150, apertureSize = 3)
    imgLine_part3 = cv2.HoughLines(imgEdge_part3, rho = 1, theta = np.pi/180, threshold = threshold)

    # Draw line
    for i in range(len(imgLine_part3)):
        for rho,theta in imgLine_part3[i]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(imgGray_part3_line, (x1,y1),(x2,y2) , (0,0,255), 2)

    # Show images
    plt.figure(figsize = (10,4))

    originalImgGray = plt.subplot(1, 3, 1)
    originalImgGray.imshow(imgGray_part3, cmap ='gray')
    plt.title('Original Grayscale Image')

    cannyImage = plt.subplot(1, 3, 2)
    cannyImage.imshow(imgEdge_part3, cmap ='gray')
    plt.title('Canny Detection')

    lineImage = plt.subplot(1, 3, 3)
    lineImage.imshow(imgGray_part3_line, cmap ='gray')
    plt.title('Hough Transform (Threshold = '+ str(threshold) + ')')

    plt.show()

### GUI ###
window = tk.Tk()
window.title('r11631006_hw6')
window.geometry('705x310')

# Trapezoidal Transformation
button_Trapezoidal = tk.Button(window, text = "Trapezoidal Transformation", command = Trapezoidal_Transformation)
button_Trapezoidal.place(x = 10, y = 10)

# Wavy_Transformation
button_Wavy = tk.Button(window, text = "Wavy Transformation", command = Wavy_Transformation)
button_Wavy.place(x = 10, y = 40)

# Circular_Transformation
button_Circular = tk.Button(window, text = "Circular Transformation", command = Circular_Transformation)
button_Circular.place(x = 10, y = 70)

# Wavlet Transform Button
button_wavelet = tk.Button(window, text = "Wavelet Transform", command = wavelet)
button_wavelet.place(x = 10, y = 115)

# Fuse images with wavelet
button_fuse = tk.Button(window, text = "Fuse Images with DWT", command = fuseImg)
button_fuse.place(x = 10, y = 145)

# User Input : Fuse images numbers
fuseNum_frame = tk.Frame(window)
fuseNum_frame.place(x = 10, y = 175)
fuseNum_label = tk.Label(fuseNum_frame, text = 'Fusing Images Number')
fuseNum_label.pack(side = tk.LEFT)
fuseNum_ = tk.Entry(fuseNum_frame, width = 7)
fuseNum_.pack()

# Hough Transform Button
button_cannyHough = tk.Button(window, text = "Hough Transform", command = cannyHough)
button_cannyHough.place(x = 10, y = 245)

# User Input : Hough Transform Threshold
threshold_frame = tk.Frame(window)
threshold_frame.place(x = 10, y = 275)
threshold_label = tk.Label(threshold_frame, text = 'Hough Threshold')
threshold_label.pack(side = tk.LEFT)
threshold_ = tk.Entry(threshold_frame, width = 9)
threshold_.pack()

# Show Text
show_text = tk.Text(window, height = 22, width = 69)
show_text.place(x = 210, y = 10)

window.mainloop()