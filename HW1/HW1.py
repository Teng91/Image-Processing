import numpy as np
import matplotlib.pyplot as plt
###1
# read "JET.64" file
f=open('JET.64','r')
file=f.read()
f.close()
# ASCII transform
list_ = []
for i in file:
    if 48 <= ord(i) <= 57:
        i = (ord(i)-48)
        list_.append(i)
    elif 65 <= ord(i) <= 86:
        i = (ord(i)-55)
        list_.append(i)
# 新建空的list存32個灰階值
list1 = np.zeros(32, int)
for i in list_:
    list1[i] += 1
# 作圖
plt.subplot(2, 2, 1)
plt.bar(range(32), list1)
plt.title("Histogram of JET Image")
plt.xlabel("gray levels")
plt.ylabel("counts")

# read "LIBERTY.64" file
f=open('LIBERTY.64','r')
file=f.read()
f.close()
# ASCII transform
list_ = []
for i in file:
    if 48 <= ord(i) <= 57:
        i = (ord(i)-48)
        list_.append(i)
    elif 65 <= ord(i) <= 86:
        i = (ord(i)-55)
        list_.append(i)
# 新建空的list存32個灰階值
list1 = np.zeros(32, int)
for i in list_:
    list1[i] += 1
# 作圖
plt.subplot(2, 2, 2)
plt.bar(range(32), list1)
plt.title("Histogram of LIBERTY Image")
plt.xlabel("gray levels")
plt.ylabel("counts")

# read "LINCOLN.64" file
f=open('LINCOLN.64','r')
file=f.read()
f.close()
# ASCII transform
list_ = []
for i in file:
    if 48 <= ord(i) <= 57:
        i = (ord(i)-48)
        list_.append(i)
    elif 65 <= ord(i) <= 86:
        i = (ord(i)-55)
        list_.append(i)
# 新建空的list存32個灰階值
list1 = np.zeros(32, int)
for i in list_:
    list1[i] += 1
# 作圖
plt.subplot(2, 2, 3)
plt.bar(range(32), list1)
plt.title("Histogram of LINCOLN Image")
plt.xlabel("gray levels")
plt.ylabel("counts")

# read "LISA.64" file
f=open('LISA.64','r')
file=f.read()
f.close()
# ASCII transform
list_ = []
for i in file:
    if 48 <= ord(i) <= 57:
        i = (ord(i)-48)
        list_.append(i)
    elif 65 <= ord(i) <= 86:
        i = (ord(i)-55)
        list_.append(i)
# 新建空的list存32個灰階值
list1 = np.zeros(32, int)
for i in list_:
    list1[i] += 1
# 作圖
plt.subplot(2, 2, 4)
plt.bar(range(32), list1)
plt.title("Histogram of LISA Image")
plt.xlabel("gray levels")
plt.ylabel("counts")
# 調整排版、出圖
plt.tight_layout()
plt.show(block=False)
plt.pause(3)
plt.close()
###2-1 add
# read "JET.64" file
f=open('JET.64','r')
file=f.read()
f.close()
# ASCII transform
list_ = []
for i in file:
    if 48 <= ord(i) <= 57:
        i = (ord(i)-48)
        list_.append(i)
    elif 65 <= ord(i) <= 86:
        i = (ord(i)-55)
        list_.append(i)
# 新建空的list存32個灰階值
list1 = np.zeros(32, int)
for i in list_:
    list1[i] += 1
# 將list轉成64*64作圖
arr1 = np.array(list_)
arr2 = np.reshape(arr1, (-1, 64))
# add 10
arr_add1 = arr2 + 10
arr_add1[arr_add1>=31]=31
arr_Add1 = arr_add1.astype(int)
arr_Add1
# 生成add 10 image
list2 = np.zeros(32, int)
for i in arr_Add1[i]:
    for j in arr_Add1[i]:
        list2[j] += 1
plt.subplot(2, 3, 1)
plt.imshow(arr_Add1, cmap='gray')
plt.clim(0,31)
plt.axis('off')
# 計算add 10 historgram
plt.subplot(2, 3, 4)
x = range(32)
y = list2
plt.bar(x, y)
plt.title("JET Add 10")
plt.xlabel("gray levels")
plt.ylabel("counts")
# add 20
arr_add1 = arr2 + 20
arr_add1[arr_add1>=31]=31
arr_Add1 = arr_add1.astype(int)
arr_Add1
# 生成add 20 image
list2 = np.zeros(32, int)
for i in arr_Add1[i]:
    for j in arr_Add1[i]:
        list2[j] += 1
