import cv2
import numpy as np
import sys
sys.path.append("..")
import ROI_main

def Matrix_Calculation(Matrix, point) :
    h11 = Matrix[0][0]
    h12 = Matrix[0][1]
    h13 = Matrix[0][2]
    h21 = Matrix[1][0]
    h22 = Matrix[1][1]
    h23 = Matrix[1][2]
    h31 = Matrix[2][0]
    h32 = Matrix[2][1]
    x = point[0]
    y = point[1]
    new_x = int ( (h11*x + h12*y + h13)/(h31*x + h32*y + 1) )
    new_y = int ( (h21*x + h22*y + h23)/(h31*x + h32*y + 1) )
    return (new_x,new_y)

def Get_Perspective_ROI(Origin_ROI , Matrix ) :
    arr_ROIs = list()
    arr_ROIs_Points = list()
    for i_ROI in Origin_ROI :
        ### LT , RT , RB , LB Rotation
        now_LT = ( i_ROI.ROI_Xmin                   , i_ROI.ROI_Ymin )
        now_RT = ( i_ROI.ROI_Xmin + i_ROI.ROI_Width , i_ROI.ROI_Ymin )
        now_RB = ( i_ROI.ROI_Xmin + i_ROI.ROI_Width , i_ROI.ROI_Ymin + i_ROI.ROI_Height )
        now_LB = ( i_ROI.ROI_Xmin                   , i_ROI.ROI_Ymin + i_ROI.ROI_Height )

        now_ROI_Points = ( now_LT , now_RT , now_RB , now_LB )
        arr_ROIs_Points.append(now_ROI_Points)
    
    arr_ROIs_Points = np.float32(arr_ROIs_Points)
    
    for i in range( len(arr_ROIs_Points) ) :
        new_LT = Matrix_Calculation(Matrix , arr_ROIs_Points[i][0])
        new_RT = Matrix_Calculation(Matrix , arr_ROIs_Points[i][1])
        new_RB = Matrix_Calculation(Matrix , arr_ROIs_Points[i][2])
        new_LB = Matrix_Calculation(Matrix , arr_ROIs_Points[i][3])
        
        
        LT_X  = min( new_LT[0] , new_RT[0] , new_RB[0] , new_LB[0] )
        LT_Y  = min( new_LT[1] , new_RT[1] , new_RB[1] , new_LB[1] )

        RB_X  = max( new_LT[0] , new_RT[0] , new_RB[0] , new_LB[0] )
        RB_Y  = max( new_LT[1] , new_RT[1] , new_RB[1] , new_LB[1] )
        
        n_ROI = ROI_main.ROI(Origin_ROI[i].ROI_Class , ROI_Xmin = LT_X, ROI_Ymin = LT_Y, ROI_Width = abs(RB_X-LT_X) , ROI_Height = abs(RB_Y -LT_Y) )
        arr_ROIs.append(n_ROI)
    
    return arr_ROIs


def Get_Random_parameter():
    ### Y X 순
    LTX = np.random.randint(0,20+1)/100 # Left Top X 0~20 %
    LTY = np.random.randint(0,20+1)/100 # Left Top Y 0~20 %
    
    LBX = np.random.randint(0,20+1)/100 # Left Bottom X 0~20 %
    LBY = np.random.randint(0,20+1)/100 # Left Bottom Y 0~20 %
    
    RBX = np.random.randint(0,20+1)/100 # Right Bottom X 0~20 %
    RBY = np.random.randint(0,20+1)/100 # Right Bottom Y 0~20 %
    
    RTX = np.random.randint(0,20+1)/100 # Right Top X 0~20 %
    RTY = np.random.randint(0,20+1)/100 # Right Top Y 0~20 %

    return ( (LTY, LTX) , ( LBY, LBX ) , (RTY,RTX) , (RBY,RBX) )

def Perspective_Transform_Main( image , arr_ROIs , parameter = 0) :
    if parameter == 0 :
        parameter = Get_Random_parameter()
    
    image = image.copy()
    n_img_Height, n_img_Width = image.shape[:2] 
    
    pt1 = np.float32([[0,0] , [n_img_Width,0] , [n_img_Height,n_img_Width], [0,n_img_Height] ]) # LT , RT , RB , LB Rotation


    pt2 = np.float32( [ [ n_img_Width * parameter[0][0]         , n_img_Height * parameter[0][1] ] , # LT 
                        [ n_img_Width * ( 1 - parameter[2][0] ) , n_img_Height * parameter[2][1] ] ,  # RT
                        [ n_img_Width * ( 1 - parameter[3][0] ) , n_img_Height * ( 1 - parameter[3][1] ) ] , # RB
                        [ n_img_Width * parameter[1][0]         , n_img_Height * ( 1 - parameter[1][1] ) ] ] ) # LB

    matrix = cv2.getPerspectiveTransform(pt1,pt2)
    Perspective_Image = cv2.warpPerspective(image,matrix,(n_img_Width,n_img_Height))
    Perspective_ROIs = Get_Perspective_ROI( arr_ROIs , matrix )
    
    return Perspective_Image , Perspective_ROIs
