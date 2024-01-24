import cv2
import math
import numpy as np
import sys
sys.path.append("..")
import ROI_main  
def Get_Translation_ROI(Origin_arr_ROIs, Shift_amount) :
    n_Amount_Shift_X = Shift_amount[0]
    n_Amount_Shift_Y = Shift_amount[1]
    arr_ROIs = list()

    for i_ROI in Origin_arr_ROIs :
        now_ROI = ROI_main.ROI( i_ROI.ROI_Class , i_ROI.ROI_Xmin+n_Amount_Shift_X , i_ROI.ROI_Ymin+n_Amount_Shift_Y , i_ROI.ROI_Width , i_ROI.ROI_Height )
        arr_ROIs.append(now_ROI)
    return arr_ROIs


def Get_Rotation_ROI(Translation_arr_ROIs, Tuple_CenterPoints, Degree) :
    Radian = Degree * (math.pi / 180.0)
    
    CenterX = Tuple_CenterPoints[0]
    CenterY = Tuple_CenterPoints[1]
    arr_ROIs = list()

    for i_ROI in Translation_arr_ROIs :
        
        i_Origin_ROI_Center_X = ( i_ROI.ROI_Xmin + i_ROI.ROI_Width )/2
        i_Origin_ROI_Center_Y = ( i_ROI.ROI_Ymin + i_ROI.ROI_Height )/2
        
        C_X = (math.cos(Radian)*(i_Origin_ROI_Center_X-CenterX) - math.sin(Radian)*(i_Origin_ROI_Center_X-CenterY) + CenterX) # ROI Center X
        C_Y = (math.sin(Radian)*(i_Origin_ROI_Center_X-CenterX) + math.cos(Radian)*(i_Origin_ROI_Center_Y-CenterY) + CenterY) # ROI Center Y
    
        LT_X = (math.cos(Radian)*(i_ROI.ROI_Xmin-CenterX) - math.sin(Radian)*(i_ROI.ROI_Ymin-CenterY) + CenterX) # ROI Left Top X
        LT_Y = (math.sin(Radian)*(i_ROI.ROI_Xmin-CenterX) + math.cos(Radian)*(i_ROI.ROI_Ymin-CenterY) + CenterY) # ROI Left Top Y

        LB_X = (math.cos(Radian)*(i_ROI.ROI_Xmin-CenterX) - math.sin(Radian)*(i_ROI.ROI_Ymin+i_ROI.ROI_Height-CenterY) + CenterX) # ROI Left Bottom X
        LB_Y = (math.sin(Radian)*(i_ROI.ROI_Xmin-CenterX) + math.cos(Radian)*(i_ROI.ROI_Ymin+i_ROI.ROI_Height-CenterY) + CenterY) # ROI Left Bottom Y

        RB_X = (math.cos(Radian)*(i_ROI.ROI_Xmin+i_ROI.ROI_Width-CenterX) - math.sin(Radian)*(i_ROI.ROI_Ymin+i_ROI.ROI_Height-CenterY) + CenterX) # ROI Right Bottom X
        RB_Y = (math.sin(Radian)*(i_ROI.ROI_Xmin+i_ROI.ROI_Width-CenterX) + math.cos(Radian)*(i_ROI.ROI_Ymin+i_ROI.ROI_Height-CenterY) + CenterY) # ROI Right Bottom Y
        
        RT_X = (math.cos(Radian)*(i_ROI.ROI_Xmin+i_ROI.ROI_Width-CenterX) - math.sin(Radian)*(i_ROI.ROI_Ymin-CenterY) + CenterX) # ROI Right Top X
        RT_Y = (math.sin(Radian)*(i_ROI.ROI_Xmin+i_ROI.ROI_Width-CenterX) + math.cos(Radian)*(i_ROI.ROI_Ymin-CenterY) + CenterY) # ROI Right Top Y

        Xmin = min( LT_X , LB_X , RB_X , RT_X )
        Ymin = min( LT_Y , LB_Y , RB_Y , RT_Y )
        Xmax = max( LT_X , LB_X , RB_X , RT_X )
        Ymax = max( LT_Y , LB_Y , RB_Y , RT_Y )

        now_ROI = ROI_main.ROI(i_ROI.ROI_Class , int(Xmin) , int(Ymin) , int(Xmax-Xmin) , int(Ymax-Ymin) )

        arr_ROIs.append(now_ROI)
    
    return arr_ROIs


