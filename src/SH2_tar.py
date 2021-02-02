import math

from FAC.W_R import Write
from FAC.GET import *
print("请选择监测月份:"
      "1.Aug 2.Sep 3.Oct")
re = input()

if re=='1':

    from configs.SH_Aug_path import *

elif re=='2':
    from configs.SH_Sep_path import *

elif re=='3':
    from configs.SH_Oct_path import *

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
                       }  # 水质指标 # dic
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
                elif str_tar =='COD':
                    list_str_tar[i] = 10 * (0.109 + 2.661 * math.log(data))  # 10(9.436+1.6241lnTP)
                else:
                    print('参数对应不上')
                '''
                elif str_tar == 'TN':
                    list_str_tar[i] = 10*(5.45+1.6941*math.log(data))  # 10(5.45+1.6941lnTN)
                elif str_tar == 'SD':
                    list_str_tar[i] = 10*(5.45+1.6941*math.log(data))  # 10(5.118-1.941lnSD)
                '''
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
                #elif str_tar == 'SD':
                #   list_str_tar[i] = 60-(14.4*math.log(data))  # 60-14.4 "Ln" Secchi disk depth （meters）
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
def evaluation1():
    '''读取部分'''

    df = read_band(output_data_path,evaluate1_data_path)
    '''计算部分'''
    surface = surface_rank(df=df, list_tar=["TP"])
    TLI = TLI_rank(df=df, list_tar=["CHLA", "COD", "TP"])
    TSI = TSI_rank(df=df, list_tar=["CHLA", "TP"])

    '''整合部分'''
    df_tar = df[["X", "Y"]]  # 多列时要写成列表形式
    df_tar["surface"] = surface
    df_tar["TLI"] = TLI
    df_tar["TSI"] = TSI
    df_tar["NDVI"] = df["NDVI"]
    '''写入部分'''

    Write(df_tar,evaluate1_data_path)


if __name__ == '__main__':
    evaluation1()


