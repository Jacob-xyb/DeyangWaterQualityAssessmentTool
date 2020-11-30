# DeyangWaterQualityAssessmentTool 
Deyang water quality assessment tool; Self; Test.

## Contents

* [DeyangWaterQualityAssessmentTool](#DeyangWaterQualityAssessmentTool)
  * [V1.0](#V1.0)

## v1.0

- 没有主函数，分为三个零散的模块
- 以哨兵卫星数据做的测试
- 输出均为.xlsx
### Module
#### 1.deyang_band_v1

> 功能：读取卫片波段值（此代码数据源为已处理好后的单波段tiff）
>
> 输入：地址需要在函数内手动更改
>
> 输出：水质数据 / 以DataFrame形式写到 .xlsx 中

#### 2.deyang_tar_v1

> 功能：对水质数据进行评价 / 地表水指标、综合营养状态指数（TLtiI）、卡尔森营养状态指数（TSI)
>
> 输入：deyang_band_v1.0 输出的 .xlsx / 水质数据
>
> 输出：水质评价结果 / 是以number记录的rank / .xlsx 

#### 3.deyang_tar_to_result_v1

> 功能：在 deyang_tar_v1.0 的基础上直接将rank准换为指标描述
>
> 输入：deyang_band_v1.0 输出的 .xlsx / 水质数据
>
> 输出：水质评价结果 / 是以指标描述记录的rank / .xlsx 
>
#### 4.from_12_get_NDVI_v1

> 功能：直接在卫片获取波段反射率，计算NDVI值
> 
> 输入：12波段的哨兵二号影像资料 -- .tif
> 
> 输出：xy坐标和value，考虑到数据尺寸问题需要将水质一起输入 -- .xlsx

### Manual

#### Import

> main: gdal, numpy, pandas, xlsxwriter, math

#### Notice

1.deyang_band_v1.0.py:

> I. 填入path_tiff: tiff文件文件夹所在路径；path1-6：分别表示CHLA，SD，TN，TP，NDVI，FAI01；
>
> II. read_tiff分别提取tiff文件中的数据存到list中，创建字典dict时与相应名字一一对应，若修改顺序或者添加指标时，需注意添加到字典中
>
> III. 所有路径写入建议在路径前加入r，如r'../../*'

2.deyang_tar_v1.0.py:

> I. 填入由deyang_band_v1.0.py输出的结果excel文件完整路径；
>
> II. df_tar为结果输出前的data frame，若需要添加条目或者改变已有条目顺序，需在整合部分进行修改

#### Functions, Params and Effects

##### read_tiff(path, key=None):
- path : tiff文件所在路径及完整文件名，可加r前缀
- key : 默认为None，当读取NDVI的数据时，需设置key=1
>>return : list包含读入单波段数据

##### read_xy(path):
- path ： 坐标文件路径及完整文件名
>>return : 储存XY坐标的列表

##### read_band(path, head=None):
- path : 储存band的excel文件所在路径及完整文件名，可加r前缀
- head : 可选择输入，表示选取前head数量的数据
>>无return，直接创建excel文件并写入所有波段数据

##### surface_rank(df, list_tar):
- df : 存储单一波段全水质数据的dataframe
- list_tar : 存储了算地表水所需的水质指标，i.e.["TP", "TN"] 

##### TLI_rank(df, list_tar):
- df : 存储单一波段全水质数据的dataframe
- list_tar : 存储了算TLI函数所需的水质指标, i.e.["CHLA", "SD", "TP", "TN"]

##### TSI_rank(df, list_tar):
- df : 存储单一波段全水质数据的dataframe
- list_tar : 存储了算TSI函数所需的水质指标, i.e.["CHLA", "SD", "TP"]

#### Run

> 想要得到水质结果：
>
> deyang_band_v1.0 - deyang_tar_to_result_V1.0
>
> 即可

> 适用范围：CHLA, SD, TP, TN四个指标 
>

### TODO
>- [x]  精简代码，删除测试过程以及多余描述
> 
>- [x] 测试扩展 蓝藻、NDVI 指标
> 

### v1.1
- 在v1.0基础上添加 from_12_get_NDVI（说明写入Module）
- 改变了文档序号



