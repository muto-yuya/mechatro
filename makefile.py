import cv2
import numpy as np



def cos(a,b):
    norm1 = np.sqrt(np.sum(a**2))
    norm2 = np.sqrt(np.sum(b**2))
    return np.dot(a,b)/(norm1*norm2)

samples_length = 37
dives = np.empty((0,784))
divs = np.empty((0,784))
divs = np.empty((0,784))
divs = np.empty((0,784))


def slide_up(filename,num,outputfilename):
    file = cv2.imread(filename)
    file = np.array(file)
    newfile = np.append(file,np.ones((num,28,3))*255,axis=0)[num:]
    print(newfile.shape)
    cv2.imwrite(outputfilename, newfile);


def slide_down(filename,num,outputfilename):
    file = cv2.imread(filename)
    file = np.array(file)
    newfile = np.append(np.ones((num,28,3))*255,file,axis=0)[:-num]
    print(newfile.shape)
    cv2.imwrite(outputfilename, newfile)


def slide_right(filename,num,outputfilename):
    file = cv2.imread(filename)
    file = np.array(file)
    newfile = np.append(np.ones((28,num,3))*255,file,axis=1)[:,:-num]
    print(newfile.shape)
    cv2.imwrite(outputfilename, newfile)


def slide_left(filename,num,outputfilename):
    file = cv2.imread(filename)
    file = np.array(file)
    newfile = np.append(file,np.ones((28,num,3))*255,axis=1)[:,num:]
    print(newfile.shape)
    cv2.imwrite(outputfilename, newfile)

slide_left("test_001.bmp",5,"out2.bmp")


def strnum_make(i):
    if i < 10:
        strnum = "00"+str(i)
    elif i < 100:
        strnum = "0"+str(i)
    else:
        strnum = str(i)
    return  strnum


for i in range(0,samples_length):
    slide_up("div/div_"+strnum_make(i)+".bmp",1,"div/div_"+strnum_make(12*i+samples_length+1)+".bmp")
    slide_up("div/div_"+strnum_make(i)+".bmp",2,"div/div_"+strnum_make(12*i+samples_length+1+1)+".bmp")
    slide_up("div/div_"+strnum_make(i)+".bmp",3,"div/div_"+strnum_make(12*i+samples_length+1+2)+".bmp")
    slide_down("div/div_"+strnum_make(i)+".bmp",1,"div/div_"+strnum_make(12*i+samples_length+1+3)+".bmp")
    slide_down("div/div_"+strnum_make(i)+".bmp",2,"div/div_"+strnum_make(12*i+samples_length+1+4)+".bmp")
    slide_down("div/div_"+strnum_make(i)+".bmp",3,"div/div_"+strnum_make(12*i+samples_length+1+5)+".bmp")
    slide_right("div/div_"+strnum_make(i)+".bmp",1,"div/div_"+strnum_make(12*i+samples_length+1+6)+".bmp")
    slide_right("div/div_"+strnum_make(i)+".bmp",2,"div/div_"+strnum_make(12*i+samples_length+1+7)+".bmp")
    slide_right("div/div_"+strnum_make(i)+".bmp",3,"div/div_"+strnum_make(12*i+samples_length+1+8)+".bmp")
    slide_left("div/div_"+strnum_make(i)+".bmp",1,"div/div_"+strnum_make(12*i+samples_length+1+9)+".bmp")
    slide_left("div/div_"+strnum_make(i)+".bmp",2,"div/div_"+strnum_make(12*i+samples_length+1+10)+".bmp")
    slide_left("div/div_"+strnum_make(i)+".bmp",3,"div/div_"+strnum_make(12*i+samples_length+1+11)+".bmp")