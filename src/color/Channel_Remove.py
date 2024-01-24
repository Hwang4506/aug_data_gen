import cv2
import numpy as np
def Channel_Remove_Main(image , arr_ROIs , parameter = 'b') : 
    height,weight, = image.shape[:2]
    zero =np.zeros((height,weight,1), dtype=np.uint8)
    Blue_Color = image[:,:,0]
    Green_Color = image[:,:,1]
    Red_Color = image[:,:,2]

    if parameter[0] == 'B' or parameter[0] == 'b' :
        Blue_Color = zero

    elif parameter[0] == 'G' or parameter[0] == 'g' :
        Green_Color = zero
        
    elif parameter[0] == 'R' or parameter[0] == 'r' :
        Red_Color = zero
        

    Color_Remove_Image = cv2.merge((Blue_Color, Green_Color, Red_Color))
    
    return Color_Remove_Image , arr_ROIs