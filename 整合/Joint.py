from READ import *
if __name__ == '__main__':#C:\Users\Administrator\PycharmProjects\input_param.xlsx
    print("选择图像类型：S（单波段）/M(多波段)")
    re=input()
    if(re=='S' or re=='s'):
        print("请输入单波段表格存放路径")#"E://shixi//github_mycellar//DeyangWaterQualityAssessmentTool//整合//input_param.xlsx"
        path=input()
        getxy_data(path,re)#获取xy坐标与对应的参数的excel表
        ref = pd.read_excel(path, index_col=0)#这个表格中给出的都是单波段图像的路径
        print("showmore??? y/n")
        get=input()
        get_sorc(ref,get=='y')#输入y代表，参数为True，展示两张表
    #单波段三张表，一张参数表，两张测评表
    elif(re=='M' or re=='m'):
        print("请输入多波段表格存放路径")
        path=input()
        getxy_data(path,re)
        ref = pd.read_excel(path, index_col=0)
        print("showmore???y/n")
        get=input()
        get_sorc(ref,get=='y')
    #多波段三张表，一张参数表，两张测评表，其中参数表多两列NDVI 和 FAI
    else:
        print("输入有误")
    #最后一步
    #file1="./" + ref.iat[14, 2] + "NDVI&FAI.xlsx"#单波段没有这个文件就报错
    file2="./" + ref.iat[14, 2] + ".xlsx"
    #df1 = pd.read_excel(file1, index_col=0)
    df2 = pd.read_excel(file2, index_col=0)
    #df2_selected = df2[df2["FAI01"] == 1]
    #count = len(df2_selected)  # df2中1的个数
    #print(count)
    #df1_selected = df1.nlargest(count, "FAI")  # df1中top个数与df2中1的个数一致
    # inner join：
    #df_merge = pd.merge(df1_selected[['X', 'Y']], df2_selected[['X', 'Y']], on=['X', 'Y'], how='inner')  # 坐标匹配的条目
    # df_merge = df1[df1["FAI"] >= 0] # 直接看大于0的条目
    # print(len(df_merge))
    #prop = len(df_merge) / count
    #print(df1_selected["FAI"])
