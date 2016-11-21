import cv2
import numpy as np
from scipy import ndimage


samples_length = 20



def rotate180(filename,outputfilename):
    file = cv2.imread(filename)
    file = np.array(file)
    file = ndimage.rotate(file, 90, reshape=True)
    file = ndimage.rotate(file, 90, reshape=True)
    cv2.imwrite(outputfilename, file)


def upsidedown(filename,outputfilename):
    file = cv2.imread(filename)
    file = np.array(file)
    file = np.flipud(file)
    cv2.imwrite(outputfilename, file)


def rightleft(filename,outputfilename):
    file = cv2.imread(filename)
    file = np.array(file)
    file = np.fliplr(file)
    cv2.imwrite(outputfilename, file)

def strnum_make(i):
    if i < 10:
        strnum = "00"+str(i)
    elif i < 100:
        strnum = "0"+str(i)
    else:
        strnum = str(i)
    return  strnum


for i in range(0,samples_length):
    rotate180("div/div_"+strnum_make(i)+".bmp","div/div_"+strnum_make(3*i+samples_length)+".bmp")
    upsidedown("div/div_"+strnum_make(i)+".bmp","div/div_"+strnum_make(3*i+samples_length+1)+".bmp")
    rightleft("div/div_"+strnum_make(i)+".bmp","div/div_"+strnum_make(3*i+samples_length+2)+".bmp")