import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic , QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout
from PyQt5.QtGui import *
import tkinter
from tkinter import filedialog
import Augmentation
form_class = uic.loadUiType(str("../ui/main.ui"))[0]


class MainWindow(QMainWindow, form_class):

    augp = Augmentation.Augmentation_Parameter
    Aug = None
    progressChanged = QtCore.pyqtSignal(int)

    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.Preprocess()
        ########## Main Tab ##########
        self.GT_Type_COMB
        self.Image_Directory_B.clicked.connect( self.Select_Input_Path )
        self.Image_Directory_LE.setReadOnly(True)
        self.Output_Directory_B.clicked.connect(self.Select_Output_Path )
        self.Output_Directory_LE.setReadOnly(True)

        
        self.Run_B.clicked.connect(self.AugmentationRun)
        self.progressChanged.connect(self.progressBar.setValue)
        self.GT_Type_COMB.currentTextChanged.connect(self.on_combobox_changed)
        self.Aug = Augmentation.Augmentation(parent = self,AugP = self.augp)
        return

    def AugmentationRun(self):
        self.progressBar.reset()

        if self.GT_Type_COMB.currentIndex() == 0  :
            self.augp.str_Data_Type =str('Yolo')
            self.augp.str_Yolo_Path = self.Image_Directory_LE.text()
        
        if self.GT_Type_COMB.currentIndex() == 1  :
            self.augp.str_Data_Type = str('TF')
            self.augp.str_CSV_Path =  self.Image_Directory_LE.text()
        
        self.augp.str_Output_Path = self.Output_Directory_LE.text()

        self.augp.Use_All_Add = self.Bright_CB.isChecked()
        self.augp.Use_Channel_Remove = self.CR_CB.isChecked()
        self.augp.Use_Channel_Shuffle = self.CS_CB.isChecked()
        self.augp.Use_CLAHE = self.CLAHE_CB.isChecked()
        self.augp.Use_Histogram_Equalization = self.HE_CB.isChecked()
        self.augp.Use_One_Color_Add = self.OCA_CB.isChecked()
        self.augp.Use_Three_Color_Add = self.T3CA_CB.isChecked()
        self.augp.Use_To_Gray = self.To_Gray_CB.isChecked()
        self.augp.Use_Two_Channel_Remove = self.TCR_CB.isChecked()
        self.augp.Use_Two_Color_Add = self.TCA_CB.isChecked()
        self.augp.Use_Coarse_Channel_Out = self.CCO_CB.isChecked()
        self.augp.Use_Coarse_Drop_Out = self.CDO_CB.isChecked()
        self.augp.Use_Gaussian_Noise = self.GN_CB.isChecked()
        self.augp.Use_Poisson_Noise = self.PN_CB.isChecked()
        self.augp.Use_SaltAndPepper_Noise = self.SAP_CB.isChecked()
        self.augp.Use_Speckle_Noise = self.SN_CB.isChecked()

        ### blur
        self.augp.Use_Basic_Blur = self.BB_CB.isChecked()
        self.augp.Use_Median_Bulr = self.MB_CB.isChecked()

        # Transformation
        self.augp.Use_Flip = self.F_CB.isChecked()
        self.augp.Use_PT = self.PT_CB.isChecked()
        self.augp.Use_Rotation = self.R_CB.isChecked()
        self.augp.Use_Edge = self.E_CB.isChecked()

        if self.GT_Type_COMB.currentIndex() == 0 :
            if os.path.isdir(self.augp.str_Yolo_Path) == False:
                msg = QMessageBox()
                msg.setWindowTitle(str("Error"))
                msg.setText("경로를 제대로 입력해주세요")
                msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
                msg.exec_()
                return

        elif self.GT_Type_COMB.currentIndex() == 1 :
            if (os.path.isfile(self.augp.str_CSV_Path)== False) or (os.path.splitext(self.augp.str_CSV_Path)[1] != str('.csv') ) :
                msg = QMessageBox()
                msg.setWindowTitle(str("Error"))
                msg.setText("경로를 제대로 입력해주세요")
                msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
                msg.exec_()
                return
                
        self.Aug.start()
        return


    def Preprocess(self):
        self.on_combobox_changed()


    def on_combobox_changed(self):
        if self.GT_Type_COMB.currentIndex() == 0 or self.GT_Type_COMB.currentIndex() == 1:
            
            self.Image_Directory_B.setEnabled(True)
            self.Run_B.setEnabled(True)
        else : 
            self.Image_Directory_B.setDisabled(True)
            self.Run_B.setDisabled(True)

    
    def Select_Input_Path(self):
        root = tkinter.Tk()
        root.withdraw()
        if self.GT_Type_COMB.currentIndex() == 0 :
            path = filedialog.askdirectory(parent=root,initialdir = str("./"),title=str("Please select a Output directory") )
            path += str("/")
            self.Image_Directory_LE.setText(path)
            
        elif self.GT_Type_COMB.currentIndex() == 1 :
            path = filedialog.askopenfilename(initialdir = str("./"), title=str("Please select a csv file") , filetypes = (("csv files", ".csv"),("all files", "*.*")))
            self.Image_Directory_LE.setText(path)
        

    def Select_Output_Path(self):
        root = tkinter.Tk()
        root.withdraw()
        
        path = filedialog.askdirectory(parent=root,initialdir = str("./"),title=str("Please select a Output directory") )
        path += str("/")
        self.Output_Directory_LE.setText(path)

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pcbWindow = MainWindow()
    pcbWindow.show()
    app.exec_()