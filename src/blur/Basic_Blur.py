import cv2

def Basic_Blur_Main(image ,arr_ROIs , parameter = (5,5)) : # parameter = ((BlurSizeX,BlurSizeY)) 5~ 20 추천

    parameter = list(parameter)

    if parameter[0] < 5 :
        parameter[0] = 5

    elif parameter[0] > 15 :
        parameter[0] = 15

    if parameter[1] < 5 :
        parameter[1] = 5

    elif parameter[1] >15 :
        parameter[1] = 15

    parameter = tuple(parameter)


    Blur_Image = cv2.blur(image,parameter)
    return Blur_Image , arr_ROIs
