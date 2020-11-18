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


if __name__ == '__main__':
    '''读取部分'''
    path_tar = r'D:\4.company\项目文件\四川\德阳\德阳水质评价\2德阳评价算法\Tar_algorithm_V1.0' +\
                '\s2b_20200216_Tar.xlsx'
    # df = read_band(path=path_band, head=200)
    df = read_band(path=path_tar)
    '''结果换算'''