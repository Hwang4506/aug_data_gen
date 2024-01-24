class ROI:
    ROI_Class = int()
    ROI_Xmin = int()
    ROI_Ymin = int()
    ROI_Width = int()
    ROI_Height = int()
    

    def __init__(self, ROI_Class, ROI_Xmin, ROI_Ymin , ROI_Width , ROI_Height):
        self.ROI_Class = ROI_Class
        self.ROI_Xmin = ROI_Xmin
        self.ROI_Ymin = ROI_Ymin
        self.ROI_Width = ROI_Width
        self.ROI_Height = ROI_Height


def Get_Origin_ROI_Yolo(GT_File , n_img_Height , n_img_Width) :
    line = None # None 로 초기화 해준다.
    arr_ROIs = list()

    while(line != "") :
        line = GT_File.readline()
        str_Now_ROI = line.split(" ")
        if len(str_Now_ROI) == 1:
            break
        
        i_object_Class = int( str_Now_ROI[0] )
        f_object_Center_x = float( str_Now_ROI[1] )
        f_object_Center_y = float( str_Now_ROI[2] )
        f_object_Width = float( str_Now_ROI[3] )
        f_object_Height = float( str_Now_ROI[4].split("\n")[0] )

        i_ROI_Width = int(n_img_Width * f_object_Width)
        i_ROI_X_min = int( (f_object_Center_x * n_img_Width) - i_ROI_Width/2)
        i_ROI_Height = int(f_object_Height * n_img_Height)
        i_ROI_Y_min = int( (f_object_Center_y * n_img_Height) - i_ROI_Height/2)
        n_ROI = ROI( i_object_Class , i_ROI_X_min, i_ROI_Y_min , i_ROI_Width , i_ROI_Height) 
        arr_ROIs.append(n_ROI)        
    
    return arr_ROIs