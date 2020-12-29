from FAC.single_band import *
from FAC.multiple_band import *
from FAC.analyze import *
from FAC.Cal_result_wenzi import *
from FAC.Cal_result_shuzi import *
if __name__ == '__main__':#E://shixi//github_mycellar//DeyangWaterQualityAssessmentTool//data//input_param.xlsx
    M=get_data_M()
    S=get_data_S()
    analyze(M,S)
    Get_shuzi(S)
    Get_wenzi(S)