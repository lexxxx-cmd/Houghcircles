import cv2

def square(image,square_size):
    """
    param image: 输入图像
    param square_size: 正方形的边长
    """
    if image is None:
        raise ValueError(f"图像为空")
    #计算中心点
    h, w = image.shape[:2]
    center_x = w // 2
    center_y = h // 2
    
    #四个顶点坐标
    half_size = square_size // 2
    top_left = (center_x - half_size, center_y - half_size)
    top_right = (center_x + half_size, center_y - half_size)
    bottom_left = (center_x - half_size, center_y + half_size)
    bottom_right = (center_x + half_size, center_y + half_size)
    
    #颜色和线条粗细
    color1 = (0, 255, 0) 
    color2 = (0, 0, 255) 
    color3 = (255, 0, 0) 
    thickness = 1 
    
    #正方形
    cv2.rectangle(image,top_left,bottom_right,color1,thickness)
    #斜线
    cv2.line(image,top_left,bottom_right,color2,thickness)
    cv2.line(image,top_right,bottom_left,color2,thickness)
    #中心
    cv2.circle(image,(center_x,center_y),2,color3,thickness)



    
    return image

#测试
path = 'DMM68.jpg'
image = cv2.imread(path)

square_size =int(0.4*min(image.shape[0],image.shape[1]))   # 自适应正方形的边长
image1 = square(image,square_size)
cv2.imshow('Image with Center Square', image1)
cv2.waitKey(0)
cv2.destroyAllWindows()