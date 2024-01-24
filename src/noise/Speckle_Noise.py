import cv2
import numpy as np
def Speckle_Main(image ,arr_ROIs) :

    GaussNoise = np.random.normal(0,1,image.size)
    GaussNoise = GaussNoise.reshape(image.shape[0],image.shape[1],image.shape[2]).astype('uint8')

    Speckle_Image = cv2.add(image,image*GaussNoise)
    return Speckle_Image , arr_ROIs
