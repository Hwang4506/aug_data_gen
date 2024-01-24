import cv2

def Edge_Main( image , arr_ROIs, Min_Threshold=50 , Max_Threshold=200 ) :
    # 파라미터 (이미지, 최소 스레시 홀드, 최대 스레시홀드)
    # 추천값 앞값 > 50 , 뒤값 = 200
    Edge_Image = cv2.Canny( image, Min_Threshold , Max_Threshold )
    Edge_Image = cv2.cvtColor(Edge_Image, cv2.COLOR_GRAY2RGB)
    
    return Edge_Image , arr_ROIs