from PyQt5.QtCore import QThread
import os
import cv2
import numpy as np
from pathlib import Path

### Color
from color import All_Color_Add
from color import Channel_Remove
from color import Channel_Shuffle
from color import CLAHE
from color import Histogram_Equalization
from color import One_Color_Add
from color import Three_Color_Add
from color import To_Gray
from color import Two_Channel_Remove
from color import Two_Color_Add
### Noise
from noise import Coarse_Channel_Out
from noise import Coarse_Drop_Out
from noise import Gaussian_Noise
from noise import Poisson_Noise
from noise import SaltAndPepper_Noise
from noise import Speckle_Noise
### Blur
from blur import Basic_Blur
from blur import Median_Blur
### Transformation
from transformation import Flip
from transformation import Perspective_Transform
from transformation import Rotation
### Edge
from edge import Edge
### ROI
import ROI_main


class Augmentation_Parameter:
    str_Data_Type = str()
    str_Yolo_Path = str()
    str_CSV_Path = str()

    str_Output_Path = str()

    ### color
    Use_All_Add = bool()
    Use_Channel_Remove = bool()
    Use_Channel_Shuffle = bool()
    Use_CLAHE = bool()
    Use_Histogram_Equalization = bool()
    Use_One_Color_Add = bool()
    Use_Three_Color_Add = bool()
    Use_To_Gray = bool()
    Use_Two_Channel_Remove = bool()
    Use_Two_Color_Add = bool()
    ### noise
    Use_Coarse_Channel_Out = bool()
    Use_Coarse_Drop_Out = bool()
    Use_Gaussian_Noise = bool()
    Use_Poisson_Noise = bool()
    Use_SaltAndPepper_Noise = bool()
    Use_Speckle_Noise = bool()
    ### blur
    Use_Basic_Blur = bool()
    Use_Median_Bulr = bool()
    # Transformation
    Use_Flip = bool()
    Use_PT = bool()
    Use_Rotation = bool()
    Use_Edge = bool()


