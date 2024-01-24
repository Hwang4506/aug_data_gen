import cv2
import numpy as np
def All_Color_Add_Main(image ,arr_ROIs , parameter=0) : 

    value = 0
    if parameter >= 0 :
        value = parameter

    elif parameter < 0 :
        value = -parameter
        

    array = np.full(image.shape,(value,value,value), dtype=np.uint8)
    All_Add_image = None
    
    if parameter >= 0 :
        All_Add_image = cv2.add(image,array)

    elif parameter < 0 :
        All_Add_image = cv2.subtract(image,array)


    return All_Add_image , arr_ROIs