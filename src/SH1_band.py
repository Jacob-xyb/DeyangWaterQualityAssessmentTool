from FAC.GET import *
from FAC.W_R import Write
print("请选择监测月份:"
      "1.Aug 2.Sep 3.Oct")
re = input()

if re=='1':

    from configs.Aug_Single_path import *

elif re=='2':
    from configs.Sep_Single_path import *

elif re=='3':


    from configs.Oct_Single_path import *


def read_single_band():

    XY = read_xy(path_tiff + path1)

    cdnX, cdnY = XY[0], XY[1]
    CHLA = read_tiff(path_tiff + path1)
    COD = read_tiff(path_tiff + path2)
    NTU= read_tiff(path_tiff + path3)
    TP = read_tiff(path_tiff + path4)
    TSM = read_tiff(path_tiff + path5)
    FAI01 = read_tiff(path_tiff + path6)
    NDVI = read_tiff(path_tiff + path7, 1)


    dict = {'X': cdnX, 'Y': cdnY, 'CHLA': CHLA,
            'COD': COD, 'NTU': NTU, 'TP': TP,'TSM ':TSM,'FAI01': FAI01, 'NDVI': NDVI}
    df = pd.DataFrame(data=dict)
    '''
     for col in df.columns:  # df1.columns : 列名称的list
        df.drop(index=(df[df[col].isin([-999])].index), inplace=True)  # 清洗4个指标
        df.drop(index=(df[df[col].isin([-2])].index), inplace=True)  # 清洗NDVI
        # df.reset_index(inplace=True)  # 重置索引，但会保留原索引
        df.reset_index(drop=True, inplace=True)  # 重置索引，不会保留原索引
    '''


    Write(df,output_data_path)
    """写入部分"""

if __name__ == '__main__':
    read_single_band()






