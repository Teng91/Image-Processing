import os
import cv2
import time
import random
import numpy as np
import tkinter as tk
from   tkinter import filedialog
from matplotlib import pyplot as plt
from math import exp, pi, sin, cos

def openImg():
    # Set variable
    global path 
    global imgGray
    global imgRGB
    global centerX
    global centerY

    # Open Img
    path = filedialog.askopenfilename()
    imgRGB = cv2.imread(path, cv2.IMREAD_COLOR)
    imgGray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    centerX = imgGray.shape[1]/2
    centerY = imgGray.shape[0]/2

    # Show Img
    cv2.destroyAllWindows()
    cv2.imshow("Original Grayscale Image", imgGray)

    # Show text
    show_text.insert('insert', "Image source : " + str(path))
    show_text.insert('insert', '\n')

def fftAndIfftImg():
    # Set up variables
    timeStart = time.time()

    # FFT
    fft = cv2.dft(np.float32(imgGray),flags=cv2.DFT_COMPLEX_OUTPUT)
    fftShift = np.fft.fftshift(fft)
    fftShift_Spectrum = np.log(cv2.magnitude(fftShift[:,:,0],fftShift[:,:,1]))   # Get specturm
    fftShift_Phase = np.angle(np.fft.fft2(imgGray))                              # Get angle

    # ifft
    ifftshift = np.fft.ifftshift(fftShift)
    ifft = cv2.idft(ifftshift)
    ifftScale = cv2.magnitude(ifft[:,:,0], ifft[:,:,1])

    # Time End
    timeEnd = time.time()
    timeSpend = timeEnd - timeStart
    
    # Show computation time
    show_text.insert('insert', "The OpenCV FFT algorithm spend " + str(timeSpend) + 
                     ' seconds processing the ' + str(imgGray.shape[0]) + " * " + str(imgGray.shape[1]) + " image")
    show_text.insert('insert', '\n')

    # Show Image
    plt.figure(figsize = (10,8))

    originalImgGray = plt.subplot(2,2,1)
    originalImgGray.imshow(imgGray, cmap ='gray')
    plt.title('Original Grayscale Image')

    ifftImage = plt.subplot(2,2,2) 
    ifftImage.imshow(ifftScale, cmap ='gray')
    plt.title('Inverse Fourier Transform')

    fftSpectrum = plt.subplot(2,2,3)
    fftSpectrum.imshow(fftShift_Spectrum, cmap ='gray')
    plt.title('Image Spectrum')
    
    fftPhase = plt.subplot(2,2,4)
    fftPhase.imshow(fftShift_Phase, cmap ='gray')
    plt.title('Image Phase Angle')

    plt.show()

def idealLowPass():
    # Set up variable
    fftShift = np.fft.fftshift(np.fft.fft2(imgGray))
    fftShift_IdealLowPass = np.copy(fftShift)
    R = 80
    cutRange = np.zeros(imgGray.shape[:2])

    # Do ideal lowpass
    for i in range(imgGray.shape[1]):
        for j in range(imgGray.shape[0]):
            if (i-centerX)*(i-centerX)+(j-centerY)*(j-centerY) > R*R:
                fftShift_IdealLowPass[j,i] = 0

    # IFFT
    idealLowPass_Spectrum = np.log(1+np.abs(fftShift_IdealLowPass))
    fftShift_IdealLowPass = np.fft.ifftshift(fftShift_IdealLowPass)
    idealLowPass_Img = np.abs(np.fft.ifft2(fftShift_IdealLowPass))

    # Show Data
    show_text.insert('insert', "Implement ideal low-pass filter")
    show_text.insert('insert', '\n')

    # Show Image
    plt.figure(figsize = (10,4))
    
    afterImgSpectrum = plt.subplot(1,2,1)
    afterImgSpectrum.imshow(idealLowPass_Spectrum, cmap ='gray')
    plt.title('Ideal low-pass spectrum')

    ifftImage = plt.subplot(1,2,2) 
    ifftImage.imshow(idealLowPass_Img, cmap ='gray')
    plt.title('Image after ideal low-pass')

    plt.show()

