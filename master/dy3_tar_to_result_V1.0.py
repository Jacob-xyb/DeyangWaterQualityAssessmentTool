import pandas as pd       # 导入pandas模块
import math

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


def surface_rank(df, list_tar):
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


def TLI_rank(df, list_tar):
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


def TSI_rank(df, list_tar):
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


if __name__ == '__main__':
    '''读取部分'''
    path_band = r'D:\4.company\项目文件\四川\德阳\德阳水质评价\1德阳水质提取\德阳水质提取V1.0' +\
                '\s2b_20200216_waterRrs.xlsx'
    # df = read_band(path=path_band, head=200)
    df = read_band(path=path_band)
    '''计算部分'''
    surface = surface_rank(df=df, list_tar=["TP", "TN"])
    TLI = TLI_rank(df=df, list_tar=["CHLA", "SD", "TP", "TN"])
    TSI = TSI_rank(df=df, list_tar=["CHLA", "SD", "TP"])
    # print(surface)
    # print(TLI)
    # print(TSI)
    '''整合部分'''
    df_tar = df[["X", "Y"]]  # 多列时要写成列表形式
    df_tar["surface"] = surface
    df_tar["TLI"] = TLI
    df_tar["TSI"] = TSI
    '''写入部分'''
    writer = pd.ExcelWriter('s2b_20200216_Res.xlsx')  # 写入Excel文件
    df_tar.to_excel(writer, float_format='%.5f')  # ‘page_1’是写入excel的sheet名 # 不写就是默认第一页
    writer.save()
    writer.close()

