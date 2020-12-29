
from FAC.GET import *
from FAC.W_R import Write
from configs.Single_path import *
def read_single_band():

    XY = read_xy(path_tiff + path1)

    cdnX, cdnY = XY[0], XY[1]
    CHLA = read_tiff(path_tiff + path1)
    SD = read_tiff(path_tiff + path2)
    TN = read_tiff(path_tiff + path3)
    TP = read_tiff(path_tiff + path4)
    FAI01 = read_tiff(path_tiff + path5)
    NDVI = read_tiff(path_tiff + path6, 1)


    dict = {'X': cdnX, 'Y': cdnY, 'CHLA': CHLA,
            'SD': SD, 'TP': TP, 'TN': TN, 'FAI01': FAI01, 'NDVI': NDVI}
    df = pd.DataFrame(data=dict)
    # df.drop(index=df[df['CHLA'].isin([-999])].index[0], inplace=True)  # 只删除了一行
    # df['CHLA'].isin([-999])  # Name: CHLA, Length: 210748, dtype: bool
    # df1 = df[df['CHLA'].isin([-999])]  # 包含-999的DataFrame
    # df.drop(index=df[df['CHLA'] < 0].index[0], inplace=True)  # 只删除了一行
    # df.drop(index=(df.loc[(df['CHLA'] == -999)].index), inplace=True)  # 可删除多行 # 只允许有一个key
    # 清洗异常值
    for col in df.columns:  # df1.columns : 列名称的list
        # print(col)  # col为一个个列名
        # df.drop(index=(df.loc[(df[col] == -999)].index), inplace=True)
        df.drop(index=(df[df[col].isin([-999])].index), inplace=True)  # 清洗4个指标
        df.drop(index=(df[df[col].isin([-2])].index), inplace=True)  # 清洗NDVI
        # df.reset_index(inplace=True)  # 重置索引，但会保留原索引
        df.reset_index(drop=True, inplace=True)  # 重置索引，不会保留原索引
    # print(df)
    Write(df,output_data_path)
    """写入部分"""





if __name__ == '__main__':
    read_single_band()






