from FAC.GET import *
from FAC.W_R import Write

print("请选择监测月份:"
      "1.Aug 2.Sep 3.Oct")
re = input()

if re=='1':

    from configs.SH_Aug_path import output_FAI_path, output_multipband
    from configs.Aug_Multiple_path import *

elif re=='2':
    from configs.SH_Sep_path import output_FAI_path, output_multipband
    from configs.Sep_Multiple_path import *

elif re=='3':
    from configs.SH_Oct_path import output_FAI_path, output_multipband
    from configs.Oct_Multiple_path import *

def Cal_FAI():
    read_band(path6, target=output_multipband)  # 读全波段并生成excel 与 SH4文件功能重复


    XY = read_xy(path_tiff + path1)

    cdnX, cdnY = XY[0], XY[1]
    CHLA = read_tiff(path_tiff + path1)
    COD = read_tiff(path_tiff + path2)
    NTU = read_tiff(path_tiff + path3)
    TP = read_tiff(path_tiff + path4)
    TSM = read_tiff(path_tiff + path5)


    '''FAI'''
    # 红光波段 R665 是rand(4)
    # 近红外波段有两个 R842 是rand(8); R865 是rand(9)
    # 短波红外波段有两个 R1610 是rand(11); R2190 是rand(12)
    R665 = read_tiff(path6, num=4, key=True)
    R842 = read_tiff(path6, num=8, key=True)
    R1610 = read_tiff(path6, num=11, key=True)
    R842_ = [R665[i] + (R1610[i] - R665[i]) * (842 - 665) / (2190 - 665)
             for i in range(len(R665))]
    # FAI = R842 - R842_
    FAI = [R842[i] - R842_[i] for i in range(len(R842))]
    # FAI = [1 if i >= 0.02 else 0 for i in FAI]
    dict = {'X': cdnX, 'Y': cdnY, 'CHLA': CHLA,
            'COD': COD, 'NTU': NTU, 'TP': TP, 'TSM': TSM, 'FAI': FAI}
    df = pd.DataFrame(data=dict)

    """清洗异常值"""
    for col in df.columns:  # df1.columns : 列名称的list
        # print(col)  # col为一个个列名
        df.drop(index=(df.loc[(df[col] == -999)].index), inplace=True)
        # df.reset_index(inplace=True)  # 重置索引，但会保留原索引
        df.reset_index(drop=True, inplace=True)  # 重置索引，不会保留原索引

    """写入部分"""
    Write(df,output_FAI_path)



if __name__ == '__main__':
    Cal_FAI()

