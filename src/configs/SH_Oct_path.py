root_path = ".."
data_path = root_path + "/Data"
result_path = root_path + "/result"



input_data_path = data_path + "/SH_Oct_input.xlsx"          # 输入数据,测试中针对于0317，如果要创建其他日期的excel 路径名也对应改一下,可以改成形如`input_0317.xlsx`/`input_0206.xlsx`
output_data_path = result_path + "/SH_1001_waterRrs.xlsx"      # 插补加预测输出结果

evaluate1_data_path=result_path+"/SH_1001_TarR.xlsx"
evaluate2_data_path=result_path+"/SH_1001_Res.xlsx"


output_FAI_path=result_path+"/SH_Oct_FAI_cal.xlsx"
output_NDVI_path=result_path+"/SH_Oct_NDVI_cal.xlsx"
output_multipband=result_path+"/十月12波段.xlsx"
output_final_path=result_path+"/沙湖十月月水质结果.xlsx"