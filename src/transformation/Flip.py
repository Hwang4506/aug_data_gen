import cv2
import sys
sys.path.append("..")
import ROI_main  

def Get_Filp_ROI(Origin_arr_ROIs ,image, parameter):

    arr_ROIs = list()
    n_img_Height, n_img_Width = image.shape[:2]

    for i_ROI in Origin_arr_ROIs :
        Xmin = i_ROI.ROI_Xmin
        Ymin = i_ROI.ROI_Ymin
        if parameter == -1 : # TBLR Filp
            Xmin = n_img_Width - i_ROI.ROI_Xmin - i_ROI.ROI_Width
            Ymin = n_img_Height - i_ROI.ROI_Ymin - i_ROI.ROI_Height

        elif parameter == 0 : # TB Filp
            Ymin = n_img_Height - i_ROI.ROI_Ymin - i_ROI.ROI_Height

        elif parameter == 1 : # LR Filp
            Xmin = n_img_Width - i_ROI.ROI_Xmin - i_ROI.ROI_Width

        n_ROI = ROI_main.ROI(i_ROI.ROI_Class , Xmin, Ymin, i_ROI.ROI_Width, i_ROI.ROI_Height)
        arr_ROIs.append(n_ROI)
        
    return arr_ROIs
        

def Flip_Main( image , arr_ROIs , parameter=0) :
    image = image.copy()
    n_img_Height, n_img_Width = image.shape[:2]
    
    if parameter < -1 :
        parameter = -1
    if parameter > 1 :
        parameter = 1

    Flip_Image = cv2.flip(image,parameter)
    Flip_ROIs = Get_Filp_ROI(arr_ROIs, image,parameter)
    
    return Flip_Image , Flip_ROIs