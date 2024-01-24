import cv2
def To_Gray_Main(image ,arr_ROIs) : 
    Gray_Image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    Gray_Image = cv2.cvtColor(Gray_Image, cv2.COLOR_GRAY2RGB)
    
    return Gray_Image , arr_ROIs