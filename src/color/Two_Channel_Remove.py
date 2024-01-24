import cv2
import numpy as np
def Two_Channel_Remove_Main(image , arr_ROIs , parameter='br') : 
    height,weight, = image.shape[:2]
    zero =np.zeros((height,weight,1), dtype=np.uint8)
    Blue_Color = image[:,:,0]
    Green_Color = image[:,:,1]
    Red_Color = image[:,:,2]

    if parameter == 'BG' or parameter == 'bg' :
        Blue_Color = zero
        Green_Color = zero

    elif parameter == 'BR' or parameter == 'br' :
        Blue_Color = zero
        Red_Color = zero

    elif parameter == 'GR' or parameter == 'gr' :
        Green_Color = zero
        Red_Color = zero

    Two_Color_Remove_Image = cv2.merge((Blue_Color, Green_Color, Red_Color))
    
    return Two_Color_Remove_Image , arr_ROIs