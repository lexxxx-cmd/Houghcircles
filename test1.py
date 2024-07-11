import os
from bias import center_loc
from pickBlue import blue
from convert import sort

#全放蓝色小圆图片的文件夹
image_folder ='blue'

#放转盘检测的文件夹
#image_folder ='photo/photo'

#对文件夹里的每个图片
for file in os.listdir(image_folder):
    img_path = os.path.join(image_folder,file)
    # #找圆心
    # dis_x,dis_y=center_loc(img_path,binary=False,param2=0.8)#346不行
    #     #2半径为50，3
    # if(dis_x!=None and dis_y!=None):  
    #     print(dis_x)
    #     print(dis_y)

    #找蓝色
    c=blue(img_path)
    print(c)
    print('----')
    sort(c)
    break
print(c)

        