def idealHighPass():
    # Set up variable
    fftShift = np.fft.fftshift(np.fft.fft2(imgGray))
    fftShift_IdealHighPass = np.copy(fftShift)
    R = 80

    # Do ideal highpass
    for i in range(imgGray.shape[1]):
        for j in range(imgGray.shape[0]):
            if (i-centerX)*(i-centerX)+(j-centerY)*(j-centerY) <= R*R:
                fftShift_IdealHighPass[j,i] = 0

    # IFFT
    idealHighPass_Spectrum = np.log(1+np.abs(fftShift_IdealHighPass))
    fftShift_IdealHighPass = np.fft.ifftshift(fftShift_IdealHighPass)
    idealHighPass_Img = np.abs(np.fft.ifft2(fftShift_IdealHighPass))

    # Show Data
    show_text.insert('insert', "Implement ideal high-pass filter")
    show_text.insert('insert', '\n')

    # Show Image
    plt.figure(figsize = (10,4))
    
    afterImgSpectrum = plt.subplot(1,2,1)
    afterImgSpectrum.imshow(idealHighPass_Spectrum, cmap ='gray')
    plt.title('Ideal high-pass spectrum')

    ifftImage = plt.subplot(1,2,2) 
    ifftImage.imshow(idealHighPass_Img, cmap ='gray')
    plt.title('Image after ideal high-pass')

    plt.show()

def gaussianHighPass():
    # Set up variable
    fftShift = np.fft.fftshift(np.fft.fft2(imgGray))
    fftShift_GaussianHighPass = np.copy(fftShift)
    D0 = 80

    # Do gaussian highpass
    for i in range(imgGray.shape[1]):
        for j in range(imgGray.shape[0]):
            fftShift_GaussianHighPass[j,i] = fftShift_GaussianHighPass[j,i] * (1 - exp(-((i-centerX)*(i-centerX)+(j-centerY)*(j-centerY))/(2*(D0**2))))

    # IFFT
    gaussianHighPass_Spectrum = np.log(1+np.abs(fftShift_GaussianHighPass))
    fftShift_GaussianHighPass = np.fft.ifftshift(fftShift_GaussianHighPass)
    gaussianHighPass_Img = np.abs(np.fft.ifft2(fftShift_GaussianHighPass))

    # Show Data
    show_text.insert('insert', "Implement gaussian high-pass filter")
    show_text.insert('insert', '\n')

    # Show Image
    plt.figure(figsize = (10,4))
    
    afterImgSpectrum = plt.subplot(1,2,1)
    afterImgSpectrum.imshow(gaussianHighPass_Spectrum, cmap ='gray')
    plt.title('Gaussian high-pass spectrum')

    ifftImage = plt.subplot(1,2,2) 
    ifftImage.imshow(gaussianHighPass_Img, cmap ='gray')
    plt.title('Image after gaussian high-pass')

    plt.show()

def gaussianLowPass():
    # Set up variable
    fftShift = np.fft.fftshift(np.fft.fft2(imgGray))
    fftShift_GaussianLowPass = np.copy(fftShift)
    D0 = 80

    # Do gaussian highpass
    for i in range(imgGray.shape[1]):
        for j in range(imgGray.shape[0]):
            fftShift_GaussianLowPass[j,i] = fftShift_GaussianLowPass[j,i] * exp(-((i-centerX)*(i-centerX)+(j-centerY)*(j-centerY))/(2*(D0**2)))

    # IFFT
    gaussianLowPass_Spectrum = np.log(1+np.abs(fftShift_GaussianLowPass))
    fftShift_GaussianLowPass = np.fft.ifftshift(fftShift_GaussianLowPass)
    gaussianLowPass_Img = np.abs(np.fft.ifft2(fftShift_GaussianLowPass))

    # Show Data
    show_text.insert('insert', "Implement gaussian low-pass filter")
    show_text.insert('insert', '\n')

    # Show Image
    plt.figure(figsize = (10,4))
    
    afterImgSpectrum = plt.subplot(1,2,1)
    afterImgSpectrum.imshow(gaussianLowPass_Spectrum, cmap ='gray')
    plt.title('Gaussian low-pass spectrum')

    ifftImage = plt.subplot(1,2,2) 
    ifftImage.imshow(gaussianLowPass_Img, cmap ='gray')
    plt.title('Image after gaussian low-pass')

    plt.show()

