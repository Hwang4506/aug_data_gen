import cv2
def Two_Color_Add_Main(image ,arr_ROIs , parameter = ('br',0,0)) :
    Blue_Color = image[:,:,0]
    Green_Color = image[:,:,1]
    Red_Color = image[:,:,2]

    value1 = 0
    value2 = 0
    if parameter[1] >= 0 :
        value1 = parameter[1]
    elif parameter[1] < 0 :
        value1 = -parameter[1]

    if parameter[2] >= 0 :
        value2 = parameter[2]

    elif parameter[2] < 0 :
        value2 = -parameter[2]


    if parameter[0] == 'BG' or parameter[0] == 'bg' :
        if parameter[1] >= 0 :
            Blue_Color = cv2.add(Blue_Color,value1)
        elif parameter[1] < 0 :
            Blue_Color = cv2.subtract(Blue_Color,value1)
        
        if parameter[2] >= 0 :
            Green_Color = cv2.add(Green_Color,value2)
        elif parameter[2] < 0 :
            Green_Color = cv2.subtract(Green_Color,value2)
        

    elif parameter[0] == 'BR' or parameter[0] == 'br' :
        if parameter[1] >= 0 :
            Blue_Color = cv2.add(Blue_Color,value1)
        elif parameter[1] < 0 :
            Blue_Color = cv2.subtract(Blue_Color,value1)

        if parameter[2] >= 0 :
            Red_Color = cv2.add(Red_Color,value2)
        elif parameter[2] < 0 :
            Red_Color = cv2.subtract(Red_Color,value2)
        

    elif parameter[0] == 'GR' or parameter[0] == 'gr' :
        if parameter[1] >= 0 :
            Green_Color = cv2.add(Green_Color,value1)
        elif parameter[1] < 0 :
            Green_Color = cv2.subtract(Green_Color,value1)

        if parameter[2] >= 0 :
            Red_Color = cv2.add(Red_Color,value2)
        elif parameter[2] < 0 :
            Red_Color = cv2.subtract(Red_Color,value2)

    Color_Add_Image = cv2.merge((Blue_Color, Green_Color, Red_Color))
    
    return Color_Add_Image , arr_ROIs
