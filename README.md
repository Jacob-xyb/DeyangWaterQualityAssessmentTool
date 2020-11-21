# DeyangWaterQualityAssessmentTool 
Deyang water quality assessment tool; Self; Test.

## Contents

* [DeyangWaterQualityAssessmentTool](#DeyangWaterQualityAssessmentTool)
  * [V1.0](#V1.0)

## V1.0

- 没有主函数，分为三个零散的模块
- 以哨兵卫星数据做的测试
- 输出均为.xlsx
### Module
#### deyang_band_v1.0

> 功能：读取卫片波段值（此代码数据源为已处理好后的单波段tiff）
>
> 输入：地址需要在函数内手动更改
>
> 输出：水质数据 / 以DataFrame形式写到 .xlsx 中

#### deyang_tar_v1.0

> 功能：对水质数据进行评价 / 地表水指标、综合营养状态指数（TLI）、卡尔森营养状态指数（TSI)
>
> 输入：deyang_band_v1.0 输出的 .xlsx / 水质数据
>
> 输出：水质评价结果 / 是以number记录的rank / .xlsx 

#### deyang_tar_to_result_V1.0

> 功能：在 deyang_tar_v1.0 的基础上直接将rank准换为指标描述
>
> 输入：deyang_band_v1.0 输出的 .xlsx / 水质数据
>
> 输出：水质评价结果 / 是以指标描述记录的rank / .xlsx 
>

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

> - [ ]  精简代码，删除测试过程以及多余描述
> - [ ]  测试扩展 蓝藻、NDVI 指标


