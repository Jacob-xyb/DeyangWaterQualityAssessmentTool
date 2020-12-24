from osgeo import gdal
import numpy as np
import pandas as pd
import xlsxwriter
import math

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
    for i in range(nXSize * nYSize):
        cdnX.append(arrSlope[i][0])
        cdnY.append(arrSlope[i][1])
    return cdnX, cdnY
def read_band(path, head=None):
    """
    :param path: 存储 band 文件所在的目录，单个字符串，最好加 r 前缀
    :return: df band全部数据
    """
    df = pd.read_excel(path, index_col=0)  # excel里面已经有一列标签 index_col=0
    if head == None:
        return df
    else:
        return df.head(head)
def surface_rank2(df, list_tar):
        df = df
        list_tar = list_tar
        dict = {}

        def surface_tar(str_tar):  # 地表水单指标分类
            """
            :param str_tar: 需要评价的指标 字符串类型
            :return: list，评价结果
            """
            surface_tar = {'TP': [0.01, 0.025, 0.05, 0.1, 0.2],
                           'TN': [0.2, 0.5, 1.0, 1.5, 2.0]}  # 水质指标 # dic
            list_str_tar = df[str_tar].tolist()
            for i in range(len(list_str_tar)):
                data = list_str_tar[i]  # 收取指定行数据
                if data <= surface_tar[str_tar][0]:
                    list_str_tar[i] = 1
                elif surface_tar[str_tar][0] < data <= surface_tar[str_tar][1]:
                    list_str_tar[i] = 2
                elif surface_tar[str_tar][1] < data <= surface_tar[str_tar][2]:
                    list_str_tar[i] = 3
                elif surface_tar[str_tar][2] < data <= surface_tar[str_tar][3]:
                    list_str_tar[i] = 4
                elif surface_tar[str_tar][3] < data <= surface_tar[str_tar][4]:
                    list_str_tar[i] = 5
                else:
                    list_str_tar[i] = 6

            return list_str_tar

        def max_bad_tar(dict):  # 算出最坏水质
            df = pd.DataFrame(data=dict)
            series_max = df.max(axis=1)
            list_max = series_max.tolist()
            return list_max

        for i in range(len(list_tar)):
            dict[list_tar[i]] = surface_tar(list_tar[i])
        return max_bad_tar(dict)
def TLI_rank2(df, list_tar):
    """
    TLI函数是 surface_tar() +(内嵌) toTLI()
    最坏水质需要改动,在两函数中间插入整合
    :param df:
    :param list_tar:
    :return:
    """
    df = df
    list_tar = list_tar
    dict = {}
    def TLI_tar(list_tar):  # 综合营养状态单指标分类
        """
        :param str_tar: 需要评价的指标 字符串类型
        :return: list，评价结果
        """
        def toTLI(str_tar):
            """
            :param str_tar: 单个字符串
            :return: 转换后的列表
            """
            list_str_tar = df[str_tar].tolist()  # 将每个水质函数提出，转化为列表
            for i in range(len(list_str_tar)):
                data = list_str_tar[i]
                # 依据类型制定不同的转换方式
                if str_tar == 'CHLA':
                    list_str_tar[i] = 10*(2.5+1.086*math.log(data))  # 10(2.5+1.086lnCHLA)
                elif str_tar == 'TP':
                    list_str_tar[i] = 10*(9.436+1.6241*math.log(data))  # 10(9.436+1.6241lnTP)
                elif str_tar == 'TN':
                    list_str_tar[i] = 10*(5.45+1.6941*math.log(data))  # 10(5.45+1.6941lnTN)
                elif str_tar == 'SD':
                    list_str_tar[i] = 10*(5.45+1.6941*math.log(data))  # 10(5.118-1.941lnSD)
                else:
                    print('参数对应不上')
            return list_str_tar

        def sum_tar(dict):  # 算出总的TLI
            df = pd.DataFrame(data=dict)
            series_sum = df.sum(axis=1)
            list_max = series_sum.tolist()
            list_max = [x/len(dict.keys()) for x in list_max]
            return list_max
        # surface_tar = {'TP': [0.01, 0.025, 0.05, 0.1, 0.2],
        #                'TN': [0.2, 0.5, 1.0, 1.5, 2.0]}  # 地表水水质指标 # dic
        # TLI/TSI_tar = [["贫营养"中营养"轻度富营养"中度~"重度~"][30, 50, 60, 70]]
        # list_str_tar = df[str_tar].tolist()

        for i in range(len(list_tar)):
            dict[list_tar[i]] = toTLI(list_tar[i])  # 生成 e.g: {"TN": values}
        list_str_tar = sum_tar(dict)
        for i in range(len(list_str_tar)):
            data = list_str_tar[i]  # 收取指定行数据
            if data <= 30:
                list_str_tar[i] = 1
            elif 30 < data <= 50:
                list_str_tar[i] = 2
            elif 50 < data <= 60:
                list_str_tar[i] = 3
            elif 60 < data <= 70:
                list_str_tar[i] = 4
            elif 70 < data:
                list_str_tar[i] = 5
        return list_str_tar

    return TLI_tar(list_tar)
