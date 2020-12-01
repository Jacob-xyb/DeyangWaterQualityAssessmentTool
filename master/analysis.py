import pandas as pd       # 导入pandas模块
import math
import xlsxwriter

if __name__ == '__main__':
    '''读取部分'''
    file1 = r'/Users/ethan/Desktop/newfiber/xyb' +\
                '/s2b_20200216_FAI.xlsx'
    file2 = r'/Users/ethan/Desktop/newfiber/xyb' +\
                '/s2b_20200216_waterRrs.xlsx'
    # df = read_band(path=path_band, head=200)
    df1 = pd.read_excel(file1, index_col=0)
    df2 = pd.read_excel(file2, index_col=0) # 只含1，0的那个文件
    '''处理部分'''
    df2_selected = df2[df2["FAI01"] == 1]
    count = len(df2_selected) # df2中1的个数
    df1_selected = df1.nlargest(count,"FAI") # df1中top个数与df2中1的个数一致
    # inner join：
    df_merge = pd.merge(df1_selected[['X','Y']],df2_selected[['X','Y']], on=['X','Y'],how='inner')
    # print(df_merge)
    prop = len(df_merge) / count
    print(prop)