def butterworthHighPass():
    # Set up variable
    fftShift = np.fft.fftshift(np.fft.fft2(imgGray))
    fftShift_butterworthHighPass = np.copy(fftShift)
    D0 = 80
    n = 5

    # Do gaussian highpass
    for i in range(imgGray.shape[1]):
        for j in range(imgGray.shape[0]):
            fftShift_butterworthHighPass[j,i] = fftShift_butterworthHighPass[j,i] * (1 - 1/(1 + (((i-centerX)*(i-centerX)+(j-centerY)*(j-centerY))/D0)**n))

    # IFFT
    butterworthHighPass_Spectrum = np.log(1+np.abs(fftShift_butterworthHighPass))
    fftShift_butterworthHighPass = np.fft.ifftshift(fftShift_butterworthHighPass)
    butterworthHighPass_Img = np.abs(np.fft.ifft2(fftShift_butterworthHighPass))

    # Show Data
    show_text.insert('insert', "Implement butterworth high-pass filter")
    show_text.insert('insert', '\n')

    # Show Image
    plt.figure(figsize = (10,4))
    
    afterImgSpectrum = plt.subplot(1,2,1)
    afterImgSpectrum.imshow(butterworthHighPass_Spectrum, cmap ='gray')
    plt.title('Butterworth high-pass spectrum')

    ifftImage = plt.subplot(1,2,2) 
    ifftImage.imshow(butterworthHighPass_Img, cmap ='gray')
    plt.title('Image after butterworth high-pass')

    plt.show()

def butterworthLowPass():
    # Set up variable
    fftShift = np.fft.fftshift(np.fft.fft2(imgGray))
    fftShift_butterworthLowPass = np.copy(fftShift)
    D0 = 80
    n = 5

    # Do gaussian highpass
    for i in range(imgGray.shape[1]):
        for j in range(imgGray.shape[0]):
            fftShift_butterworthLowPass[j,i] = fftShift_butterworthLowPass[j,i] * 1/(1 + (((i-centerX)*(i-centerX)+(j-centerY)*(j-centerY))/D0)**n)

    # IFFT
    butterworthLowPass_Spectrum = np.log(1+np.abs(fftShift_butterworthLowPass))
    fftShift_butterworthLowPass = np.fft.ifftshift(fftShift_butterworthLowPass)
    butterworthLowPass_Img = np.abs(np.fft.ifft2(fftShift_butterworthLowPass))

    # Show Data
    show_text.insert('insert', "Implement butterworth low-pass filter")
    show_text.insert('insert', '\n')

    # Show Image
    plt.figure(figsize = (10,4))
    
    afterImgSpectrum = plt.subplot(1,2,1)
    afterImgSpectrum.imshow(butterworthLowPass_Spectrum, cmap ='gray')
    plt.title('Butterworth low-pass spectrum')

    ifftImage = plt.subplot(1,2,2) 
    ifftImage.imshow(butterworthLowPass_Img, cmap ='gray')
    plt.title('Image after butterworth Low-pass')

    plt.show()

def homomorphic():
    # Set up variable
    fftShift = np.fft.fftshift(np.fft.fft2(imgGray))
    fftShift_homomorphic = np.copy(fftShift)
    if '/' in str(gammaH_.get()):
        gammaH_str = str(gammaH_.get()).split('/')
        gammaH = float(gammaH_str[0]) / float(gammaH_str[1])
    else :
        gammaH = int(gammaH_.get())

    if '/' in str(gammaL_.get()):
        gammaL__str = str(gammaL_.get()).split('/')
        gammaL = float(gammaL__str[0]) / float(gammaL__str[1])
    else :
        gammaL = int(gammaL_.get())

    if '/' in str(D0_.get()):
        D0_str = str(D0_.get()).split('/')
        D0 = float(D0_str[0]) / float(D0_str[1])
    else :
        D0 = int(D0_.get())
    c = 1

    # Do gaussian highpass
    for i in range(imgGray.shape[1]):
        for j in range(imgGray.shape[0]):
            fftShift_homomorphic[j,i] = fftShift_homomorphic[j,i] * ((gammaH - gammaL)*(1 - exp(-c*((i-centerX)*(i-centerX)+(j-centerY)*(j-centerY))/D0/D0)) + gammaL)

    # IFFT
    homomorphic_Spectrum = np.log(1+np.abs(fftShift_homomorphic))
    fftShift_homomorphic = np.fft.ifftshift(fftShift_homomorphic)
    homomorphic_Img = np.abs(np.fft.ifft2(fftShift_homomorphic))
    #homomorphic_Img = (homomorphic_Img - homomorphic_Img.min())*255/homomorphic_Img.max() # naormalize

    # Show Data
    show_text.insert('insert', "Implement homomorphic filter" + ", gammaH = " + str(gammaH) + ", gammaL = " + str(gammaL) + ", D0 = " + str(D0))
    show_text.insert('insert', '\n')

    # Show Image
    plt.figure(figsize = (10,4))
    
    afterImgSpectrum = plt.subplot(1,2,1)
    afterImgSpectrum.imshow(homomorphic_Spectrum, cmap ='gray')
    plt.title('Homomorphic spectrum')

    ifftImage = plt.subplot(1,2,2) 
    ifftImage.imshow(homomorphic_Img, cmap ='gray')
    plt.title('Image after homomorphic filter')

    plt.show()

