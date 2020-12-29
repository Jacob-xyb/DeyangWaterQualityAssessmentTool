import pandas as pd
from configs.Path_parameters import input_data_path
ref = pd.read_excel(input_data_path, index_col=0)
path_tiff=ref.iat[4, 2]
path1 = ref.iat[5, 2]
path2 = ref.iat[6, 2]
path3 = ref.iat[7, 2]
path4 = ref.iat[8, 2]
path5 = ref.iat[9, 2]
path6 = ref.iat[10, 2]