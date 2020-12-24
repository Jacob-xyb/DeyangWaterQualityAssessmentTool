from READ import *
def getxy_data(path):
    ref = pd.read_excel(path, index_col=0)
    path_tiff = ref.iat[4, 2]
    path1 = ref.iat[5, 2]
    path2 = ref.iat[6, 2]
    path3 = ref.iat[7, 2]
    path4 = ref.iat[8, 2]
   #path5 = r"D:\1.company\德阳\水质评价模块\转换后tiff\哨兵_2020_10m_cgcs2000\12波段\0317after_12.tif"
   # NIR_8 = read_tiff(path5, num=8, key=True)
   # path5 = ref.iat[9, 2]
   # path6 = ref.iat[10, 2]
    #read_band(path_tiff + path1, target="/12波段.xlsx")
    XY = read_xy(path_tiff + path1)

    cdnX, cdnY = XY[0], XY[1]
    CHLA = read_tiff(path_tiff + path1)
    SD = read_tiff(path_tiff + path2)
    TN = read_tiff(path_tiff + path3)
    TP = read_tiff(path_tiff + path4)
   # NIR_8 = read_tiff(path5, num=8, key=True)
    # NIR_9 = read_tiff(path5, num=9, key=True)
   # R = read_tiff(path5, num=4, key=True)
   # NDVI_8 = [0] * len(NIR_8)
    # NDVI_9 = [0] * len(SD)
   # for i in range(len(NIR_8)):
    #    NDVI_8[i] = (NIR_8[i] - R[i]) / (NIR_8[i] + R[i])
    # FAI01 = read_tiff(path_tiff+path5)
    # NDVI = read_tiff(path_tiff + path6, 1)

    # print(cdnX[0])
    # 创建DataFrame
    # data n= [cdnX, cdnY, CHLA, SD, TN, TP]
    # columns = ['X', 'Y', 'CHLA', 'SD', 'TP', 'TN']
    dict = {'X': cdnX, 'Y': cdnY, 'CHLA': CHLA,
            'SD': SD, 'TP': TP, 'TN': TN}  # , 'FAI01':FAI01, 'NDVI':NDVI}
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

    """写入部分"""
    writer = pd.ExcelWriter("./" + ref.iat[14, 2] + ".xlsx")  # 写入Excel文件
    df.to_excel(writer, float_format='%.5f')  # ‘page_1’是写入excel的sheet名 # 不写就是默认第一页
    writer.save()
    writer.close()
def get_sorc(ref,fac= False):
    if(fac==False):##写两张表
        path_band = ("./" + ref.iat[14, 2] + ".xlsx")
        df = read_band(path=path_band)
        surface = surface_rank2(df=df, list_tar=["TP", "TN"])
        TLI = TLI_rank2(df=df, list_tar=["CHLA", "SD", "TP", "TN"])
        TSI = TSI_rank2(df=df, list_tar=["CHLA", "SD", "TP"])
        df_tar = df[["X", "Y"]]  # 多列时要写成列表形式
        df_tar["surface"] = surface
        df_tar["TLI"] = TLI
        df_tar["TSI"] = TSI
        writer = pd.ExcelWriter("./" + ref.iat[23, 2] + ".xlsx")  # 写入Excel文件
        df_tar.to_excel(writer, float_format='%.5f')  # ‘page_1’是写入excel的sheet名 # 不写就是默认第一页
        writer.save()
        writer.close()
    else:##写三张表
        path_band = ("./" + ref.iat[14, 2] + ".xlsx")
        print(path_band)
        df = read_band(path=path_band)
        surface = surface_rank2(df=df, list_tar=["TP", "TN"])
        TLI = TLI_rank2(df=df, list_tar=["CHLA", "SD", "TP", "TN"])
        TSI = TSI_rank2(df=df, list_tar=["CHLA", "SD", "TP"])
        df_tar = df[["X", "Y"]]  # 多列时要写成列表形式
        df_tar["surface"] = surface
        df_tar["TLI"] = TLI
        df_tar["TSI"] = TSI
        writer = pd.ExcelWriter("./" + ref.iat[23, 2] + ".xlsx")  # 写入Excel文件
        df_tar.to_excel(writer, float_format='%.5f')  # ‘page_1’是写入excel的sheet名 # 不写就是默认第一页
        writer.save()
        writer.close()

        path_band = ("./" + ref.iat[14, 2] + ".xlsx")
        df = read_band(path=path_band)
        surface = surface_rank3(df=df, list_tar=["TP", "TN"])
        TLI3 = TLI_rank3(df=df, list_tar=["CHLA", "SD", "TP", "TN"])
        TSI3 = TSI_rank3(df=df, list_tar=["CHLA", "SD", "TP"])
        df_tar = df[["X", "Y"]]  # 多列时要写成列表形式
        df_tar["surface"] = surface
        df_tar["TLI"] = TLI3
        df_tar["TSI"] = TSI3
        writer = pd.ExcelWriter('s2b_20200216_Res.xlsx')  # 写入Excel文件
        df_tar.to_excel(writer, float_format='%.5f')  # ‘page_1’是写入excel的sheet名 # 不写就是默认第一页
        writer.save()
        writer.close()