plt.subplot(2, 3, 2)
plt.imshow(arr_Add1, cmap='gray')
plt.clim(0,31)
plt.axis('off')
# 計算add 20 historgram
plt.subplot(2, 3, 5)
x = range(32)
y = list2
plt.bar(x, y)
plt.title("JET Add 20")
plt.xlabel("gray levels")
plt.ylabel("counts")
# add 30
arr_add1 = arr2 + 30
arr_add1[arr_add1>=31]=31
arr_Add1 = arr_add1.astype(int)
arr_Add1
# 生成add 30 image
list2 = np.zeros(32, int)
for i in arr_Add1[i]:
    for j in arr_Add1[i]:
        list2[j] += 1
plt.subplot(2, 3, 3)
plt.imshow(arr_Add1, cmap='gray')
plt.clim(0,31)
plt.axis('off')
# 計算add 30 historgram
plt.subplot(2, 3, 6)
x = range(32)
y = list2
plt.bar(x, y)
plt.title("JET Add 30")
plt.xlabel("gray levels")
plt.ylabel("counts")
#調整排版、出圖
plt.tight_layout()
plt.show(block=False)
plt.pause(3)
plt.close()
###2-1 minus
# read "JET.64" file
f=open('JET.64','r')
file=f.read()
f.close()
# ASCII transform
list_ = []
for i in file:
    if 48 <= ord(i) <= 57:
        i = (ord(i)-48)
        list_.append(i)
    elif 65 <= ord(i) <= 86:
        i = (ord(i)-55)
        list_.append(i)
# 新建空的list存32個灰階值
list1 = np.zeros(32, int)
for i in list_:
    list1[i] += 1
# 將list轉成64*64作圖
arr1 = np.array(list_)
arr2 = np.reshape(arr1, (-1, 64))
# minus 10
arr_minus1 = arr2 - 10
arr_minus1[arr_minus1<=0]=0
arr_Minus1 = arr_minus1.astype(int)
arr_Minus1
# 生成minus 10 image
list2 = np.zeros(32, int)
for i in arr_Minus1[i]:
    for j in arr_Minus1[i]:
        list2[j] += 1
plt.subplot(2, 3, 1)
plt.imshow(arr_Minus1, cmap='gray')
plt.clim(0,31)
plt.axis('off')
# 計算minus 10 historgram
plt.subplot(2, 3, 4)
x = range(32)
y = list2
plt.bar(x, y)
plt.title("JET Minus 10")
plt.xlabel("gray levels")
plt.ylabel("counts")
# minus 20
arr_minus1 = arr2 - 20
arr_minus1[arr_minus1<=0]=0
arr_Minus1 = arr_minus1.astype(int)
arr_Minus1
# 生成minus 20 image
list2 = np.zeros(32, int)
for i in arr_Minus1[i]:
    for j in arr_Minus1[i]:
        list2[j] += 1
plt.subplot(2, 3, 2)
plt.imshow(arr_Minus1, cmap='gray')
plt.clim(0,31)
plt.axis('off')
# 計算minus 20 historgram
plt.subplot(2, 3, 5)
x = range(32)
y = list2
plt.bar(x, y)
plt.title("JET Minus 20")
plt.xlabel("gray levels")
plt.ylabel("counts")
# minus 30
arr_minus1 = arr2 - 30
arr_minus1[arr_minus1<=0]=0
arr_Minus1 = arr_minus1.astype(int)
arr_Minus1
# 生成minus 30 image
list2 = np.zeros(32, int)
for i in arr_Minus1[i]:
    for j in arr_Minus1[i]:
        list2[j] += 1
plt.subplot(2, 3, 3)
plt.imshow(arr_Minus1, cmap='gray')
plt.clim(0,31)
plt.axis('off')
# 計算minus 30 historgram
plt.subplot(2, 3, 6)
x = range(32)
y = list2
plt.bar(x, y)
plt.title("JET Minus 30")
plt.xlabel("gray levels")
plt.ylabel("counts")
#調整排版、出圖
plt.tight_layout()
plt.show(block=False)
plt.pause(3)
plt.close()
###2-2 multi
# read "JET.64" file
f=open('JET.64','r')
file=f.read()
f.close()
# ASCII transform
list_ = []
for i in file:
    if 48 <= ord(i) <= 57:
        i = (ord(i)-48)
        list_.append(i)
    elif 65 <= ord(i) <= 86:
        i = (ord(i)-55)
        list_.append(i)
# 新建空的list存32個灰階值
list1 = np.zeros(32, int)
for i in list_:
    list1[i] += 1
# 將list轉成64*64作圖
arr1 = np.array(list_)
arr2 = np.reshape(arr1, (-1, 64))
# multi 1.5
arr_multi1 = arr2*1.5
arr_multi1[arr_multi1>=31]=31
arr_Multi1 = arr_multi1.astype(int)
arr_Multi1
# 生成multi 1.5 image
list2 = np.zeros(32, int)
for i in arr_Multi1[i]:
    for j in arr_Multi1[i]:
        list2[j] += 1