def blurWiener():
    # Set up variable
    fftShift = np.fft.fftshift(np.fft.fft2(imgGray))
    fftShift_blur = np.copy(fftShift)

    # Do Motion Blur
    a = 0.1
    b = 0.1
    T = 1
    for i in range(0, imgGray.shape[0]):
        for j in range(0, imgGray.shape[1]):
            if i == 0 and j == 0 :
                fftShift_blur[i,j] = fftShift_blur[i,j] 
            else :
                motionBlur = sin(pi*(i*a + j*b))*T/(pi*(i*a + j*b))*cos(-pi*(i*a + j*b))
                fftShift_blur[i,j] = fftShift_blur[i,j] * motionBlur
    
    # IFFT
    fftShift_blur_ = np.fft.ifftshift(fftShift_blur)
    motionBlur_Img = np.abs(np.fft.ifft2(fftShift_blur_))

    # Show motion blur image
    plt.figure(figsize = (10,8))
    afterImg= plt.subplot(2,2,1)
    afterImg.imshow(motionBlur_Img, cmap ='gray')
    plt.title('Motion blur image')

    # Do inverse filter
    fftShift_blur_inverse = np.copy(fftShift_blur)
    for i in range(0, imgGray.shape[0]):
        for j in range(0, imgGray.shape[1]):
            if i == 0 and j == 0 :
                fftShift_blur_inverse[i,j] = fftShift_blur_inverse[i,j]
            else :
                motionBlur = sin(pi*(i*a + j*b))*T/(pi*(i*a + j*b))*cos(-pi*(i*a + j*b))
                fftShift_blur_inverse[i,j] = 1 / motionBlur * fftShift_blur_inverse[i,j]

    # Do wiener filter
    K = 0.001
    fftShift_blur_wiener = np.copy(fftShift_blur)
    for i in range(0, imgGray.shape[0]):
        for j in range(0, imgGray.shape[1]):
            if i == 0 and j == 0 :
                fftShift_blur_wiener[i,j] = fftShift_blur_wiener[i,j]
            else :
                motionBlur = sin(pi*(i*a + j*b))*T/(pi*(i*a + j*b))*cos(-pi*(i*a + j*b))
                fftShift_blur_wiener[i,j] = 1 / motionBlur * (motionBlur**2/(motionBlur**2 + K)) * fftShift_blur_wiener[i,j]

    # IFFT
    fftShift_blur_inverse = np.fft.ifftshift(fftShift_blur_inverse)
    blurInverse_Img = np.abs(np.fft.ifft2(fftShift_blur_inverse))
    fftShift_blur_wiener = np.fft.ifftshift(fftShift_blur_wiener)
    blurWiener_Img = np.abs(np.fft.ifft2(fftShift_blur_wiener))

    # Regulate
    blurInverse_Img = (blurInverse_Img - blurInverse_Img.min())*255/blurInverse_Img.max()
    blurWiener_Img = (blurWiener_Img - blurWiener_Img.min())*255/blurWiener_Img.max()
    compare_Img = blurWiener_Img - blurInverse_Img

    # Show Data
    show_text.insert('insert', "Add motion blur in image, and use wiener filter to reconstruct")
    show_text.insert('insert', '\n')

    # Show image 
    ifftImage_compare = plt.subplot(2,2,2) 
    ifftImage_compare.imshow(compare_Img, cmap ='gray')
    plt.title('Compare the difference between inverse & wiener filter')

    ifftImage_inverse = plt.subplot(2,2,3) 
    ifftImage_inverse.imshow(blurInverse_Img, cmap ='gray')
    plt.title('After inverse filter')

    ifftImage_wiener = plt.subplot(2,2,4) 
    ifftImage_wiener.imshow(blurWiener_Img, cmap ='gray')
    plt.title('After wiener filter')
    
    plt.show()