def TSI_rank2(df, list_tar):
    """
    TSI函数是 TLI函数改编
    最坏水质需要改动,在两函数中间插入整合
    :param df:
    :param list_tar:
    :return:
    """
    df = df
    list_tar = list_tar
    dict = {}
    def TSI_tar(list_tar):  # 综合营养状态单指标分类
        """
        :param str_tar: 需要评价的指标 字符串类型
        :return: list，评价结果
        """
        def toTSI(str_tar):
            """
            :param str_tar: 单个字符串
            :return: 转换后的列表
            """
            list_str_tar = df[str_tar].tolist()  # 将每个水质函数提出，转化为列表
            for i in range(len(list_str_tar)):
                data = list_str_tar[i]
                # 依据类型制定不同的转换方式
                if str_tar == 'CHLA':
                    list_str_tar[i] = (9.81*math.log(data))+30.6  # 9.81 "Ln" chlorophyll ɑ （μg/L）+30.6
                elif str_tar == 'TP':
                    list_str_tar[i] = (14.42*math.log(data))+4.15  # 14.42 Ln total phosphorus （μg/L）+4.15
                # elif str_tar == 'TN':
                #     pass
                elif str_tar == 'SD':
                    list_str_tar[i] = 60-(14.4*math.log(data))  # 60-14.4 "Ln" Secchi disk depth （meters）
                else:
                    print('参数对应不上')
            # print(list_str_tar)
            return list_str_tar

        def sum_tar(dict):  # 算出总的TSI
            df = pd.DataFrame(data=dict)
            series_sum = df.sum(axis=1)
            list_max = series_sum.tolist()
            list_max = [x/len(dict.keys()) for x in list_max]
            return list_max
        # surface_tar = {'TP': [0.01, 0.025, 0.05, 0.1, 0.2],
        #                'TN': [0.2, 0.5, 1.0, 1.5, 2.0]}  # 地表水水质指标 # dic
        # TLI/TSI_tar = [["贫营养"中营养"轻度富营养"中度~"重度~"][30, 50, 60, 70]]
        # list_str_tar = df[str_tar].tolist()

        for i in range(len(list_tar)):
            dict[list_tar[i]] = toTSI(list_tar[i])  # 生成 e.g: {"TN": values}
        list_str_tar = sum_tar(dict)
        for i in range(len(list_str_tar)):
            data = list_str_tar[i]  # 收取指定行数据
            if data <= 30:
                list_str_tar[i] = 1
            elif 30 < data <= 50:
                list_str_tar[i] = 2
            elif 50 < data <= 60:
                list_str_tar[i] = 3
            elif 60 < data <= 70:
                list_str_tar[i] = 4
            elif 70 < data:
                list_str_tar[i] = 5
        return list_str_tar

    return TSI_tar(list_tar)

