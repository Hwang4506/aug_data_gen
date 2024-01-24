import cv2
def Channel_Shuffle_Main(image, arr_ROIs , parameter = 'rgb') :
    height,weight, = image.shape[:2]
    Blue_Color = image[:,:,0]
    Green_Color = image[:,:,1]
    Red_Color = image[:,:,2]
    Channel_Shuffle_image = None

    if parameter == 'BGR' or parameter == 'bgr' :
        Channel_Shuffle_image = cv2.merge((Blue_Color, Green_Color, Red_Color))

    elif parameter == 'BRG' or parameter == 'brg' :
        Channel_Shuffle_image = cv2.merge((Blue_Color, Red_Color, Green_Color))

    elif parameter == 'GBR' or parameter == 'gbr' :
        Channel_Shuffle_image = cv2.merge((Green_Color, Blue_Color, Red_Color))

    elif parameter == 'GRB' or parameter == 'grb' :
        Channel_Shuffle_image = cv2.merge((Green_Color, Red_Color, Blue_Color))

    elif parameter == 'RBG' or parameter == 'rbg' :
        Channel_Shuffle_image = cv2.merge((Red_Color, Blue_Color, Green_Color))

    elif parameter == 'RGB' or parameter == 'rgb' :
        Channel_Shuffle_image = cv2.merge((Red_Color, Green_Color, Blue_Color))
    

    return Channel_Shuffle_image , arr_ROIs