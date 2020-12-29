from single_band import *
from multiple_band import *
from analyze import *
from Cal_result_shuzi import *
from Cal_result_wenzi import  *
if __name__ == '__main__':#E://shixi//github_mycellar//DeyangWaterQualityAssessmentTool//整合//input_param.xlsx
    M=get_data_M()
    S=get_data_S()
    analyze(M,S)
    Get_shuzi(S)
    Get_wenzi(S)
