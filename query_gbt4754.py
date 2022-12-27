# %%
import os
import pandas as pd
import numpy as np

# %%
QUERY_EXCEL = './国民经济行业分类查询表.xlsx'
OUT_EXCEL = './query_result.xlsx'
CLASS_ID_TABLE = dict(  A=[ 1, 5], B=[ 6,12], C=[13,43], D=[44,46], 
                        E=[47,50], F=[51,52], G=[53,60], H=[61,62], 
                        I=[63,65], J=[66,69], K=[70,70], L=[71,72], 
                        M=[73,75], N=[76,79], O=[80,82], P=[83,83], 
                        Q=[84,85], R=[86,90], S=[91,96], T=[97,97])
CLASS_LEVELS = ('门类', '大类', '中类', '小类')

# %%
def get_name_by_class_id(dataframe, class_level, class_id):
    # 需要考虑异常情况
    if (not isinstance(class_id, str)) and np.isnan(class_id):
        return np.nan
    return dataframe[dataframe[class_level]==class_id].iloc[0,4]

def get_class_ids_by_name(dataframe, class_name):
    # x xx x x 门类 大类 中类 小类
    query_rows = dataframe[dataframe['类别名称']==class_name]
    if 0 == len(query_rows):
        return np.nan, np.nan, np.nan, np.nan
        
    id_4 = query_rows.iloc[-1,3]
    # 中类 1位数
    id_3 = id_4//10 if not np.isnan(id_4) else query_rows.iloc[-1,2]
    #大类 1位或2位数
    id_2 = id_3//10 if not np.isnan(id_3) else query_rows.iloc[-1,1]
    # 门类
    id_1 = np.nan
    if np.isnan(id_2):
        id_1 = query_rows.iloc[-1,0]
    else:
        for k, v in CLASS_ID_TABLE.items():
            if id_2 in range(v[0],v[1]+1):
                id_1 = k
                break

    return id_1, id_2, id_3, id_4

def get_all_class_names_by_name(dataframe, class_name):
    class_ids = get_class_ids_by_name(dataframe, class_name)
    # print(class_ids)
    class_names = []
    for i in range(len(class_ids)):
        class_names.append(get_name_by_class_id(dataframe, CLASS_LEVELS[i], class_ids[i]))
    return class_names

def main():
    try:
        dataframes = pd.read_excel(QUERY_EXCEL, sheet_name=None)
    except:
        print('{} 读取失败，请确认是否存在'.format(QUERY_EXCEL))
        return 
    dataframe = dataframes['查询表']

    for i in range(len(dataframe)):
        name = dataframe.iloc[i]['类别名称']
        if not isinstance(name, str):
            continue 
        class_names = get_all_class_names_by_name(dataframes['GBT4574'], name.strip())
        print(class_names)
        for j in range(4):
            dataframe.iloc[i,j+1] = class_names[j]

    dataframe.to_excel(OUT_EXCEL)
    print('执行成功，写入{}'.format(OUT_EXCEL))
    os.system('pause')


# %%
main()