def Get_Image_Rotate_Points(image, Degree) :

    n_img_Height, n_img_Width = image.shape[:2]
    Radian = Degree * (math.pi / 180.0)

    img_Center_X = n_img_Width/2
    img_Center_Y = n_img_Height/2

    ## Counterwatch
    LT_X = math.floor(math.cos(Radian)*(0-img_Center_X) - math.sin(Radian)*(0-img_Center_Y) + img_Center_X) # Left Top X
    LT_Y = math.floor(math.sin(Radian)*(0-img_Center_X) + math.cos(Radian)*(0-img_Center_Y) + img_Center_Y) # Left Top Y

    LB_X = math.floor(math.cos(Radian)*(0-img_Center_X) - math.sin(Radian)*(n_img_Height-img_Center_Y) + img_Center_X) # Left Bottom X
    LB_Y = math.floor(math.sin(Radian)*(0-img_Center_X) + math.cos(Radian)*(n_img_Height-img_Center_Y) + img_Center_Y) # Left Bottom Y
    
    RB_X = math.floor(math.cos(Radian)*(n_img_Width-img_Center_X) - math.sin(Radian)*(n_img_Height-img_Center_Y) + img_Center_X) # Right Bottom X
    RB_Y = math.floor(math.sin(Radian)*(n_img_Width-img_Center_X) + math.cos(Radian)*(n_img_Height-img_Center_Y) + img_Center_Y) # Right Bottom Y

    RT_X = math.floor(math.cos(Radian)*(n_img_Width-img_Center_X) - math.sin(Radian)*(0-img_Center_Y) + img_Center_X) # Right Top X
    RT_Y = math.floor(math.sin(Radian)*(n_img_Width-img_Center_X) + math.cos(Radian)*(0-img_Center_Y) + img_Center_Y) # Right Top Y

    arr_Image_Rotate_Points = ( ( LT_X , LT_Y ) , ( LB_X , LB_Y ), ( RB_X , RB_Y ) , ( RT_X , RT_Y ) )
    
    return arr_Image_Rotate_Points

def Rotation_Main(image , arr_ROIs , parameter=0.0) : # parameter = Rotation_Degree

    image = image.copy()

    n_img_Height, n_img_Width = image.shape[:2]
    parameter # 회전 시킬 각도

    arr_Image_Rotate_Points = Get_Image_Rotate_Points(image, -parameter)

    airp = np.array(arr_Image_Rotate_Points)
    airp = airp[airp[:, 0].argsort()[::1]] # sort X min
    n_temp_Shitf_X = airp[0,0]
    airp = airp[airp[:, 1].argsort()[::1]] # sort Y min
    n_temp_Shitf_Y = airp[0,1]

    
    n_First_Shift_X = int()
    n_First_Shift_Y = int()
    
    if n_temp_Shitf_X <= 0 :
        n_First_Shift_X = -n_temp_Shitf_X

    if n_temp_Shitf_Y <= 0 :
        n_First_Shift_Y = -n_temp_Shitf_Y


    ### 2. Translation ROI
    Shif_matrix = np.float32([ [1,0,n_First_Shift_X]  , [0,1,n_First_Shift_Y] ] )
    First_Shift_Image = cv2.warpAffine( 
                                        image , Shif_matrix,
                                        ( n_img_Width+(n_First_Shift_X) , n_img_Height+(n_First_Shift_Y) )
                                    )

    tuple_Shift_Amount = (n_First_Shift_X,n_First_Shift_Y)
    arr_ROIs = Get_Translation_ROI(arr_ROIs, tuple_Shift_Amount)



    ### 3. Rotate ROI
    Rotation_Center_Point = ( n_img_Width/2 + (n_First_Shift_X) , n_img_Height/2 + (n_First_Shift_Y) )

    Rotation_Matrix = cv2.getRotationMatrix2D( Rotation_Center_Point , parameter, 1) 
    Rotation_Image = cv2.warpAffine(
                                        First_Shift_Image , Rotation_Matrix ,
                                        ( n_img_Width + (n_First_Shift_X*2), n_img_Height + (n_First_Shift_Y*2) ) 
                                    )
    
    Rotation_ROIs = Get_Rotation_ROI(arr_ROIs , Rotation_Center_Point , -parameter)
    
    
    return Rotation_Image , Rotation_ROIs
