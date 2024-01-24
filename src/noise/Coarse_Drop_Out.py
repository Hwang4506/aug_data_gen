import cv2
import numpy as np
import math

def get_filter( Ysize , Xsize , filterColor ) :
    Return_Image = np.zeros((Ysize+1, Xsize+1,3), dtype=np.uint8)
    Black_Image = np.zeros((Ysize+1, Xsize+1,3), dtype=np.uint8)

    Blue_Color = Return_Image[:,:,0]
    Green_Color = Return_Image[:,:,1]
    Red_Color = Return_Image[:,:,2]

    num_salt = np.ceil( 1 * Return_Image.size * 0.5 )
    num_pepper = np.ceil( 1 * Return_Image.size * 0.5 )


    if filterColor == "BLACK" or filterColor == "b" :
        Return_Image = Black_Image

    elif filterColor == "SP" or filterColor == "sp" :
        coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in Blue_Color.shape]
        Blue_Color[coords[0], coords[1]] = 255
        Green_Color[coords[0], coords[1]] = 255
        Red_Color[coords[0], coords[1]] = 255
        SaltAndPepper_Image = cv2.merge((Blue_Color, Green_Color, Red_Color))
        Return_Image = SaltAndPepper_Image
    
    elif filterColor == "c" or filterColor == "C" :
        Blue_Color = cv2.add(Blue_Color,np.random.randint(1,255))
        Green_Color = cv2.add(Green_Color,np.random.randint(1,255))
        Red_Color = cv2.add(Red_Color,np.random.randint(1,255))
        
        Return_Image = cv2.merge((Blue_Color, Green_Color, Red_Color))

    if filterColor == "GRAY" or filterColor == "g" :
        Gray_Fliter = np.random.randint(1,255)
        Blue_Color = cv2.add(Blue_Color,Gray_Fliter)
        Green_Color = cv2.add(Green_Color,Gray_Fliter)
        Red_Color = cv2.add(Red_Color,Gray_Fliter)
        Return_Image = cv2.merge((Blue_Color, Green_Color, Red_Color))
        
    return Return_Image



# parameter[1] 는 가릴 영역을 의미하고 최대 25% 만 가릴 수 있게 한다.
# parameter[2] 는 픽셀의 크기를 나타낸다.
def Coarse_Drop_Out_Main(image, arr_ROIs, parameter = ('b',0,0) ) :
    parameter = list(parameter)
    n_img_Height, n_img_Width = image.shape[:2]     
    CoarseDropout_Image = image.copy()

    # 가리는(지우는) 영역
    if parameter[1] > 0.25 :
        parameter[1] = 0.25
    
    # 가리는 픽셀 사이즈의 크기
    # 가리는 픽셀 사이즈의 크기의 MAX Size 를 이미지 전체 크기에서 ROI 영역의 크기로 바꾸는 것이 합당하다.
    
    ROIsize = min(arr_ROIs[0].ROI_Xmin,arr_ROIs[0].ROI_Ymin)
    for i in range(len(arr_ROIs)) :
        ROIsize = min(ROIsize ,arr_ROIs[i].ROI_Xmin,arr_ROIs[i].ROI_Ymin )
 
    if parameter[2] > math.sqrt(ROIsize*ROIsize*parameter[1]/2) :
        parameter[2] = int(math.sqrt(ROIsize*ROIsize*parameter[1])/2)
    if parameter[2] == 0 :
        parameter[2] = 1
    
    # 가리는 영역 픽셀 좌표의 개수
    Random_Array_Size = int(n_img_Height*n_img_Width*parameter[1]/parameter[2]**2 /4)
    
    
    Random_Point = []
    # 사이즈가 작다면 다시뽑고
    if(5000 >= Random_Array_Size) :
        for i in range(0,Random_Array_Size) :
            # 여기서 랜덤하게 좌표를 선택해야 한다.
            # 내생각에는 여기서 최대 좌표/ 픽셀 사이즈 만큼 해줘야 하지만/ 그냥 해본다
            randomX = np.random.randint(1+parameter[2],n_img_Width-parameter[2]-1)
            randomY = np.random.randint(1+parameter[2],n_img_Height-parameter[2]-1)

            while (randomX, randomY) in Random_Point :
                randomX = np.random.randint(1+parameter[2],n_img_Width-parameter[2]-1)
                randomY = np.random.randint(1+parameter[2],n_img_Height-parameter[2]-1)

            Random_Point.append((randomX,randomY))
    
    # 사이즈가 크다면 무시 한다
    else :
        for i in range(0,Random_Array_Size) :
            # 여기서 랜덤하게 좌표를 선택해야 한다.
            # 내생각에는 여기서 최대 좌표/ 픽셀 사이즈 만큼 해줘야 하지만/ 그냥 해본다
            randomX = np.random.randint(1+parameter[2],n_img_Width-parameter[2]-1)
            randomY = np.random.randint(1+parameter[2],n_img_Height-parameter[2]-1)          
            Random_Point.append((randomX,randomY))
            
    
    for point in Random_Point :
        Filter = get_filter( 2*parameter[2] , 2*parameter[2] , parameter[0] )
        CoarseDropout_Image[point[1]-parameter[2] : point[1]+parameter[2] ,
                            point[0]-parameter[2] : point[0]+parameter[2]] = Filter[0:2*parameter[2] , 0:2*parameter[2]]

    return CoarseDropout_Image , arr_ROIs
