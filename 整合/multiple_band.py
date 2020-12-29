import pandas as pd
from GET import  *

def get_data_M():
    print('请输入多波段图像表格路径:')
    path = input()
    ref = pd.read_excel(path, index_col=0)
    path_tiff = "E://shixi//github_mycellar//水质参数//s2b20200317waterRrs_"
    path1 = "CHLAz.tif"
    path2 = "SDz.tif"
    path3 = "TNz.tif"
    path4 = "TPz.tif"
    path5 = "E://shixi//github_mycellar//水质参数//0317after_12.tif"
    path6 = path5#上述所有路径都可以换成excel里读
    read_band(path_tiff + path1, target="C://Users//Administrator//Desktop//12波段.xlsx")  # 读全波段并生成excel
    # exit()
    #下一步可以改为输入计算的波段数
    XY = read_xy(path5) #这里用path1就可以了，因为手上没有CHLA的多波段图才用的path5
    cdnX, cdnY = XY[0], XY[1]
    CHLA = read_tiff(path_tiff + path1)
    SD = read_tiff(path_tiff + path2)
    TN = read_tiff(path_tiff + path3)
    TP = read_tiff(path_tiff + path4)
    NIR_8 = read_tiff(path5, num=8, key=True)
    # NIR_9 = read_tiff(path5, num=9, key=True)
    R = read_tiff(path5, num=4, key=True)
    NDVI_8 = [0] * len(NIR_8)
    # NDVI_9 = [0] * len(SD)
    for i in range(len(NIR_8)):
        NDVI_8[i] = (NIR_8[i] - R[i]) / (NIR_8[i] + R[i])

    R665 = read_tiff(path6, num=4, key=True)
    R842 = read_tiff(path6, num=8, key=True)
    R1610 = read_tiff(path6, num=11, key=True)
    # R842_ = R665 + (R1610-R665)*(842-665)/(1610-665)
    R842_ = [R665[i] + (R1610[i] - R665[i]) * (842 - 665) / (2190 - 665)
             for i in range(len(R665))]
    # FAI = R842 - R842_
    FAI = [R842[i] - R842_[i] for i in range(len(R842))]
    dict = {'X': cdnX, 'Y': cdnY, 'CHLA': CHLA,
            'SD': SD, 'TP': TP, 'TN': TN, 'NDVI': NDVI_8, 'FAI': FAI}
    df = pd.DataFrame(data=dict)

    """清洗异常值"""
    for col in df.columns:  # df1.columns : 列名称的list
        # print(col)  # col为一个个列名
        df.drop(index=(df.loc[(df[col] == -999)].index), inplace=True)
        # df.drop(index=(df[df[col].isin([-999])].index), inplace=True)
        # df.reset_index(inplace=True)  # 重置索引，但会保留原索引
        df.reset_index(drop=True, inplace=True)  # 重置索引，不会保留原索引

    """写入部分"""
    path_multiple="./" + "多波段图计算结果.xlsx"
    writer = pd.ExcelWriter(path_multiple)  # 写入Excel文件
    df.to_excel(writer, float_format='%.5f')  # ‘page_1’是写入excel的sheet名 # 不写就是默认第一页
    writer.save()
    writer.close()
    return path_multiple

   # NIR_8 = read_tiff(path_tiff+path4, num=1, key=True)
   # NIR_9 = read_tiff(path5, num=9, key=True)
   # R = read_tiff(path5, num=4, key=True)
   # NDVI_8 = [0] * len(NIR_8)
    # NDVI_9 = [0] * len(SD)
   # for i in range(len(NIR_8)):
    #    NDVI_8[i] = (NIR_8[i] - R[i]) / (NIR_8[i] + R[i])
    # FAI01 = read_tiff(path_tiff+path5)
    # NDVI = read_tiff(path_tiff + path6, 1)

    # print(cdnX[0])
    # 创建DataFrame
    # data n= [cdnX, cdnY, CHLA, SD, TN, TP]
    # columns = ['X', 'Y', 'CHLA', 'SD', 'TP', 'TN']

    # df.drop(index=df[df['CHLA'].isin([-999])].index[0], inplace=True)  # 只删除了一行
    # df['CHLA'].isin([-999])  # Name: CHLA, Length: 210748, dtype: bool
    # df1 = df[df['CHLA'].isin([-999])]  # 包含-999的DataFrame
    # df.drop(index=df[df['CHLA'] < 0].index[0], inplace=True)  # 只删除了一行
    # df.drop(index=(df.loc[(df['CHLA'] == -999)].index), inplace=True)  # 可删除多行 # 只允许有一个key
    # 清洗异常值