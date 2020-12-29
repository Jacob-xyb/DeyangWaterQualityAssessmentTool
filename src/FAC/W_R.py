import pandas as pd
def Write(df,path):
    writer = pd.ExcelWriter(path)  # 写入Excel文件
    df.to_excel(writer, float_format='%.5f')  # ‘page_1’是写入excel的sheet名 # 不写就是默认第一页
    writer.save()
    writer.close()