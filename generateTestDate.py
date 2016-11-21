import cv2
import numpy as np


def image_convert(filename):
    file = cv2.imread(filename)
    file = np.array(file[:,:,0]).flatten()
    file = (255-file)/255
    return file

test_X = np.array([#image_convert("test_000.bmp"),
#                    image_convert("test_001.bmp"),
#                    image_convert("test_002.bmp"),
#                    image_convert("test_003.bmp"),
#                    image_convert("test_004.bmp"),
#                    image_convert("test_005.bmp"),
#                    image_convert("test_006.bmp"),
#                    image_convert("test_007.bmp"),
#                    image_convert("test_008.bmp"),
                    image_convert("test_009.bmp")]).astype('float32')

np.save('test_X.npy',test_X)
