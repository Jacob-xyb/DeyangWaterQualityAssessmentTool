from FAC.GET import *
from configs.Path_parameters import output_data_path
from configs.Single_path import *
from FAC.W_R import Write
def get_data_S():
    '''
    可以检测读取到的图片波段数与参数fac是否对应，不对应则try-except报错
    '''
    XY = read_xy(path_tiff + path1)
    cdnX, cdnY = XY[0], XY[1]

    CHLA = read_tiff(path_tiff + path1)
    SD = read_tiff(path_tiff + path2)
    TN = read_tiff(path_tiff + path3)
    TP = read_tiff(path_tiff + path4)
    NDVI = read_tiff(path_tiff + path5)
    FAI = read_tiff(path_tiff + path6)
    dict = {'X': cdnX, 'Y': cdnY, 'CHLA': CHLA,
            'SD': SD, 'TP': TP, 'TN': TN,'NDVI':NDVI,'FAI':FAI}
    df = pd.DataFrame(data=dict)
    for col in df.columns:  # df1.columns : 列名称的list
        # print(col)  # col为一个个列名
        # df.drop(index=(df.loc[(df[col] == -999)].index), inplace=True)
        df.drop(index=(df[df[col].isin([-999])].index), inplace=True)  # 清洗4个指标
        df.drop(index=(df[df[col].isin([-2])].index), inplace=True)  # 清洗NDVI
        # df.reset_index(inplace=True)  # 重置索引，但会保留原索引
        df.reset_index(drop=True, inplace=True)  # 重置索引，不会保留原索引
    Write(df,output_data_path)
    return output_data_path