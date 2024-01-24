import cv2
def CLAHE_Main(image, arr_ROIs , parameter) : # strRGB 아래 7개
    
    ycrcb_img = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    ycrcb_img[:, :, 0] = cv2.equalizeHist(ycrcb_img[:, :, 0])
    equalized_img = cv2.cvtColor(ycrcb_img, cv2.COLOR_YCrCb2BGR)
    b_plane = image[:, :, 0] # 파란색 채널
    g_plane = image[:, :, 1] # 초록색 채널
    r_plane = image[:, :, 2] # 빨간색 채널
    clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))


    if parameter == 'b' :
        b_plane = clahe.apply(b_plane)

    elif parameter == 'g' :
        g_plane = clahe.apply(g_plane)

    elif parameter == 'r' :
        r_plane = clahe.apply(r_plane)

    elif parameter == 'bg' :
        b_plane = clahe.apply(b_plane)
        g_plane = clahe.apply(g_plane)

    elif parameter == 'br' :
        b_plane = clahe.apply(b_plane)
        r_plane = clahe.apply(r_plane)

    elif parameter == 'gr' :
        g_plane = clahe.apply(g_plane)
        r_plane = clahe.apply(r_plane)
    
    elif parameter == 'bgr' :
        b_plane = clahe.apply(b_plane)
        g_plane = clahe.apply(g_plane)
        r_plane = clahe.apply(r_plane)
    
    
    CLAHE_Image = cv2.merge((b_plane, g_plane, r_plane))
    return CLAHE_Image , arr_ROIs