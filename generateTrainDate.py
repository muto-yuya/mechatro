import cv2
from sklearn.utils import shuffle
from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams

import numpy as np

trng = RandomStreams(42)
rng = np.random.RandomState(1234)


def image_convert(filename):
    file = cv2.imread(filename)
    file = np.array(file[:,:,0]).flatten()
    file = (255-file)/255
    return file


def strnum_make(i):
    if i < 10:
        strnum = "00"+str(i)
    elif i < 100:
        strnum = "0"+str(i)
    else:
        strnum = str(i)
    return strnum


#read +-*/files
samples_length = 1000
pluses = np.empty((0,784))
subs = np.empty((0,784))
multis = np.empty((0,784))
divs = np.empty((0,784))

for i in range(0,samples_length):
    img_plus = image_convert("plus/plus_"+strnum_make(i)+".bmp")
    img_sub = image_convert("sub/sub_"+strnum_make(i)+".bmp")
    img_multi = image_convert("multi/multi_"+strnum_make(i)+".bmp")
    img_div = image_convert("div/div_"+strnum_make(i)+".bmp")

    pluses = np.append(pluses,np.array([img_plus]),axis=0)
    subs = np.append(subs,np.array([img_sub]),axis=0)
    multis = np.append(multis,np.array([img_multi]),axis=0)
    divs = np.append(divs,np.array([img_div]),axis=0)

train_X = np.append(pluses,subs,axis=0)
train_X = np.append(train_X,multis,axis=0)
train_X = np.append(train_X,divs,axis=0)
train_y = np.append(np.ones(samples_length)*0,np.ones(samples_length)*1)
train_y = np.append(train_y,np.ones(samples_length)*2)
train_y = np.append(train_y,np.ones(samples_length)*3)
train_X,train_y = shuffle(train_X.astype('float32'),train_y.astype('int32'))
train_y = np.eye(4)[train_y]

np.save('train_X.npy',train_X)
np.save('train_y.npy',train_y)


