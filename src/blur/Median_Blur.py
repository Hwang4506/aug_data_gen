import cv2

def Median_Bulr_Main(image , arr_ROIs , parameter = 5) : # parameter = 홀수 1개 5~15 추천
    
    
    if parameter < 3 :
        parameter = 3

    elif parameter > 7 :
        parameter = 7
    
    if (parameter % 2) == 0 :
        parameter -= 1


    MedianBulr_Image = cv2.medianBlur(image, parameter)
    return MedianBulr_Image , arr_ROIs
