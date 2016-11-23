import cv2
import numpy as np


def separate_letter(filename):
    file = (cv2.imread(filename))
    file_array = np.array(file[:,:,0])
    file_array = (255-file_array)
    sumArr = np.sum(file_array,axis=0)

    boarder = []
    for i in range(0,sumArr.shape[0]-1):
        if sumArr[i] == 0 and sumArr[i+1] != 0:
            boarder.append(i)
        elif sumArr[i] != 0 and sumArr[i+1] == 0:
            boarder.append(i)

    def treatboarderLeft(boarderP):
        if boarderP - 15 < 0:
            return 0
        else:
            return boarderP -15

    def treatboarderRight(boarderP):
        if boarderP + 15 > file.shape[1]:
            return file.shape[1]
        else:
            return boarderP + 15

    boarderA = int((boarder[0]+boarder[1])/2)
    boarderB = int((boarder[2]+boarder[3])/2)
    boarderC = int((boarder[4]+boarder[5])/2)
    file1 = file[:,treatboarderLeft(boarderA):boarderA+15,:]
    file2 = file[:,boarderB-15:boarderB+15,:]
    file3 = file[:,boarderC-15:treatboarderRight(boarderC),:]

    file1_s = cv2.resize(file1,(28,28))
    file2_s = cv2.resize(file2,(28,28))
    file3_s = cv2.resize(file3,(28,28))

    cv2.imwrite('file1.bmp',file1_s)
    cv2.imwrite('file2.bmp',file2_s)
    cv2.imwrite('file3.bmp',file3_s)

    return file1_s,file2_s,file3_s