def surface_rank3(df, list_tar):
    df = df
    list_tar = list_tar
    dict = {}

    def surface_tar(str_tar):  # 地表水单指标分类
        """
        :param str_tar: 需要评价的指标 字符串类型
        :return: list，评价结果
        """
        surface_tar = {'TP': [0.01, 0.025, 0.05, 0.1, 0.2],
                       'TN': [0.2, 0.5, 1.0, 1.5, 2.0]}  # 水质指标 # dic
        list_str_tar = df[str_tar].tolist()
        for i in range(len(list_str_tar)):
            data = list_str_tar[i]  # 收取指定行数据
            if data <= surface_tar[str_tar][0]:
                list_str_tar[i] = 1
            elif surface_tar[str_tar][0] < data <= surface_tar[str_tar][1]:
                list_str_tar[i] = 2
            elif surface_tar[str_tar][1] < data <= surface_tar[str_tar][2]:
                list_str_tar[i] = 3
            elif surface_tar[str_tar][2] < data <= surface_tar[str_tar][3]:
                list_str_tar[i] = 4
            elif surface_tar[str_tar][3] < data <= surface_tar[str_tar][4]:
                list_str_tar[i] = 5
            else:
                list_str_tar[i] = 6

        return list_str_tar

    def max_bad_tar(dict):  # 算出最坏水质
        df = pd.DataFrame(data=dict)
        series_max = df.max(axis=1)
        list_max = series_max.tolist()
        return list_max

    for i in range(len(list_tar)):
        dict[list_tar[i]] = surface_tar(list_tar[i])

    # 新添加 to 整合版
    # 大写罗马数字： Ⅰ Ⅱ Ⅲ Ⅳ Ⅴ
    surface_rank = max_bad_tar(dict)
    for i in range(len(surface_rank)):
        data = surface_rank[i]
        if data == 1:
            surface_rank[i] = "Ⅰ类"
        elif data == 2:
            surface_rank[i] = "Ⅱ类"
        elif data == 3:
            surface_rank[i] = "Ⅲ类"
        elif data == 4:
            surface_rank[i] = "Ⅳ类"
        elif data == 5:
            surface_rank[i] = "Ⅴ类"
        elif data == 6:
            surface_rank[i] = "劣Ⅴ类"

    return surface_rank
def TLI_rank3(df, list_tar):
    """
    TLI函数是 surface_tar() +(内嵌) toTLI()
    最坏水质需要改动,在两函数中间插入整合
    :param df:
    :param list_tar:
    :return:
    """
    df = df
    list_tar = list_tar
    dict = {}
    def TLI_tar(list_tar):  # 综合营养状态单指标分类
        """
        :param str_tar: 需要评价的指标 字符串类型
        :return: list，评价结果
        """
        def toTLI(str_tar):
            """
            :param str_tar: 单个字符串
            :return: 转换后的列表
            """
            list_str_tar = df[str_tar].tolist()  # 将每个水质函数提出，转化为列表
            for i in range(len(list_str_tar)):
                data = list_str_tar[i]
                # 依据类型制定不同的转换方式
                if str_tar == 'CHLA':
                    list_str_tar[i] = 10*(2.5+1.086*math.log(data))  # 10(2.5+1.086lnCHLA)
                elif str_tar == 'TP':
                    list_str_tar[i] = 10*(9.436+1.6241*math.log(data))  # 10(9.436+1.6241lnTP)
                elif str_tar == 'TN':
                    list_str_tar[i] = 10*(5.45+1.6941*math.log(data))  # 10(5.45+1.6941lnTN)
                elif str_tar == 'SD':
                    list_str_tar[i] = 10*(5.45+1.6941*math.log(data))  # 10(5.118-1.941lnSD)
                else:
                    print('参数对应不上')
            return list_str_tar

        def sum_tar(dict):  # 算出总的TLI
            df = pd.DataFrame(data=dict)
            series_sum = df.sum(axis=1)
            list_max = series_sum.tolist()
            list_max = [x/len(dict.keys()) for x in list_max]
            return list_max
        # surface_tar = {'TP': [0.01, 0.025, 0.05, 0.1, 0.2],
        #                'TN': [0.2, 0.5, 1.0, 1.5, 2.0]}  # 地表水水质指标 # dic
        # TLI/TSI_tar = [["贫营养"中营养"轻度富营养"中度~"重度~"][30, 50, 60, 70]]
        # list_str_tar = df[str_tar].tolist()

        for i in range(len(list_tar)):
            dict[list_tar[i]] = toTLI(list_tar[i])  # 生成 e.g: {"TN": values}
        list_str_tar = sum_tar(dict)
        for i in range(len(list_str_tar)):
            data = list_str_tar[i]  # 收取指定行数据
            if data <= 30:
                list_str_tar[i] = "贫营养"
            elif 30 < data <= 50:
                list_str_tar[i] = "中营养"
            elif 50 < data <= 60:
                list_str_tar[i] = "轻度富营养"
            elif 60 < data <= 70:
                list_str_tar[i] = "中度富营养"
            elif 70 < data:
                list_str_tar[i] = "重度度富营养"
        return list_str_tar

    return TLI_tar(list_tar)
