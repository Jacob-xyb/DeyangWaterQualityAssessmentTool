from osgeo import gdal
import numpy as np
import pandas as pd
import xlsxwriter


def read_tiff(path, key = None):
    """
    固定成了单波段
    :param path: tiff 文件所在的目录，单个字符串，最好加 r 前缀
    :return: list
    """
    dataset = gdal.Open(path)
    # print(dataset.GetDescription())  # 数据描述
    # print(dataset.RasterCount)  # 波段数
    nXSize = dataset.RasterXSize  # 列数
    nYSize = dataset.RasterYSize  # 行数
    band = dataset.GetRasterBand(1)  # 获取波段
    # print(nXSize, nYSize)
    data = band.ReadAsArray(0, 0, nXSize, nYSize)  # data为numpy格式
    # dataDF = pd.DataFrame(data)
    data_list = []
    for i in range(nYSize):
        for j in range(nXSize):
            if data[i, j] >= 0:
                data_list.append(data[i, j])
            elif key == 1:   # 读取NDVI，小于-1异常值及NA设置为-2
                if data[i, j] > -1:
                    data_list.append(data[i, j])
                else:
                    data_list.append(-2)
            else:
                data_list.append(-999)
    return data_list

def read_xy(path):
    """
    读取坐标，一般一期文件读一次就行
    :param path: 路径文件
    :return: 存储XY坐标的列表，def[0] is X ; def[1] is Y.
    """
    '''tiff坐标提取'''  # 两列
    gdal.AllRegister()  # 注册所有已知的驱动，包括动态库自动加载的驱动
    dataset = gdal.Open(path)
    adfGeoTransform = dataset.GetGeoTransform()
    # # 左上角地理坐标
    # print(adfGeoTransform[0])
    # print(adfGeoTransform[3])
    nXSize = dataset.RasterXSize  # 列数
    nYSize = dataset.RasterYSize  # 行数
    print(nXSize, nYSize)
    arrSlope = []  # 用于存储每个像素的（X，Y）坐标
    for i in range(nYSize):  # 注意XY不要写反
        # row = []
        for j in range(nXSize):
            px = adfGeoTransform[0] + j * adfGeoTransform[1] + i * adfGeoTransform[2]
            py = adfGeoTransform[3] + j * adfGeoTransform[4] + i * adfGeoTransform[5]
            # GT(0)和GT(3)是第一组，表示图像左上角的地理坐标；
            # GT(1)和GT(5)是第二组，表示图像横向和纵向的分辨率（一般这两者的值相等，符号相反，横向分辨率为正数，纵向分辨率为负数）；
            # GT(2)和GT(4)是第三组，表示图像旋转系数，对于一般图像来说，这两个值都为0。
            col = [px, py]
            arrSlope.append(col)
    cdnX, cdnY = [], []  # 用于分别存储每个像素的(x,y)坐标
    for i in range(nXSize*nYSize):
        cdnX.append(arrSlope[i][0])
        cdnY.append(arrSlope[i][1])
    return cdnX, cdnY


if __name__ == '__main__':
    path_tiff = r"/Users/ethan/Desktop/newfiber/xyb/德阳/20200317"
    path1 = r"/s2b20200317waterRrs_CHLAz.tif"
    path2 = r"/s2b20200317waterRrs_SDz.tif"
    path3 = r"/s2b20200317waterRrs_TNz.tif"
    path4 = r"/s2b20200317waterRrs_TPz.tif"
    path5 = r"/s2b20200317waterRrs_NDVIz.tif"
    path6 = r"/s2b20200317waterRrs_FAI01z.tif"

    XY = read_xy(path_tiff+path1)
    cdnX, cdnY = XY[0], XY[1]
    CHLA = read_tiff(path_tiff+path1)
    SD = read_tiff(path_tiff+path2)
    TN = read_tiff(path_tiff+path3)
    TP = read_tiff(path_tiff+path4)
    NDVI = read_tiff(path_tiff+path5, 1)
    FAI01 = read_tiff(path_tiff+path6)

    # print(cdnX[0])
    # 创建DataFrame
    # data n= [cdnX, cdnY, CHLA, SD, TN, TP]
    # columns = ['X', 'Y', 'CHLA', 'SD', 'TP', 'TN']
    dict = {'X': cdnX, 'Y': cdnY, 'CHLA': CHLA,
            'SD': SD, 'TP': TP, 'TN': TN, 'FAI01':FAI01, 'NDVI':NDVI}
    df = pd.DataFrame(data=dict)
    # df.drop(index=df[df['CHLA'].isin([-999])].index[0], inplace=True)  # 只删除了一行
    # df['CHLA'].isin([-999])  # Name: CHLA, Length: 210748, dtype: bool
    # df1 = df[df['CHLA'].isin([-999])]  # 包含-999的DataFrame 
    # df.drop(index=df[df['CHLA'] < 0].index[0], inplace=True)  # 只删除了一行
    # df.drop(index=(df.loc[(df['CHLA'] == -999)].index), inplace=True)  # 可删除多行 # 只允许有一个key
    # 清洗异常值
    for col in df.columns:  # df1.columns : 列名称的list
        #print(col)  # col为一个个列名
        #df.drop(index=(df.loc[(df[col] == -999)].index), inplace=True)
        df.drop(index=(df[df[col].isin([-999])].index), inplace=True) #清洗4个指标
        df.drop(index=(df[df[col].isin([-2])].index), inplace=True) #清洗NDVI
        # df.reset_index(inplace=True)  # 重置索引，但会保留原索引
        df.reset_index(drop=True, inplace=True)  # 重置索引，不会保留原索引
    # print(df)

    """写入部分"""
    writer = pd.ExcelWriter(r'../../../德阳/s2b_20200317_waterRrs.xlsx')  # 写入Excel文件
    df.to_excel(writer, float_format='%.5f')  # ‘page_1’是写入excel的sheet名 # 不写就是默认第一页
    writer.save()
    writer.close()






