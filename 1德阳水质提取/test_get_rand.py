from osgeo import gdal
import numpy as np
import pandas as pd
import xlsxwriter
import numpy.ma as ma

np.set_printoptions(threshold=np.inf)  # 使print大量数据不用符号...代替而显示所有

'''读取tiff'''
path = r"D:\4.company\项目文件\四川\德阳\转换后tiff\哨兵_2020_10m_cgcs2000\s2b20200216waterRrs_CHLAz.tif"
dataset = gdal.Open(path)
print(dataset.GetDescription())  # 数据描述
print(dataset.RasterCount)  # 波段数
nXSize = dataset.RasterXSize  # 列数
nYSize = dataset.RasterYSize  # 行数
band = dataset.GetRasterBand(1)  # 获取波段
# ndv = -999
# band.SetNodataValue(ndv)  # 无用
print(nXSize, nYSize)
data = band.ReadAsArray(0, 0, nXSize, nYSize)
dataDF = pd.DataFrame(data)
# print(dataDF)

'''pd_excel写入_一列'''  # 部分可行
workbook = xlsxwriter.Workbook('res'+'.xlsx')  # 创建excel
worksheet = workbook.add_worksheet()  # 创建sheet
# data[np.isnan(data)] = 0  # numpy 替换
z = 0
for i in range(nYSize):
    for j in range(nXSize):
        # 第一种
        worksheet.write(z, 2, str(data[i, j]))  # 无效值为 nan ,但是数字为str形式，后期不能运算
        z += 1
workbook.close()

'''df删除空值行'''
pd.set_option('display.unicode.east_asian_width', True)  # 保证输出时列名对齐
# df = pd.read_excel('res.xlsx', header=None)  # 导入第二列
df = pd.read_excel('res.xlsx', usecols=[2], header=None)  # 导入第二列
# header: 指定作为列名的行，默认值为0。若数据不包含列名，则设置为header=None.
print(df)  # 德阳 210748行
# df1 = df.dropna()  # 删除含有缺失值的行 这是一个新的对象不改变原df # 22632行
# ndv = df[2][1]
# df1 = df.drop(index=df[df[2].isin([ndv])].index[0])
# print(df1)