plt.subplot(2, 3, 1)
plt.imshow(arr_Multi1, cmap='gray')
plt.clim(0,31)
plt.axis('off')
# 計算multi 1.5 historgram
plt.subplot(2, 3, 4)
x = range(32)
y = list2
plt.bar(x, y)
plt.title("JET Multi 1.5")
plt.xlabel("gray levels")
plt.ylabel("counts")
# multi 10
arr_multi1 = arr2*10
arr_multi1[arr_multi1>=31]=31
arr_Multi1 = arr_multi1.astype(int)
arr_Multi1
# 生成multi 10 image
list2 = np.zeros(32, int)
for i in arr_Multi1[i]:
    for j in arr_Multi1[i]:
        list2[j] += 1
plt.subplot(2, 3, 2)
plt.imshow(arr_Multi1, cmap='gray')
plt.clim(0,31)
plt.axis('off')
# 計算multi 10 historgram
plt.subplot(2, 3, 5)
x = range(32)
y = list2
plt.bar(x, y)
plt.title("JET Multi 10")
plt.xlabel("gray levels")
plt.ylabel("counts")
# multi 31
arr_multi1 = arr2*31
arr_multi1[arr_multi1>=31]=31
arr_Multi1 = arr_multi1.astype(int)
arr_Multi1
# 生成multi 31 image
list2 = np.zeros(32, int)
for i in arr_Multi1[i]:
    for j in arr_Multi1[i]:
        list2[j] += 1
plt.subplot(2, 3, 3)
plt.imshow(arr_Multi1, cmap='gray')
plt.clim(0,31)
plt.axis('off')
# 計算multi 31 historgram
plt.subplot(2, 3, 6)
x = range(32)
y = list2
plt.bar(x, y)
plt.title("JET Multi 31")
plt.xlabel("gray levels")
plt.ylabel("counts")
#調整排版、出圖
plt.tight_layout()
plt.show(block=False)
plt.pause(3)
plt.close()
###2-3
f1=open('LINCOLN.64','r')
f2=open('LISA.64','r')
file1=f1.read()
file2=f2.read()
f.close()
# ASCII transform
list1 = []
for i in file1:
    if 48 <= ord(i) <= 57:
        i = (ord(i)-48)
        list1.append(i)
    elif 65 <= ord(i) <= 86:
        i = (ord(i)-55)
        list1.append(i)
arr3 = np.array(list1)
arr4 = np.reshape(arr3, (-1, 64))
list2 = []
for i in file2:
    if 48 <= ord(i) <= 57:
        i = (ord(i)-48)
        list2.append(i)
    elif 65 <= ord(i) <= 86:
        i = (ord(i)-55)
        list2.append(i)
arr5 = np.array(list2)
arr6 = np.reshape(arr5, (-1, 64))
# 合成兩張圖片
arr_new = (arr4+arr6)//2
arr_new[arr_new>=31]=31
arr_new[arr_new<=0]=0
arr_New = arr_new.astype(int)
arr_New
# 生成合成後image
list3 = np.zeros(32, int)
for i in range(32):
    for j in arr_New[i]:
        list3[j] += 1
plt.subplot(1, 2, 1)
plt.imshow(arr_New, cmap='gray')
plt.clim(0,31)
plt.axis('off')
plt.subplot(1, 2, 2)
# 計算合成後historgram
x = range(32)
y = list3
plt.bar(x, y)
plt.title("average of two images")
plt.xlabel("gray levels")
plt.ylabel("counts")
#調整排版、出圖
plt.tight_layout()
plt.show(block=False)
plt.pause(3)
plt.close()
###2-4
f=open('LINCOLN.64','r')
file=f.read()
f.close()
# ASCII transform
list_ = []
for i in file:
    if 48 <= ord(i) <= 57:
        i = (ord(i)-48)
        list_.append(i)
    elif 65 <= ord(i) <= 86:
        i = (ord(i)-55)
        list_.append(i)
# 複製array
arr1 = np.array(list_)
arr2 = np.reshape(arr1, (-1, 64))
arr3 = arr2.copy()
# g(x,y) = f(x,y) - f(x-1,y)
for i in range(64):
    for j in range(64):
        if j == 0:
            continue
        arr3[i,j] = arr3[i,j] - arr2[i-1,j]
arr3[arr3>=31]=31
arr3[arr3<=0]=0
# 生成image
list3 = np.zeros(32, int)
for i in range(32):
    for j in arr3[i]:
        list3[j] += 1
plt.subplot(1, 2, 1)
plt.imshow(arr3, cmap='gray')
plt.clim(0,31)
plt.axis('off')
# 計算historgram
plt.subplot(1, 2, 2)
x = range(32)
y = list3
plt.bar(x, y)
plt.title("LINCOLN g(x,y)")
plt.xlabel("gray levels")
plt.ylabel("counts")
#調整排版、出圖
plt.tight_layout()
plt.show(block=False)
plt.pause(3)
plt.close()
