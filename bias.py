import cv2
import numpy as np
def center_loc(
        address,

        #图像预处理操作
        gray=True,
        enhance=True,
        binary=True,
        blur=True,
        fliter=True,

        fx=0.25,
        fy=0.25,
        clipLimit=255.0,
        bi_threshold=99,
        minDist=100,
        param1=80,
        param2=0.9,
        minRadius=50, 
        maxRadius=120,
        threhsold=60):
    '''
    Param address:目标图片地址
    return (检测圆心到图片中心x像素距离,检测圆心到图片中心y像素距离)
    未成功检测会返回(None,None)

    负数表示要向右或者向下移动
    '''
    print('------------')
    #读取输入地址的图片
    image = cv2.imread(address)
    #固定输入2048*2448然后resize
    image=cv2.resize(image,None,fx=fx,fy=fy,interpolation=cv2.INTER_AREA)
    res = image
    #确定中线,预先设定，这里先假设为下例(x,y)，用于后续判断合理圆心位置
    mid_line = int(res.shape[1]*0.536)
    #图片中心(x,y)
    center = [res.shape[1]//2,res.shape[0]//2]


    #预处理
    #灰度
    if gray:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('bw',image)
        # cv2.waitKey(0)
    
   
    # 增强对比度cliplimit越大越黑白
    if enhance:
        clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=(8, 8))
        image = clahe.apply(image)
        # cv2.imshow('eg',image)
        # cv2.waitKey(0)
    
    if blur:
        # 对图像进行模糊处理，以减少噪声
        image = cv2.GaussianBlur(image, (5, 5), 2)
        # cv2.imshow('bw',image)
        # cv2.waitKey(0)
    if fliter:
        # 应用拉普拉斯滤波器
        # image = cv2.Laplacian(image, cv2.CV_8U)
        # cv2.imshow('bw',image)
        # cv2.waitKey(0)
        # 定义锐化卷积核
        kernel = np.array([[-1, -1, -1],
                   [-1, 9, -1],
                   [-1, -1, -1]], dtype=np.float32)
        kernel2 = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]], dtype=np.float32)

        # 应用卷积核进行图像滤波
        image = cv2.filter2D(image, -1, kernel2)
        # cv2.imshow('eg',image)
        # cv2.waitKey(0)
    #二值化
    if binary:
        _, image = cv2.threshold(image, bi_threshold, 255, cv2.THRESH_BINARY)
        # cv2.imshow('bg',image)
        # cv2.waitKey(0)

    #检测
    # 霍夫圆变换检测圆形，返回列表
    circles = cv2.HoughCircles(
    image,
    cv2.HOUGH_GRADIENT_ALT,
    dp=1,
    minDist=minDist, #圆之间的最小距离，只用检测一个圆所以尽量调大点，后期设为resize图的一半大小
    param1=param1,
    param2=param2,
    minRadius=minRadius, 
    maxRadius=maxRadius#(614, 734, 3)大小的图片对应80-100的半径,旋钮半径大约图短边0.14~0.16
    )



    if circles is not None:
        count=0
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:#对每个检测到的圆形,格式为(x,y,r)
            if(abs(i[0]-mid_line)<=threhsold):#与固定轴线的x距离不超过十个像素点，则确定为目标
                count+=1
                # cv2.imshow('prototype',image)
                # cv2.waitKey(0)
                # 绘制圆形的边缘
                cv2.line(res,(mid_line,0),(mid_line,res.shape[0]),(255, 0, 0), 2)
                cv2.circle(res, (i[0], i[1]), i[2], (0, 255, 0), 1)
                # 绘制圆形的中心
                cv2.circle(res, (i[0], i[1]), 1, (0, 0, 255), 3)
                cv2.circle(res, (center[0], center[1]), 2, (0, 0, 255), 3)
                cv2.imshow('ss',res)
                cv2.waitKey(0)

                #算距离，开头缩小四倍，这里放大四倍
                pixel_x=4*(circles[0][0][0]-center[0])
                pixel_y=4*(circles[0][0][1]-center[1])

                return pixel_x,pixel_y
        if(count==0):
            print("没有符合要求的圆形")
            return None,None
        cv2.imshow('ss',res)
        cv2.waitKey(0)
    else:
        print("未检测成功")
        return None,None


def pad(image, target_size, pad_color=0):
    """
    将小图像填充到固定大小。

    :param image: 输入图像
    :param target_size: 目标大小 (width, height)
    :param pad_color: 填充颜色 (默认为黑色)
    :return: 填充后的图像
    """
    original_height, original_width = image.shape[:2]
    target_height, target_width = target_size

    # 计算需要填充的像素
    delta_width = max(0, target_width - original_width)
    delta_height = max(0, target_height - original_height)

    top = delta_height // 2
    bottom = delta_height - top
    left = delta_width // 2
    right = delta_width - left

    # 填充图像
    padded_image = cv2.copyMakeBorder(
        image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=pad_color
    )
    
    # 如果原图像大于目标尺寸，则进行裁剪
    if padded_image.shape[0] > target_height or padded_image.shape[1] > target_width:
        padded_image = cv2.resize(image,target_size,interpolation=cv2.INTER_AREA)

    return padded_image
