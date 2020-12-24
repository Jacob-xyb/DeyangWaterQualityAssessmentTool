from READ import *
from Getdata import *
if __name__ == '__main__':#C:\Users\Administrator\PycharmProjects\input_param.xlsx
    print("请输入文件路径")
    path=input()
    #C://Users//Administrator//PycharmProjects//input_param.xlsx
    getxy_data(path)#获取xy坐标与对应的参数的excel表
    ref = pd.read_excel("C://Users//Administrator//PycharmProjects//input_param.xlsx", index_col=0)
    '''
    根据要求选择是一步形成结果还是多步分开，每步都展示结果
    '''
    print("showmore??? y/n")
    get=input()
    get_sorc(ref,get=='y')#输入y代表，参数为True，展示两张表
