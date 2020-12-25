from READ import *
if __name__ == '__main__':#C:\Users\Administrator\PycharmProjects\input_param.xlsx
    print("请输入表格存放路径")#"E://shixi//github_mycellar//DeyangWaterQualityAssessmentTool//整合//input_param.xlsx"
    path=input()
    getxy_data(path)#获取xy坐标与对应的参数的excel表
    ref = pd.read_excel("E://shixi//github_mycellar//DeyangWaterQualityAssessmentTool//整合//input_param.xlsx", index_col=0)
    '''
    根据要求选择是一步形成结果还是多步分开，每步都展示结果
    '''
    print("showmore??? y/n")
    get=input()
    get_sorc(ref,get=='y')#输入y代表，参数为True，展示两张表
