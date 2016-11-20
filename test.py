import cv2
import numpy as np
from scipy import stats
def image_convert(filename):
    file = cv2.imread(filename)
    file = np.array(file[:,:,0]).flatten()
    file = (255-file)/100
    return file


def cos(a,b):
    norm1 = np.sqrt(np.sum(a**2))
    norm2 = np.sqrt(np.sum(b**2))
    return np.dot(a,b)/(norm1*norm2)


def strnum_make(i):
    if i < 10:
        strnum = "00"+str(i)
    elif i < 100:
        strnum = "0"+str(i)
    else:
        strnum = str(i)
    return strnum


samples_length = 482
pluses = np.empty((0,784))
subs = np.empty((0,784))
multis = np.empty((0,784))
divs = np.empty((0,784))

for i in range(0,samples_length):
    print(i)
    img_plus = image_convert("plus/plus_"+strnum_make(i)+".bmp")
    img_sub = image_convert("sub/sub_"+strnum_make(i)+".bmp")
    img_multi = image_convert("multi/multi_"+strnum_make(i)+".bmp")
    img_div = image_convert("div/div_"+strnum_make(i)+".bmp")

    pluses = np.append(pluses,np.array([img_plus]),axis=0)
    subs = np.append(subs,np.array([img_sub]),axis=0)
    multis = np.append(multis,np.array([img_multi]),axis=0)
    divs = np.append(divs,np.array([img_div]),axis=0)

all_X = np.append(pluses,subs,axis=0)
all_X = np.append(all_X,multis,axis=0)
all_X = np.append(all_X,divs,axis=0)
all_y = np.append(np.ones(samples_length)*0,np.ones(samples_length)*1)
all_y = np.append(all_y,np.ones(samples_length)*2)
all_y = np.append(all_y,np.ones(samples_length)*3)


test_x = cv2.imread("test_009.bmp")
test_x = np.array(test_x[:,:,0]).flatten()
test_x = np.abs(test_x-255)/255.0


distance = [cos(test_x,all_X[i]) for i in range(0,samples_length*4)]
print(distance)
print(all_y[np.argsort(distance)][-10::])
mode = stats.mode(all_y[np.argsort(distance)][-3:])
mode = int(mode[0])

if mode == 0:
    print("これは　+")
elif mode == 1:
    print("これは　-")
elif mode == 2:
    print("これは　*")
elif mode == 3:
    print("これは　/")



