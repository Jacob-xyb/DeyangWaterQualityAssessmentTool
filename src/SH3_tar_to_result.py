

from FAC.GET import *
from FAC.W_R import Write
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
def evaluation2():
    '''读取部分'''
    df = read_band(output_data_path,evaluate2_data_path)
    '''计算部分'''
    surface = surface_rank(df=df, list_tar=["TP"])
    '''整合部分'''
    df_tar = df[["X", "Y"]]  # 多列时要写成列表形式
    df_tar["surface"] = surface

    '''写入部分'''
    Write(df_tar,evaluate2_data_path)


if __name__ == '__main__':
    evaluation2()

