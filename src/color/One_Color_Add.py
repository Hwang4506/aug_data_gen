import cv2
def One_Color_Add_Main(image ,arr_ROIs , parameter = ('r',0)) : 
    Blue_Color = image[:,:,0]
    Green_Color = image[:,:,1]
    Red_Color = image[:,:,2]

    value = 0
    if parameter[1] >= 0 :
        value = parameter[1]

    elif parameter[1] < 0 :
        value = -parameter[1]



    if parameter[0] == 'B' or parameter[0] == 'b' :
        if parameter[1] >= 0 :
            Blue_Color = cv2.add(Blue_Color,value)
        elif parameter[1]< 0 :
            Blue_Color = cv2.subtract(Blue_Color,value)

    elif parameter[0] == 'G' or parameter[0] == 'g' :
        if parameter[1] >= 0 :
            Green_Color = cv2.add(Green_Color,value)
        elif parameter[1]< 0 :
            Green_Color = cv2.subtract(Green_Color,value)

    elif parameter[0] == 'R' or parameter[0] == 'r' :
        if parameter[1] >= 0 :
            Red_Color = cv2.add(Red_Color,value)
        elif parameter[1]< 0 :
            Red_Color = cv2.subtract(Red_Color,value)

    Color_Add_Image = cv2.merge((Blue_Color, Green_Color, Red_Color))
    return Color_Add_Image , arr_ROIs
