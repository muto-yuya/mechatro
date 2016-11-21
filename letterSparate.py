import cv2
import numpy as np


def separate_letter(filename):
    file = (cv2.imread(filename))
    file_array = np.array(file[:,:,0])
    file_array = (255-file_array)
    sumArr = np.sum(file_array,axis=0)
    print(sumArr)

    boarder = []
    for i in range(0,sumArr.shape[0]-1):
        if sumArr[i] == 0 and sumArr[i+1] != 0:
            boarder.append(i)
        elif sumArr[i] != 0 and sumArr[i+1] == 0:
            boarder.append(i)
    print(boarder)
    boarderA = int((boarder[1]+boarder[2])/2)
    boarderB = int((boarder[3]+boarder[4])/2)

    file1 = file[:,0:boarderA,:]
    file2 = file[:,boarderA:boarderB,:]
    file3 = file[:,boarderB:,:]

    file1_s = cv2.resize(file1,(28,28))
    file2_s = cv2.resize(file2,(28,28))
    file3_s = cv2.resize(file3,(28,28))
    print(file1.shape)
    print(file2.shape)
    print(file3.shape)

    cv2.imwrite('file1.bmp',file1_s)
    cv2.imwrite('file2.bmp',file2_s)
    cv2.imwrite('file3.bmp',file3_s)

    return file1_s,file2_s,file3_s

separate_letter("Toseparate.bmp")