from FAC.Cal_result_shuzi import *
from FAC.W_R import Write
def evaluation1():
    '''读取部分'''

    df = read_band(output_data_path)
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
    df_tar["NDVI"] = df["NDVI"]
    '''写入部分'''

    Write(df_tar,evaluate1_data_path)


if __name__ == '__main__':
    evaluation1()


