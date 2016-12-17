import cv2
import numpy as np
import time
from serial import Serial
import struct
import os

def extract_color( src, h_th_low, h_th_up, s_th, v_th ):

    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    if h_th_low > h_th_up:
        ret, h_dst_1 = cv2.threshold(h, h_th_low, 255, cv2.THRESH_BINARY)
        ret, h_dst_2 = cv2.threshold(h, h_th_up,  255, cv2.THRESH_BINARY_INV)

        dst = cv2.bitwise_or(h_dst_1, h_dst_2)

    else:
        ret, dst = cv2.threshold(h,   h_th_low, 255, cv2.THRESH_TOZERO)
        ret, dst = cv2.threshold(dst, h_th_up,  255, cv2.THRESH_TOZERO_INV)

        ret, dst = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY)

    ret, s_dst = cv2.threshold(s, s_th, 255, cv2.THRESH_BINARY)
    ret, v_dst = cv2.threshold(v, v_th, 255, cv2.THRESH_BINARY)

    dst = cv2.bitwise_and(dst, s_dst)
    dst = cv2.bitwise_and(dst, v_dst)

    return dst

def x_yConvert(cameraX,cameraY):
    x = int(((cameraX-50)*1.3)/3.376)
    y = int((cameraY-(cameraY-400)/250.0*(cameraX-300)/300.0*30-180)/3.376)

    if x < 0:
        x = 0
    elif x > 185:
        x = 185
    if y < 0:
        y = 0
    elif y > 130:
        y = 130
    print(x,y)
    return x,y
os.system('nohup python /Users/mutouyuuya/UTLecture/mechatroPy3.5/music.py &')
cap = cv2.VideoCapture(0)
com = Serial(port="/dev/cu.usbmodem1421",baudrate=9600,timeout=1)
time.sleep(5)
width = 8
ret, frame = cap.read()

#frameを表示
frame = np.array(frame)

red = [160,10]
yellow = [15,35]
green = [40,100]
blue = [100,120]
color = green
newframe = frame[200:900,200:900,:]
result = extract_color(newframe,color[0],color[1],70,70) #red 180-10,70,70 #green 50,70,70,70 #blue 100,130,70,70

cameraY = (np.argmax(np.sum(result,axis=0)))
cameraX = (np.argmax(np.sum(result,axis=1)))
print(cameraX)
print(cameraY)
newframe[int(np.argmax(np.sum(result,axis=1))),:] = 0
newframe[:,int(np.argmax(np.sum(result,axis=0)))] = 0

x,y = x_yConvert(cameraX,cameraY)
if x <10:
    strX = "00"+str(x)
elif x <100:
    strX = "0"+str(x)
else:
    strX = str(x)
if y <10:
    strY = "00"+str(y)
elif y <100:
    strY = "0"+str(y)
else:
    strY = str(y)
com.write(strX.encode('utf-8'))

com.write(strY.encode('utf-8'))
print(newframe.shape)
cv2.imshow('camera capture', newframe)
cv2.imshow('result',result)
cap.release()
time.sleep(0.5)
#10msecキー入力待ち
k = cv2.waitKey(0)

#キャプチャを終了
cv2.destroyAllWindows()


