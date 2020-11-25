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

> 功能：对水质数据进行评价 / 地表水指标、综合营养状态指数（TLI）、卡尔森营养状态指数（TSI)
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



