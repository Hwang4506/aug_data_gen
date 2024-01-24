import cv2
import numpy as np

def Gaussian_Main(image, arr_ROIs) :
    GaussNoise = np.random.normal(0,1,image.size)
    GaussNoise = GaussNoise.reshape(image.shape[0],image.shape[1],image.shape[2]).astype('uint8')
    GaussNoise_Image = cv2.add(image,GaussNoise)
    return GaussNoise_Image , arr_ROIs
