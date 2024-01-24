import cv2
import numpy as np

def Poisson_Main(image , arr_ROIs) :
    vals = len(np.unique(image))
    vals = 2 ** np.ceil(np.log2(vals))
    poissonNoise = np.random.poisson(image*vals)/float(vals)
    poissonNoise = poissonNoise.astype('uint8')
    return poissonNoise , arr_ROIs