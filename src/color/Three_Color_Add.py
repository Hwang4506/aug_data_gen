import cv2
def Three_Color_Add_Main(image , arr_ROIs , parameter = (0,0,0)) :
    Blue_Color = image[:,:,0]
    Green_Color = image[:,:,1]
    Red_Color = image[:,:,2]

    if parameter[0] >= 0 :
        Blue_Color = cv2.add(Blue_Color,parameter[0])
    elif parameter[0] < 0 :
        Blue_Color = cv2.subtract(Blue_Color,-parameter[0])


    if parameter[1] >= 0 :
        Green_Color = cv2.add(Green_Color,parameter[1])
    elif parameter[1] < 0 :
        Green_Color = cv2.subtract(Green_Color,-parameter[1])


    if parameter[2] >= 0 :
        Red_Color = cv2.add(Red_Color,parameter[2])
    elif parameter[2] < 0 :
        Red_Color = cv2.subtract(Red_Color,-parameter[2])

    Color_Add_Image = cv2.merge((Blue_Color, Green_Color, Red_Color))

    return Color_Add_Image , arr_ROIs