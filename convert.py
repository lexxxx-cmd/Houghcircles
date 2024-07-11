def sort(circles):
    '''
    param : circles是霍夫检测返回的包含各个圆的[x,y,r]列表
    return : 返回从左上到右下排好序的列表
    '''


    c = circles[0]
    #先按y分组排序
    sorted_c = c[c[:,1].argsort()]
    len_sc = len(sorted_c)
    # print(sorted_c)
    # print('---')
    ssorted_c  =[]
    counts=[]
    count=0
    #第一个的y坐标
    flag =sorted_c[0][1]


    for i,item in enumerate(sorted_c,1):#主要做组别分类
        if abs(item[1]-flag)<=5 and i<=len_sc:
            #说明是一行的
            count+=1
            if(i==len_sc):
                counts.append(count)
                break
        else:
            counts.append(count)
            flag=item[1]

   
    listNum = len(counts)
    for i in range(listNum-1):
        counts[3-i] = counts[3-i]-counts[2-i]+1
    #需要一个计数的，和放不同组别园的列表
    flag1 =0
    list_temp = []
    #按counts中分好的组去分别排序x,counts有多长就有几组先截出来
    for i in range(listNum):
        if i==0:
            list_temp.append(sorted_c[flag1:counts[i]])
            flag1 = counts[i]
        else:
            list_temp.append(sorted_c[flag1:flag1+counts[i]])
            flag1 = flag1+counts[i]

    print(list_temp)
    #分好组后对每一组排序
    for i in range(listNum):
        ssorted_c.extend(list_temp[i][list_temp[i][:,0].argsort()])
    
    return ssorted_c



    
