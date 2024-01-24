import cv2
import numpy as np
import math
def Channel_Out( Origin_Image , tuple_Filter_Size , rm_Chnnel , arr_Random_Point) :
    CoarseChannelout_Image = Origin_Image.copy()

    height,weight, = Origin_Image.shape[:2]
    zero =np.zeros((height,weight,1), dtype=np.uint8)
    Blue_Channel = Origin_Image[:,:,0]
    Green_Channel = Origin_Image[:,:,1]
    Red_Channel = Origin_Image[:,:,2]

    Filter_Size_X = tuple_Filter_Size[0]
    Filter_Size_Y = tuple_Filter_Size[1]

    if (( rm_Chnnel == 'r' ) or ( rm_Chnnel == 'R' )) :        
        Now_Channel = cv2.merge((Blue_Channel, Green_Channel, zero))

    elif (( rm_Chnnel == 'g' ) or ( rm_Chnnel == 'g' )) :
        Now_Channel = cv2.merge((Blue_Channel, zero, Red_Channel))

    elif (( rm_Chnnel == 'b' ) or ( rm_Chnnel == 'b' )) :
        Now_Channel = cv2.merge((zero, Green_Channel, Red_Channel))

    elif (( rm_Chnnel == 'BG') or (rm_Chnnel == 'bg' )) :
        Now_Channel = cv2.merge((zero, zero, Red_Channel))
            
    elif (( rm_Chnnel == 'BR') or (rm_Chnnel == 'br')) :
        Now_Channel = cv2.merge((zero, Green_Channel, zero))
            
    elif (( rm_Chnnel == 'GR') or (rm_Chnnel == 'gr')) :
        Now_Channel = cv2.merge((Blue_Channel, zero, zero))
    
    for point in arr_Random_Point :

        CoarseChannelout_Image[ point[1]-Filter_Size_Y : point[1]+Filter_Size_Y ,
                                    point[0]-Filter_Size_X : point[0]+Filter_Size_X ] = Now_Channel[ point[1]-Filter_Size_Y : point[1]+Filter_Size_Y ,
                                                                                                     point[0]-Filter_Size_X : point[0]+Filter_Size_X ]
        
    return CoarseChannelout_Image



# parameter[1] 는 가릴 영역을 의미하고 최대 25% 만 가릴 수 있게 한다.
# parameter[2] 는 픽셀의 크기를 나타낸다.
def Coarse_Channel_Out_Main(image, arr_ROIs,parameter = ('r',0,0)  ) :
    parameter = list(parameter)
    n_img_Height, n_img_Width = image.shape[:2]     
    CoarseChannelout_Image = image.copy()

    if parameter[1] > 0.25 :
        parameter[1] = 0.25

    ROIsize = min(arr_ROIs[0].ROI_Xmin,arr_ROIs[0].ROI_Ymin)
    for i in range(len(arr_ROIs)) :
        ROIsize = min(ROIsize ,arr_ROIs[i].ROI_Xmin,arr_ROIs[i].ROI_Ymin )
 
    if parameter[2] > math.sqrt(ROIsize*ROIsize*parameter[1]/2) :
        parameter[2] = int(math.sqrt(ROIsize*ROIsize*parameter[1])/2)
    if parameter[2] == 0 :
        parameter[2] = 1
    
    Random_Array_Size = int(n_img_Height*n_img_Width*parameter[1]/parameter[2]**2 /4)    
    arr_Random_Point = list()
    # 사이즈가 작다면 다시뽑고
    if(5000 >= Random_Array_Size) :
        for i in range(0,Random_Array_Size) :
            # 여기서 랜덤하게 좌표를 선택해야 한다.
            # 내생각에는 여기서 최대 좌표/ 픽셀 사이즈 만큼 해줘야 하지만/ 그냥 해본다
            randomX = np.random.randint(1+parameter[2],n_img_Width-parameter[2]-1)
            randomY = np.random.randint(1+parameter[2],n_img_Height-parameter[2]-1)

            while (randomX, randomY) in arr_Random_Point :
                randomX = np.random.randint(1+parameter[2],n_img_Width-parameter[2]-1)
                randomY = np.random.randint(1+parameter[2],n_img_Height-parameter[2]-1)

            arr_Random_Point.append((randomX,randomY))
    
    # 사이즈가 크다면 무시 한다
    else :
        for i in range(0,Random_Array_Size) :
            # 여기서 랜덤하게 좌표를 선택해야 한다.
            # 내생각에는 여기서 최대 좌표/ 픽셀 사이즈 만큼 해줘야 하지만/ 그냥 해본다
            randomX = np.random.randint(1+parameter[2],n_img_Width-parameter[2]-1)
            randomY = np.random.randint(1+parameter[2],n_img_Height-parameter[2]-1)          
            arr_Random_Point.append((randomX,randomY))
            
    CoarseChannelout_Image = Channel_Out( image, (parameter[2] , parameter[2]) , parameter[0]  , arr_Random_Point)

    return CoarseChannelout_Image , arr_ROIs
