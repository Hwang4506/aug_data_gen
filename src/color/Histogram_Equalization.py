import cv2
def Histogram_Equalization_Main(image, arr_ROIs , parameter='r') : # strRGB 아래 7개
    
    Blue_Color = image[:, :, 0] # 파란색 채널
    Green_Color = image[:, :, 1] # 초록색 채널
    Red_Color = image[:, :, 2] # 빨간색 채널


    blue_eq_ch = cv2.equalizeHist(Blue_Color)
    green_eq_ch = cv2.equalizeHist(Green_Color)
    red_eq_ch = cv2.equalizeHist(Red_Color)

    if parameter == 'b' :
        Blue_Color = cv2.equalizeHist(Blue_Color)

    elif parameter == 'g' :
        Green_Color = cv2.equalizeHist(Green_Color)

    elif parameter == 'r' :
        Red_Color = cv2.equalizeHist(Red_Color)

    elif parameter == 'bg' :
        Blue_Color = cv2.equalizeHist(Blue_Color)
        Green_Color = cv2.equalizeHist(Green_Color)

    elif parameter == 'br' :
        Blue_Color = cv2.equalizeHist(Blue_Color)
        Red_Color = cv2.equalizeHist(Red_Color)

    elif parameter == 'gr' :
        Green_Color = cv2.equalizeHist(Green_Color)
        Red_Color = cv2.equalizeHist(Red_Color)
    
    elif parameter == 'bgr' :
        Blue_Color = cv2.equalizeHist(Blue_Color)
        Green_Color = cv2.equalizeHist(Green_Color)
        Red_Color = cv2.equalizeHist(Red_Color)
    
    
    
    EQ_Image = cv2.merge((Blue_Color, Green_Color, Red_Color))

    return EQ_Image , arr_ROIs