class Augmentation(QThread):
    AugP = None
    count = int(1)
    
    def __init__(self , parent , AugP= None ):
        super().__init__()
        self.n = 0
        self.main = parent
        self.AugP = AugP

    # ROI영역정보와 이미지를 YOLO Data set에 맞게 저장한다.
    # arr_tp_aug_Info = [tuple, tuple, tuple, tuple, ]
    # tp = tuple(이미지, ROIs)
    # ROIs = src/ROI_main.py의 ROI_Main 클래스들의 list입니다.

    def Save_Yolo_Data(self,arr_tp_aug_Info,f_name):
        for tuple in arr_tp_aug_Info:
            Aug_Image = tuple[0]
            Aug_ROIs = tuple[1]
            #file_name = str(self.AugP.str_Output_Path+str(self.count)) # output 경로
            file_name = self.AugP.str_Output_Path+'{}_{:010d}'.format(f_name,self.count) # output 경로
            cv2.imwrite(file_name+'.jpg',Aug_Image)
            f = open(file_name+str(".txt"), 'w')
            img_h , img_w , img_c = Aug_Image.shape
            for Now_ROI in Aug_ROIs :
                X_Center = ((Now_ROI.ROI_Xmin*2+Now_ROI.ROI_Width)/2)/img_w
                Y_Center = ((Now_ROI.ROI_Ymin*2+Now_ROI.ROI_Height)/2)/img_h
                Width = Now_ROI.ROI_Width/img_w
                Height = Now_ROI.ROI_Height/img_h

                f.write(str(Now_ROI.ROI_Class) + str(" ") + str(X_Center)
                                + str(" ") + str(Y_Center)
                                + str(" ") + str(Width)
                                + str(" ") + str(Height) 
                                + str("\n")
                        )
            f.close()
            self.count+=1
        return
    
    def Save_CSV_Data(self,arr_tp_aug_Info):
        file_csv_File = open(str(self.AugP.str_Output_Path+"output.csv"),'a') # output 경로
        for tuple in arr_tp_aug_Info:
            file_name = str(self.AugP.str_Output_Path+str(self.count)+str('.jpg')) # output 경로
            Aug_Image = tuple[0]
            Aug_ROIs = tuple[1]
            cv2.imwrite(file_name+'.jpg',Aug_Image)
            img_h , img_w , img_c = Aug_Image.shape
            for Now_ROI in Aug_ROIs :
                file_csv_File.write(str(file_name)+ str(",") + str(img_w) + str(",") + str(img_h) + str(",") + str(Now_ROI.ROI_Class) + str(",") +\
                          str(Now_ROI.ROI_Xmin) + str(",") + str(Now_ROI.ROI_Ymin) + str(",") +\
                          str(Now_ROI.ROI_Xmin + Now_ROI.ROI_Width) + str(",") + str(Now_ROI.ROI_Ymin + Now_ROI.ROI_Height) +\
                          str("\n"))            
            self.count+=1
        file_csv_File.close()
        return

    def Do_Augmantation(self , image ,arr_ROIs, f_name):
        arr_tp_aug_Info = list()

        ### color
        if self.AugP.Use_All_Add == True :
            parameter = np.random.randint(-50,50+1) # -50~ 50 사이 랜덤해서 전체적인 밝기를 높이거나 줄인다.
            Aug_Image,Aug_ROIs  = All_Color_Add.All_Color_Add_Main(image ,arr_ROIs , parameter=parameter)
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))
        
        
        if self.AugP.Use_Channel_Remove == True :
            random_Num = np.random.randint(1,3+1) # RGB 선택을 위함
            parameter = str()
            if random_Num == 1:
                parameter = 'b' # Blue 채널 삭제
            elif random_Num == 2:
                parameter = 'g' # Green 채널 삭제
            elif random_Num == 3:
                parameter = 'r' # Red 채널 삭제
            Aug_Image,Aug_ROIs = Channel_Remove.Channel_Remove_Main(image , arr_ROIs , parameter=parameter)
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))
        

        if self.AugP.Use_Channel_Shuffle == True :
            random_Num = np.random.randint(1,5+1) # 채널을 어떻게 섞을지 랜덤 선택
            parameter = str()
            if random_Num == 1:
                parameter = 'bgr'
            elif random_Num == 2:
                parameter = 'brg'
            elif random_Num == 3:
                parameter = 'gbr'
            elif random_Num == 4:
                parameter = 'grb'
            elif random_Num == 5:
                parameter = 'rbg'
            Aug_Image , Aug_ROIs = Channel_Shuffle.Channel_Shuffle_Main(image, arr_ROIs , parameter = parameter)
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))
        

        if self.AugP.Use_CLAHE == True :
            random_Num = np.random.randint(1,7+1) # CLAHE를 적용할 채널 랜덤 선택
            parameter = str()
            if random_Num == 1:
                parameter = 'b'
            elif random_Num == 1:
                parameter = 'g'
            elif random_Num == 3:
                parameter = 'r'
            elif random_Num == 4:
                parameter = 'bg'
            elif random_Num == 5:
                parameter = 'br'
            elif random_Num == 6:
                parameter = 'gr'
            elif random_Num == 7:
                parameter = 'bgr'
            Aug_Image,Aug_ROIs = CLAHE.CLAHE_Main(image, arr_ROIs , parameter = parameter)
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))

        if self.AugP.Use_Histogram_Equalization == True :
            random_Num = np.random.randint(1,7+1) # 히스토그램 평준화를 적용할 채널 랜덤 선택
            parameter = str()
            if random_Num == 1:
                parameter = 'b'
            elif random_Num == 1:
                parameter = 'g'
            elif random_Num == 3:
                parameter = 'r'
            elif random_Num == 4:
                parameter = 'bg'
            elif random_Num == 5:
                parameter = 'br'
            elif random_Num == 6:
                parameter = 'gr'
            elif random_Num == 7:
                parameter = 'bgr'
            Aug_Image,Aug_ROIs = Histogram_Equalization.Histogram_Equalization_Main(image, arr_ROIs , parameter = parameter)
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))


        if self.AugP.Use_One_Color_Add == True :
            random_Num = np.random.randint(1,3+1) # 채널
            parameter0 = str()
            if random_Num == 1:
                parameter0 = 'b'
            elif random_Num == 2:
                parameter0 = 'g'
            elif random_Num == 3:
                parameter0 = 'r'
            parameter1 = np.random.randint(-50,50+1) # -50~ 50 값 더하거나 빼기
            Aug_Image,Aug_ROIs = One_Color_Add.One_Color_Add_Main(image ,arr_ROIs , parameter = (parameter0,parameter1))
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))


        if self.AugP.Use_Three_Color_Add == True :
            parameter0 = np.random.randint(-50,50+1)
            parameter1 = np.random.randint(-50,50+1)
            parameter2 = np.random.randint(-50,50+1)
            Aug_Image,Aug_ROIs = Three_Color_Add.Three_Color_Add_Main(image , arr_ROIs , parameter = (parameter0,parameter1,parameter2))
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))


        if self.AugP.Use_To_Gray == True :
            Aug_Image,Aug_ROIs = To_Gray.To_Gray_Main(image , arr_ROIs )
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))


        if self.AugP.Use_Two_Channel_Remove == True :
            random_Num = np.random.randint(1,3+1)
            parameter = str()
            if random_Num == 1:
                parameter = 'br'
            elif random_Num == 2:
                parameter = 'gr'
            elif random_Num == 3:
                parameter = 'bg'
            Aug_Image,Aug_ROIs =Two_Channel_Remove.Two_Channel_Remove_Main(image , arr_ROIs , parameter=parameter)
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))


        if self.AugP.Use_Two_Color_Add == True :
            random_Num = np.random.randint(1,7+1)
            parameter0 = str()
            if random_Num == 1:
                parameter0 = 'br'
            elif random_Num == 1:
                parameter0 = 'gr'
            elif random_Num == 3:
                parameter0 = 'bg'
            parameter1 = np.random.randint(-50,50+1)
            parameter2 = np.random.randint(-50,50+1)
            Aug_Image,Aug_ROIs =Two_Color_Add.Two_Color_Add_Main(image , arr_ROIs ,  parameter = (parameter0,parameter1,parameter2))
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))


        ### noise
        if self.AugP.Use_Coarse_Channel_Out == True :
            random_Num = np.random.randint(1,6+1)
            parameter0 = str('b')
            if random_Num == 1:
                parameter0 = 'b'
            elif random_Num == 1:
                parameter0 = 'g'
            elif random_Num == 3:
                parameter0 = 'r'
            elif random_Num == 4:
                parameter0 = 'bg'
            elif random_Num == 5:
                parameter0 = 'br'
            elif random_Num == 6:
                parameter0 = 'gr'
            parameter1 = np.random.randint(0,25+1)
            parameter2 = np.random.randint(0,500)
            Aug_Image,Aug_ROIs = Coarse_Channel_Out.Coarse_Channel_Out_Main(image , arr_ROIs ,  parameter = (parameter0,parameter1/100,parameter2))
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))


        if self.AugP.Use_Coarse_Drop_Out == True :
            random_Num = np.random.randint(1,6+1)
            parameter0 = str('b')
            if random_Num == 1:
                parameter0 = 'b'
            elif random_Num == 1:
                parameter0 = 'sp'
            elif random_Num == 3:
                parameter0 = 'c'
            elif random_Num == 4:
                parameter0 = 'g'
            parameter1 = np.random.randint(0,25+1)
            parameter2 = np.random.randint(0,500)
            Aug_Image,Aug_ROIs = Coarse_Drop_Out.Coarse_Drop_Out_Main(image , arr_ROIs ,  parameter = (parameter0,parameter1/100,parameter2))
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))
        

        if self.AugP.Use_Gaussian_Noise == True :
            Aug_Image,Aug_ROIs =Gaussian_Noise.Gaussian_Main(image, arr_ROIs)
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))


        if self.AugP.Use_Poisson_Noise == True :
            Aug_Image,Aug_ROIs = Poisson_Noise.Poisson_Main(image, arr_ROIs)
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))


        if self.AugP.Use_SaltAndPepper_Noise == True :
            parameter0 = np.random.randint(0,25+1)
            parameter1 = np.random.randint(0,100+1)
            SaltAndPepper_Noise.SaltAndPepper_Main(image, arr_ROIs,parameter= (parameter0,parameter1))
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))


        if self.AugP.Use_Speckle_Noise == True :
            Aug_Image,Aug_ROIs = Speckle_Noise.Speckle_Main(image ,arr_ROIs)
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))


        ### blur
        if self.AugP.Use_Basic_Blur == True :
            parameter0 = np.random.randint(3,15+1)
            parameter1 = np.random.randint(3,15+1)
            Aug_Image,Aug_ROIs =Basic_Blur.Basic_Blur_Main(image ,arr_ROIs,parameter=(parameter0,parameter1))
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))


        if self.AugP.Use_Median_Bulr == True :
            parameter = np.random.randint(3,15+1)
            Aug_Image,Aug_ROIs =Median_Blur.Median_Bulr_Main(image ,arr_ROIs,parameter=parameter)
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))


        ### Transformation
        if self.AugP.Use_Flip == True :
            parameter = np.random.randint(-1,1+1)
            Aug_Image,Aug_ROIs = Flip.Flip_Main(image ,arr_ROIs,parameter=parameter)
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))

        if self.AugP.Use_PT == True :
            Aug_Image,Aug_ROIs = Perspective_Transform.Perspective_Transform_Main(image ,arr_ROIs,parameter=0)
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))

        if self.AugP.Use_Rotation == True :
            parameter = np.random.randint(10,350+1)
            Aug_Image,Aug_ROIs = Rotation.Rotation_Main(image ,arr_ROIs,parameter=parameter)
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))

        if self.AugP.Use_Edge == True :
            Aug_Image,Aug_ROIs =Edge.Edge_Main(image ,arr_ROIs)
            arr_tp_aug_Info.append((Aug_Image,Aug_ROIs))


        if self.AugP.str_Data_Type == 'Yolo' :
            self.Save_Yolo_Data(arr_tp_aug_Info,f_name)
            


        elif self.AugP.str_Data_Type == 'TF':
            self.Save_CSV_Data(arr_tp_aug_Info)
        elif self.AugP.str_Data_Type == 'Pascal':
            None
        
        
        del[arr_tp_aug_Info]
        return

    def run(self) :
        self.main.Run_B.setDisabled(True)
        self.main.Image_Directory_B.setDisabled(True)

        
        def Load_Yolo_File(str_Dir_Path):
            arr_tuple_Return_File_list = list()
            arr_File_list = os.listdir(str_Dir_Path)
            for i in range(len(arr_File_list)):
                Now_Filename, Now_File_Extension = os.path.splitext(arr_File_list[i])
                if Now_File_Extension== str(".jpg") :
                    Next_Filename, Next_File_Extension = os.path.splitext(arr_File_list[i+1])
                    if (Now_Filename == Next_Filename) and (Next_File_Extension ==str(".txt") ):
                        arr_tuple_Return_File_list.append( (str_Dir_Path+arr_File_list[i],str_Dir_Path+arr_File_list[i+1]) )
            return arr_tuple_Return_File_list
        
        def Load_CSV_File(str_CSV_Path):
            
            templist = list()
            f_CSV_File = open(str_CSV_Path, 'r')
            str_line = None
            
            while(str_line != "") :
                
                str_line = f_CSV_File.readline()
                strNowROI = str_line.split(",")
                if len(strNowROI) == 1:
                    break
                
                image_path = strNowROI[0]
                if strNowROI[3] == "class" :
                    continue
                Now_ROI = ROI_main.ROI( strNowROI[3], int(strNowROI[4]),int(strNowROI[5]) , int(strNowROI[6])-int(strNowROI[4]) , int(strNowROI[7].split("\n")[0])-int(strNowROI[5]))
                templist.append((image_path,Now_ROI))
            
            
            f_CSV_File.close()
            ### Now, there will be duplicate image files in the List. But ROI is not redundant.
            ### To remove duplicate images 
            templist.sort(key=lambda x:x[0])
            arr_tuple_Return_File_list = list()
            Now_Image_Path = templist[0][0]
            arr_ROIs = list()
            
            for i in range(1,len(templist)) :
                if i == len(templist)-1 :
                    arr_tuple_Return_File_list.append((Now_Image_Path,arr_ROIs))
                    arr_ROIs = list()
                    break

                if Now_Image_Path != templist[i][0] :
                    arr_tuple_Return_File_list.append((Now_Image_Path,arr_ROIs))
                    arr_ROIs = list()               # Empty ROI and
                    arr_ROIs.append(templist[i][1]) # Input New ROI.
                    Now_Image_Path = templist[i][0]
                

                elif Now_Image_Path == templist[i][0]:
                    arr_ROIs.append(templist[i][1])
            
            return arr_tuple_Return_File_list
        
        
        if self.AugP.str_Data_Type == 'Yolo':
            arr_tuple_File_list = Load_Yolo_File(self.AugP.str_Yolo_Path)
            denominator = len(arr_tuple_File_list)
            numerator = 0
            for tuple_Now_File in arr_tuple_File_list :
                self.count = 1
                Now_Image = cv2.imread(tuple_Now_File[0])
                GT_File = open(tuple_Now_File[1], 'r')
                Base_name = os.path.basename(tuple_Now_File[0])
                File_name = os.path.splitext(Base_name)[0]
                arr_ROIs = ROI_main.Get_Origin_ROI_Yolo(GT_File,Now_Image.shape[0],Now_Image.shape[1]) # GT file , Image Size
                self.Do_Augmantation(Now_Image,arr_ROIs,File_name)
                numerator +=1
                self.main.progressChanged.emit((numerator/denominator)*100)
        
        elif self.AugP.str_Data_Type == 'TF':
            arr_tuple_File_list = Load_CSV_File(self.AugP.str_CSV_Path) # Load_CSV_File function is return image and ROI. # input 경로
            denominator = len(arr_tuple_File_list)
            numerator = 0

            file_csv_File = open(str(self.AugP.str_Output_Path+"output.csv"),'a') # output 경로
            file_csv_File.write(str("filename,width,height,class,xmin,ymin,xmax,ymax\n"))
            file_csv_File.close()

            for tuple_Now_File in arr_tuple_File_list :
                Now_Image = cv2.imread(tuple_Now_File[0])
                Now_img_name = tuple_Now_File[0]
                Now_txt_name = tuple_Now_File[1]
                arr_ROIs = tuple_Now_File[1]
                self.Do_Augmantation(Now_Image,arr_ROIs, Now_img_name, Now_txt_name)
                numerator +=1
                self.main.progressChanged.emit((numerator/denominator)*100)



        elif self.AugP.str_Data_Type == 'Pascal':
            None
        
        self.main.Run_B.setEnabled(True)
        self.main.Image_Directory_B.setEnabled(True)
        self.main.progressChanged.emit(100)

        os.startfile(Path(self.AugP.str_Output_Path))
