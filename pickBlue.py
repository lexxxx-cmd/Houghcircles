import cv2
import numpy as np
def blue(adress):

    # 读取图片
    image = cv2.imread(adress)

    img_copy = image.copy()
    img_copy=cv2.resize(img_copy,None,fx=0.25,fy=0.25,interpolation=cv2.INTER_AREA)
    cv2.imshow('img_copy', img_copy)
    cv2.waitKey(0)
    """
    提取图中的蓝色部分 hsv范围可以自行优化
    cv2.inRange()
    参数介绍：
    第一个参数：hsv指的是原图
    第二个参数：在图像中低于这个数值的全部变为0
    第二个参数：在图像中高于这个数值的全部变为0
    在之间的变为255
    图像中0-255。是变得越来越亮的
    """
    hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)
    # cv2.imshow('hsv', hsv)
    # cv2.waitKey(0)
    low_hsv = np.array([100, 80, 80])  # 这里的阈值是自己进行设置的
    high_hsv = np.array([115, 255, 255])
    # 设置HSV的阈值
    mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)
    # cv2.imshow('mask', mask)
    # cv2.waitKey(0)
    # show_pic('hsv_color_find', mask)#这里是得到黑白颜色的图片
    # 将掩膜与图像层逐像素相加
    # cv2.bitwise_and()是对二进制数据进行“与”操作，即对图像（灰度图像或彩色图像均可）每个像素值进行二进制“与”操作，1&1=1，1&0=0，0&1=0，0&0=0
    res = cv2.bitwise_and(img_copy, img_copy, mask=mask)
    # cv2.imshow('res', res)
    # cv2.waitKey(0)

    # show_pic('hsv_color_find2',res)#在这里得到蓝底黑字的照片
    print('hsv提取蓝色部分完毕')

    # 定义膨胀和腐蚀的核
    kernel = np.ones((5, 5), np.uint8)
    # 腐蚀操作
    eroded_image = cv2.erode(res, kernel, iterations=2)

    # 膨胀操作
    dilated_image = cv2.dilate(eroded_image, kernel, iterations=2)
    # cv2.imshow('dilated_image', dilated_image)
    # cv2.waitKey(0)
    imagegray = cv2.cvtColor(dilated_image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('image', imagegray)
    # cv2.waitKey(0)
    
    # edge = cv2.Canny(imagegray,50,100)
    # cv2.imshow('image', edge)
    # cv2.waitKey(0)

    #0.9以上对有缺陷的小圆检测不明显，只能在调小该参数同时调整最小距离以免重复
    circles=cv2.HoughCircles(imagegray,cv2.HOUGH_GRADIENT_ALT,dp=1,minDist=30,param1=100,param2=0.8)
    if circles is not None:
        count=0
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:#对每个检测到的圆形,格式为(x,y,r)
            if(1):#与固定轴线的x距离不超过十个像素点，则确定为目标，这里先设置为永真
                count+=1
                # 绘制圆形的边缘
                cv2.circle(img_copy, (i[0], i[1]), i[2], (0, 255, 0), 1)
                # 绘制圆形的中心
                cv2.circle(img_copy, (i[0], i[1]), 1, (0, 0, 255), 3)
                
        cv2.imshow('ss',img_copy)
        cv2.waitKey(0)
        if(count==0):
            print("没有符合要求的圆形")
    else:
        print("未检测成功")
    return circles
