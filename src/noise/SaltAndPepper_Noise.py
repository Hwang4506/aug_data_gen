import cv2
import numpy as np

def SaltAndPepper_Main(image,arr_ROIs, parameter = (0, 0) ) :

    SaltAndPepper_Image = image.copy()

    Blue_Color = SaltAndPepper_Image[:,:,0]
    Green_Color = SaltAndPepper_Image[:,:,1]
    Red_Color = SaltAndPepper_Image[:,:,2]

    if parameter[0] > 25 :
        parameter[0] = 25
    
    if parameter[1] < 0 :
        parameter[1] =0

    if parameter[1] > 100 :
        parameter[1] = 100


    salt_vs_pepper = parameter[1]/100
        
    fAmount = parameter[0]/1000        # 추가될 노이즈의 량을 나타낸다. 0.001 ~ 0.025 정도를 추천한다.

    num_salt = np.ceil(fAmount * image.size * salt_vs_pepper )
    num_pepper = np.ceil(fAmount * image.size * (1-salt_vs_pepper)  )

    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in Blue_Color.shape]
    Blue_Color[coords[0], coords[1]] = 0
    Green_Color[coords[0], coords[1]] = 0
    Red_Color[coords[0], coords[1]] = 0
    
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in Blue_Color.shape]
    Blue_Color[coords[0], coords[1]] = 255
    Green_Color[coords[0], coords[1]] = 255
    Red_Color[coords[0], coords[1]] = 255

    SaltAndPepper_Image = cv2.merge((Blue_Color, Green_Color, Red_Color))
    
    return SaltAndPepper_Image,arr_ROIs
