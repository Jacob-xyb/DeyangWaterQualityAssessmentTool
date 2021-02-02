import os
from osgeo import gdal
import pandas as pd


def is_already_exist(filename): #判断给出的路径对应文件是否存在，存在则读取数据，不存在则报错
    if os.path.exists(filename):
        return True
    else:
        return False

def read_xy(path):#读坐标
    """
       读取坐标，一般一期文件读一次就行
       :param path: 路径文件
       :return: 存储XY坐标的列表，def[0] is X ; def[1] is Y.
       """
    '''tiff坐标提取'''  # 两列
    if (is_already_exist(path) == False):
        print('该文件不存在！')
    else:
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
        for i in range(nXSize * nYSize):
            cdnX.append(arrSlope[i][0])
            cdnY.append(arrSlope[i][1])
        return cdnX, cdnY

def read_tiff(path, num=1, key=None):#默认单波段
    """
    固定成了单波段
    :param path: tiff 文件所在的目录，单个字符串，最好加 r 前缀
    :return: list
    """
    if(is_already_exist(path)==False):
        print('该文件不存在！')
    else:
        dataset = gdal.Open(path)
        nXSize = dataset.RasterXSize  # 列数
        nYSize = dataset.RasterYSize  # 行数
        band = dataset.GetRasterBand(num)  # 获取波段
        data = band.ReadAsArray(0, 0, nXSize, nYSize)  # data为numpy格式
        # dataDF = pd.DataFrame(data)
        data_list = []
        if key == True:
            for i in range(nYSize):
                for j in range(nXSize):
                    # if data[i, j] > 0:
                    data_list.append(data[i, j])
                    # else:
                    #     data_list.append(-999)
        else:
            for i in range(nYSize):
                for j in range(nXSize):
                    if data[i, j] > 0:
                        data_list.append(data[i, j])
                    else:
                        data_list.append(-999)
            # print(len(data_list))
        return data_list


def read_band(path, target, num=0, key=None):
    """
    :param path: 全波段文件路径
    :param num: 默认值为0，表示全波段读取；若指定数字，则读取指定波段
    :param key:
    :effect：生成excel文件包含全波段数据
    """
    #还可以加一个判断path中图像是不是单波段的函数
    if (is_already_exist(path) == False):
        print('该文件不存在！')
    else:
        dataset = gdal.Open(path)
        try:
            nob = dataset.RasterCount#单波段图像打开后是没有RasterCount的，会报错，这里捕捉报错
        except:
            df = pd.read_excel(path, index_col=0)  # excel里面已经有一列标签 index_col=0
            if key == None:
                return df
            else:
                return df.head(key)#报错代表读的是单波段
        else:#不报错就是多波段，直接执行
            #print("请输入查询波段:")
            #num=input()
            dataset = gdal.Open(path)
            nXSize = dataset.RasterXSize  # 列数
            nYSize = dataset.RasterYSize  # 行数
            df_list = []
            if num == 0:
                for i in range(1, nob + 1):
                    band = dataset.GetRasterBand(i)  # 获取波段
                    data = band.ReadAsArray(0, 0, nXSize, nYSize)  # data为numpy格式
                    data_list = []
                    for j in range(nYSize):
                        data_list = [*data_list, *data[j]]
                    df_list.append(data_list)
            else:
                band = dataset.GetRasterBand(num)  # 获取波段
                data = band.ReadAsArray(0, 0, nXSize, nYSize)  # data为numpy格式
                for j in range(nYSize):
                    df_list = [*df_list, *data[j]]
            # print(len(df_list))
            df = pd.DataFrame(df_list)
            #print(df.shape)
            df = df.transpose() # 行列转换

            '''写入部分'''
            writer = pd.ExcelWriter(target)  # 写入Excel文件
            df.to_excel(writer, float_format='%.5f')  # ‘page_1’是写入excel的sheet名 # 不写就是默认第一页
            writer.save()
            writer.close()