def blurNoiseWiener():
    # Set up variable
    fftShift = np.fft.fftshift(np.fft.fft2(imgGray))
    fftShift_blur = np.copy(fftShift)

    # Do Motion Blur
    a = 0.1
    b = 0.1
    T = 1
    for i in range(0, imgGray.shape[0]):
        for j in range(0, imgGray.shape[1]):
            if i == 0 and j == 0 :
                fftShift_blur[i,j] = fftShift_blur[i,j]
            else :
                motionBlur = sin(pi*(i*a + j*b))*T/(pi*(i*a + j*b))*cos(-pi*(i*a + j*b))
                fftShift_blur[i,j] = fftShift_blur[i,j] * motionBlur

    # IFFT
    fftShift_blur_ = np.fft.ifftshift(fftShift_blur)
    motionBlur_Img = np.abs(np.fft.ifft2(fftShift_blur_))

    # Add noise
    mean = 0
    variance = 20
    noise = np.random.normal(mean, variance, motionBlur_Img.size)
    noise = noise.reshape(imgGray.shape[0], imgGray.shape[1]).astype('uint8')
    motionBlurNoise_Img = motionBlur_Img*noise

    # Show Image
    plt.figure(figsize = (10,8))
    afterImg = plt.subplot(2,2,1)
    afterImg.imshow(motionBlurNoise_Img, cmap ='gray')
    plt.title('Motion blur and noise image')

    # Do inverse filter
    fftShift_blurNoise_inverse = np.fft.fftshift(np.fft.fft2(motionBlurNoise_Img))
    for i in range(0, imgGray.shape[0]):
        for j in range(0, imgGray.shape[1]):
            if i == 0 and j == 0 :
                fftShift_blurNoise_inverse[i,j] = fftShift_blurNoise_inverse[i,j]
            else :
                motionBlur = sin(pi*(i*a + j*b))*T/(pi*(i*a + j*b))*cos(-pi*(i*a + j*b))
                fftShift_blurNoise_inverse[i,j] = 1 / motionBlur * fftShift_blurNoise_inverse[i,j]
    
    # Do wiener filter
    K = 0.001
    fftShift_blurNoise_wiener = np.fft.fftshift(np.fft.fft2(motionBlurNoise_Img))
    for i in range(0, imgGray.shape[0]):
        for j in range(0, imgGray.shape[1]):
            if i == 0 and j == 0 :
                fftShift_blurNoise_wiener[i,j] = fftShift_blurNoise_wiener[i,j]
            else :
                motionBlur = sin(pi*(i*a + j*b))*T/(pi*(i*a + j*b))*cos(-pi*(i*a + j*b))
                fftShift_blurNoise_wiener[i,j] = 1 / motionBlur * (motionBlur**2/(motionBlur**2 + K)) * fftShift_blurNoise_wiener[i,j]

    # IFFT
    fftShift_blurNoise_inverse = np.fft.ifftshift(fftShift_blurNoise_inverse)
    blurNoiseInverse_Img = np.abs(np.fft.ifft2(fftShift_blurNoise_inverse))
    fftShift_blurNoise_wiener = np.fft.ifftshift(fftShift_blurNoise_wiener)
    blurNoiseWiener_Img = np.abs(np.fft.ifft2(fftShift_blurNoise_wiener))

    # Regulate
    blurNoiseInverse_Img = (blurNoiseInverse_Img - blurNoiseInverse_Img.min())*255/blurNoiseInverse_Img.max()
    blurNoiseWiener_Img = (blurNoiseWiener_Img - blurNoiseWiener_Img.min())*255/blurNoiseWiener_Img.max()
    compare_Img = blurNoiseInverse_Img - blurNoiseWiener_Img

    # Show Data
    show_text.insert('insert', "Add motion blur and gaussian noise in image, and use wiener filter to reconstruct")
    show_text.insert('insert', '\n')

    # Show Image
    ifftImage_compare = plt.subplot(2,2,2) 
    ifftImage_compare.imshow(compare_Img, cmap ='gray')
    plt.title('Compare the difference between inverse & wiener filter')

    ifftImage_inverese = plt.subplot(2,2,3) 
    ifftImage_inverese.imshow(blurNoiseInverse_Img, cmap ='gray')
    plt.title('After inverse filter')

    ifftImage_wiener = plt.subplot(2,2,4) 
    ifftImage_wiener.imshow(blurNoiseWiener_Img, cmap ='gray')
    plt.title('After wiener filter')

    plt.show()

