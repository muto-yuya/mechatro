import numpy as np
import cv2

file = cv2.imread("largeSize.bmp")
file = cv2.resize(file,(28,28))
cv2.imshow("test",file)
cv2.imwrite("samllSize.bmp",file)