def TSI_rank3(df, list_tar):
    """
    TSI函数是 TLI函数改编
    最坏水质需要改动,在两函数中间插入整合
    :param df:
    :param list_tar:
    :return:
    """
    df = df
    list_tar = list_tar
    dict = {}
    def TSI_tar(list_tar):  # 综合营养状态单指标分类
        """
        :param str_tar: 需要评价的指标 字符串类型
        :return: list，评价结果
        """
        def toTSI(str_tar):
            """
            :param str_tar: 单个字符串
            :return: 转换后的列表
            """
            list_str_tar = df[str_tar].tolist()  # 将每个水质函数提出，转化为列表
            for i in range(len(list_str_tar)):
                data = list_str_tar[i]
                # 依据类型制定不同的转换方式
                if str_tar == 'CHLA':
                    list_str_tar[i] = (9.81*math.log(data))+30.6  # 9.81 "Ln" chlorophyll ɑ （μg/L）+30.6
                elif str_tar == 'TP':
                    list_str_tar[i] = (14.42*math.log(data))+4.15  # 14.42 Ln total phosphorus （μg/L）+4.15
                # elif str_tar == 'TN':
                #     pass
                elif str_tar == 'SD':
                    list_str_tar[i] = 60-(14.4*math.log(data))  # 60-14.4 "Ln" Secchi disk depth （meters）
                else:
                    print('参数对应不上')
            # print(list_str_tar)
            return list_str_tar

        def sum_tar(dict):  # 算出总的TSI
            df = pd.DataFrame(data=dict)
            series_sum = df.sum(axis=1)
            list_max = series_sum.tolist()
            list_max = [x/len(dict.keys()) for x in list_max]
            return list_max
        # surface_tar = {'TP': [0.01, 0.025, 0.05, 0.1, 0.2],
        #                'TN': [0.2, 0.5, 1.0, 1.5, 2.0]}  # 地表水水质指标 # dic
        # TLI/TSI_tar = [["贫营养"中营养"轻度富营养"中度~"重度~"][30, 50, 60, 70]]
        # list_str_tar = df[str_tar].tolist()

        for i in range(len(list_tar)):
            dict[list_tar[i]] = toTSI(list_tar[i])  # 生成 e.g: {"TN": values}
        list_str_tar = sum_tar(dict)
        for i in range(len(list_str_tar)):
            data = list_str_tar[i]  # 收取指定行数据
            if data <= 30:
                list_str_tar[i] = "贫营养"
            elif 30 < data <= 50:
                list_str_tar[i] = "中营养"
            elif 50 < data <= 60:
                list_str_tar[i] = "轻度富营养"
            elif 60 < data <= 70:
                list_str_tar[i] = "中度富营养"
            elif 70 < data:
                list_str_tar[i] = "重度富营养"
        return list_str_tar

    return TSI_tar(list_tar)