# GUI
window = tk.Tk()
window.title('r11631006_hw4')
window.geometry('1024x512')

# Open Img Button
button_selectCSV = tk.Button(window, text = "Open Image", command = openImg)
button_selectCSV.place(x = 10, y = 10)

# FFT and IFFT Img Button
button_fftIfftImg = tk.Button(window, text = "FFT function", command = fftAndIfftImg)
button_fftIfftImg.place(x = 10, y = 40)

# Ideal Highpass
button_idealHighPass = tk.Button(window, text = "Ideal Highpass", command = idealHighPass)
button_idealHighPass.place(x = 10, y = 100)

# Ideal Lowpass
button_idealLowPass = tk.Button(window, text = "Ideal Lowpass", command = idealLowPass)
button_idealLowPass.place(x = 10, y = 130)

# Gaussian Highpass
button_gaussianHighPass = tk.Button(window, text = "Gaussian Highpass", command = gaussianHighPass)
button_gaussianHighPass.place(x = 10, y = 160)

# Gaussian Lowpass
button_gaussianLowPass = tk.Button(window, text = "Gaussian Lowpass", command = gaussianLowPass)
button_gaussianLowPass.place(x = 10, y = 190)

# Butterworth Highpass
button_butterworthHighPass = tk.Button(window, text = "Butterworth Highpass", command = butterworthHighPass)
button_butterworthHighPass.place(x = 10, y = 220)

# Butterworth Lowpass
button_butterworthLowPass = tk.Button(window, text = "Butterworth Lowpass", command = butterworthLowPass)
button_butterworthLowPass.place(x = 10, y = 250)

# User Input : GammaH of Homomorphic Filtering 
gammaH_frame = tk.Frame(window)
gammaH_frame.place(x = 10, y = 310)
gammaH_label = tk.Label(gammaH_frame, text = 'gammaH   ')
gammaH_label.pack(side = tk.LEFT)
gammaH_ = tk.Entry(gammaH_frame, width = 10)
gammaH_.pack()

# User Input : GammaL of Homomorphic Filtering 
gammaL_frame = tk.Frame(window)
gammaL_frame.place(x = 10, y = 330)
gammaL_label = tk.Label(gammaL_frame, text = 'gammaL    ')
gammaL_label.pack(side = tk.LEFT)
gammaL_ = tk.Entry(gammaL_frame, width = 10)
gammaL_.pack()

# User Input : D0 of Homomorphic Filtering 
D0_frame = tk.Frame(window)
D0_frame.place(x = 10, y = 350)
D0_label = tk.Label(D0_frame, text = 'D0               ')
D0_label.pack(side = tk.LEFT)
D0_ = tk.Entry(D0_frame, width = 10)
D0_.pack()

# Homomorphic Filtering 
button_homomorphic = tk.Button(window, text = "Homomorphic Filter", command = homomorphic)
button_homomorphic.place(x = 10, y = 380)

# Blur and Wiener
button_blurWiner = tk.Button(window, text = "Blur", command = blurWiener)
button_blurWiner.place(x = 10, y = 440)

# Blur, Noise and Wiener
button_blurNoiseWiener = tk.Button(window, text = "Blur + Noise", command = blurNoiseWiener)
button_blurNoiseWiener.place(x = 10, y = 470)

# Show Text
show_text = tk.Text(window, height = 40, width = 120)
show_text.place(x = 175, y = 10)

window.mainloop()