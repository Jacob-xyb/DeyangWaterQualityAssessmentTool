import pandas as pd
from configs.Path_parameters import output_FAI_path,output_data_path

def analyze():
    '''读取部分'''
    file1 = output_FAI_path  # 自己跑出来要检验结果的文件
    file2 = output_data_path  # 只含1，0的"原文件"
    # df = read_band(path=path_band, head=200)
    df1 = pd.read_excel(file1, index_col=0)
    df2 = pd.read_excel(file2, index_col=0)  # 只含1，0的那个文件
    '''处理部分'''
    df2_selected = df2[df2["FAI01"] == 1]
    count = len(df2_selected)  # df2中1的个数
    df1_selected = df1.nlargest(count, "FAI")  # df1中top个数与df2中1的个数一致
    # inner join：
    df_merge = pd.merge(df1_selected[['X', 'Y']], df2_selected[['X', 'Y']], on=['X', 'Y'], how='inner')  # 坐标匹配的条目
    # df_merge = df1[df1["FAI"] >= 0] # 直接看大于0的条目
    # print(len(df_merge))
    prop = len(df_merge) / 1  # 这里count=0会报错，因为手上没有单波段的FAI图片，所以分母由count换成1让程序不报错
    print(df1_selected["FAI"])
if __name__ == '__main__':
    analyze()

