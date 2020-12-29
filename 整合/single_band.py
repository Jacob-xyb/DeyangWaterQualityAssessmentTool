import pandas as pd
from GET import read_xy,read_tiff



def get_data_S():
    '''
    可以检测读取到的图片波段数与参数fac是否对应，不对应则try-except报错
    '''
    print('请输入单波段图像表格路径:')
    path = input()

    ref = pd.read_excel(path, index_col=0)
    path_tiff = ref.iat[4, 2]  # 初始路径
    path1 = ref.iat[5, 2]  # CHLA参数
    path2 = ref.iat[6, 2]  # SD参数
    path3 = ref.iat[7, 2]  # TP参数
    path4 = ref.iat[8, 2]  # TN参数
    path5 = ref.iat[9, 2]  # FAI参数
    path6 = ref.iat[10, 2]  # NDVI参数
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
    path_single="./" + ref.iat[14, 2] + ".xlsx"
    writer = pd.ExcelWriter(path_single)  # 写入Excel文件
    df.to_excel(writer, float_format='%.5f')  # ‘page_1’是写入excel的sheet名 # 不写就是默认第一页
    writer.save()
    writer.close()
    return path_single