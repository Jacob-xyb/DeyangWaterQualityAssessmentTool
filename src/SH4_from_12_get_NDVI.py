"""README"""
'''
NIR为近红外波段的反射值；sb2_band(8)
R为红波段的反射值; sb2_band_band(4)
'''

from FAC.GET import *
from FAC.W_R import Write
print("请选择监测月份:"
      "1.Aug 2.Sep 3.Oct")
re = input()

if re=='1':

    from configs.SH_Aug_path import output_NDVI_path,output_multipband
    from configs.Aug_Multiple_path import *

elif re=='2':
    from configs.SH_Sep_path import output_NDVI_path,output_multipband
    from configs.Sep_Multiple_path import *

elif re=='3':
    from configs.SH_Oct_path import output_NDVI_path,output_multipband
    from configs.Oct_Multiple_path import *

def Cal_NDVI():

    #read_band(path6, target=output_multipband)
    # 读全波段并生成excel
    # exit()

    XY = read_xy(path_tiff + path1)

    cdnX, cdnY = XY[0], XY[1]
    CHLA = read_tiff(path_tiff + path1)
    COD = read_tiff(path_tiff + path2)
    NTU = read_tiff(path_tiff + path3)
    TP = read_tiff(path_tiff + path4)
    TSM = read_tiff(path_tiff + path5)
    
    NIR_8 = read_tiff(path6, num=8, key=True)
    R = read_tiff(path6, num=4, key=True)
    NDVI_8 = [0] * len(NIR_8)
    for i in range(len(NIR_8)):
        NDVI_8[i] = (NIR_8[i] - R[i]) / (NIR_8[i] + R[i])
        # NDVI_9[i] = (NIR_9[i]-R[i]) / (NIR_9[i]+R[i])
    dict = {'X': cdnX, 'Y': cdnY, 'CHLA': CHLA,
            'COD': COD, 'NTU': NTU, 'TP': TP, 'TSM': TSM,'NDVI_8':NDVI_8}
    df = pd.DataFrame(data=dict)

    """清洗异常值"""

    for col in df.columns:  # df1.columns : 列名称的list
        df.drop(index=(df[df[col].isin([-999])].index), inplace=True)  # 清洗4个指标

        #df.drop(index=(df[df[col].isin([-2])].index), inplace=True)  # 清洗NDVI
        df.drop(index=(df[df['NDVI_8']<=0].index), inplace=True)  # 清洗NDVI
    # df.reset_index(inplace=True)  # 重置索引，但会保留原索引
        df.reset_index(drop=True, inplace=True)  # 重置索引，不会保留原索引


    """写入部分"""
    Write(df,output_NDVI_path)

if __name__ == '__main__':
    Cal_NDVI()
