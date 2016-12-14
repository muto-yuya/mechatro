import cv2
import numpy as np
import time
from serial import Serial
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

#os.system('nohup python /Users/mutouyuuya/UTLecture/mechatroPy3.5/music.py &')
cap = cv2.VideoCapture(0)
#com = Serial(port="/dev/cu.usbmodem1421",baudrate=9600,timeout=1)
time.sleep(2)
width = 8
ret, frame = cap.read()
#frameを表示
frame = np.array(frame)
red = [180,10]
green = [50,70]
blue = [100,130]
color = green
newframe = frame[200:900,200:900,:]
result = extract_color(newframe,color[0],color[1],70,70) #red 180-10,70,70 #green 50,70,70,70 #blue 100,130,70,70
print(np.argmax(np.sum(result,axis=0)))
print(np.argmax(np.sum(result,axis=1)))

#newframe[int(np.argmax(np.sum(result,axis=1))),:] = 0
#newframe[:,int(np.argmax(np.sum(result,axis=0)))] = 0
newframe[280,:] = 0 #上下x
newframe[:,180] = 0 #左右y
#kiritori frame 200-900,200-900

if np.argmax(np.sum(result,axis=1))>350:
    if np.argmax(np.sum(result,axis=0))>350:
        #com.write(b"b")
        print("2b") #カメラ右下
    else:
        #com.write(b"c")
        print("3c") #カメラ左下
else:
    if np.argmax(np.sum(result,axis=0))>350:
        #com.write(b"a")
        print("1a") #カメラ右上
    else:
        #com.write(b"d")
        print("4d") #カメラ左上

print(newframe.shape)
cv2.imshow('camera capture', newframe)
cv2.imshow('result',result)
cap.release()
time.sleep(0.5)
#10msecキー入力待ち
k = cv2.waitKey(0)

#キャプチャを終了
cv2.destroyAllWindows()