"""README"""
'''
NIR为近红外波段的反射值；sb2_band(8)
R为红波段的反射值; sb2_band_band(4)
'''
from configs.Path_parameters import output_NDVI_path,output_multipband
from configs.Multiple_path import *
from FAC.GET import *
from FAC.W_R import Write

def Cal_NDVI():

    read_band(path_tiff + path1, target=output_multipband)
    # 读全波段并生成excel
    # exit()

    XY = read_xy(path5)  # 这里因为没有CHLAz的图，所以文件路径由path_tiff+path1换成path5，不然读不出xy坐标
    cdnX, cdnY = XY[0], XY[1]
    CHLA = read_tiff(path_tiff + path1)
    SD = read_tiff(path_tiff + path2)
    TN = read_tiff(path_tiff + path3)
    TP = read_tiff(path_tiff + path4)
    NIR_8 = read_tiff(path5, num=8, key=True)
    # NIR_9 = read_tiff(path5, num=9, key=True)
    R = read_tiff(path5, num=4, key=True)
    NDVI_8 = [0] * len(NIR_8)
    # NDVI_9 = [0] * len(SD)
    for i in range(len(NIR_8)):
        NDVI_8[i] = (NIR_8[i] - R[i]) / (NIR_8[i] + R[i])
        # NDVI_9[i] = (NIR_9[i]-R[i]) / (NIR_9[i]+R[i])
    # print(cdnX[0])
    # 创建DataFrame
    # data = [cdnX, cdnY, CHLA, SD, TN, TP]
    # columns = ['X', 'Y', 'CHLA', 'SD', 'TP', 'TN']
    dict = {'X': cdnX, 'Y': cdnY, 'CHLA': CHLA,
            'SD': SD, 'TP': TP, 'TN': TN, 'NDVI': NDVI_8}
    df = pd.DataFrame(data=dict)
    # df.drop(index=df[df['CHLA'].isin([-999])].index[0], inplace=True)  # 只删除了一行
    # df['CHLA'].isin([-999])  # Name: CHLA, Length: 210748, dtype: bool
    # df1 = df[df['CHLA'].isin([-999])]  # 包含-999的DataFrame
    # df.drop(index=df[df['CHLA'] < 0].index[0], inplace=True)  # 只删除了一行
    # df.drop(index=(df.loc[(df['CHLA'] == -999)].index), inplace=True)  # 可删除多行 # 只允许有一个key

    """清洗异常值"""
    for col in df.columns:  # df1.columns : 列名称的list
        # print(col)  # col为一个个列名
        df.drop(index=(df.loc[(df[col] == -999)].index), inplace=True)
        # df.drop(index=(df[df[col].isin([-999])].index), inplace=True)
        # df.reset_index(inplace=True)  # 重置索引，但会保留原索引
        df.reset_index(drop=True, inplace=True)  # 重置索引，不会保留原索引

    """写入部分"""
    Write(df,output_NDVI_path)

if __name__ == '__main__':
    Cal_NDVI()