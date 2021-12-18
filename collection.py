####################################################################################################################
# 다음분기 데이터가 있는 데이터 분류

import pandas as pd

df = pd.read_csv('data.csv')
df['0'] = df['0'].apply(lambda x:str(x))
code_list = list(df['0'])

def get_next_div_code (x):
    if x[4] == '3':
        y = str(int(x[0:4])+1) + '0' + x[5:]
    else:
        y = x[0:4] + str(int(x[4])+1) + x[5:]
    return y

has_next_list = []
for i in range(len(code_list)):
    next_code = get_next_div_code(code_list[i])

    if next_code in code_list:
        has_next_list.append(True)
    else:
        has_next_list.append(False)

df_has_next = df[has_next_list]
df_has_next['0'] = df_has_next['0'].apply(lambda x : x[5:]+x[:5]) # 소팅을 위해 자리변경
df_has_next = df_has_next.sort_values(by=['0'], axis=0)
df_has_next['0'] = df_has_next['0'].apply(lambda x : x[6:]+x[:6]) # 소팅 후 원위치
df_has_next.set_index('0', inplace=True)
df_has_next.to_csv('data_sorted.csv')

####################################################################################################################
# 데이터 나누기 / 랜덤시드, 랜덤초이스k값 바꾸면 비율 조정가능 / 612개 기업 8984개 자료 -> 테스트 61개기업 896개 자료

import pandas as pd

df = pd.read_csv('data_sorted.csv')
code_list = list(df['0'])
code_list = [x[5:] for x in code_list]
code_dict = dict()

for code in code_list:
    if code in code_dict:
        code_dict[code] += 1
    else:
        code_dict[code] = 1

import random
random.seed(2)
test_data_list = random.choices(list(code_dict.keys()),k=61)
df_test, df_train = pd.DataFrame(), pd.DataFrame()
df.set_index('0', inplace=True)
i = 0
for code, num in code_dict:
    if code in test_data_list:
        df_test = df_test.append(df.iloc[i,:])
    else:
        df_train = df_train.append(df.iloc[i,:])

df_test.to_csv('test_data.csv')
df_train.to_csv('train_data.csv')

####################################################################################################################
# 작업용 주가정보 구하기

import pandas as pd
from pykrx import stock
import time

start_date_list = ['0401', '0701', '1001', '0101']
end_date_list = ['0630', '0930', '1231', '0331']

df = pd.read_csv('test_data.csv')
search_list = list(df['0'])

def info_changer (code):
    switch = int(code[4])
    start_date = str(int(code[0:4]) + int(switch/3)) + start_date_list[switch]
    end_date = str(int(code[0:4]) + int(switch/3)) + end_date_list[switch]
    ticker = code[5:11]
    return start_date, end_date, ticker

final_df = pd.DataFrame()

for code in search_list:
    start_date, end_date, ticker = info_changer(str(code))
    print(start_date, end_date, ticker)
    stock_info = stock.get_market_ohlcv_by_date(start_date, end_date, ticker)
    cap_info = stock.get_market_cap_by_date(start_date, end_date, ticker)
    stock_info['시가총액'] = cap_info['시가총액']
    stock_info['코드'] = [code for i in range(len(stock_info))]
    final_df = pd.concat([final_df, stock_info])
    time.sleep(0.2)

final_df.to_csv('주가정보_완_test.csv')

####################################################################################################################
# 데이터 합쳐서 학습용 데이터 완성하기

import pandas as pd

df = pd.read_csv('test_data.csv')
df2 = pd.read_csv('주가정보_완_test.csv')
final_df = pd.DataFrame()

df['0'] = df['0'].apply(lambda x: int(x))
df2['코드'] = df2['코드'].apply(lambda x : int(x))

df3 = df[['0','1','3','7','8','9','10','11','12','13']] # 원본 데이터에서 재무제표 지표 선택
df3.insert(2, '2', df['1']-df['4'])

code_list = list(df['0'])
code_dict = dict()
for i in list(reversed(code_list)):
    code = str(i)[5:]
    if code in code_dict:
        code_dict[code] += 1
    else:
        code_dict[code] = 1

i = len(df['0'])-1
for code, key in code_dict.items():
    for j in range(key-1):
        df.iloc[i,9] = df.iloc[i,9] - df.iloc[i-1,9]
        df.iloc[i,10] = df.iloc[i,10] - df.iloc[i-1,10]
        df.iloc[i,11] = df.iloc[i,11] - df.iloc[i-1,11]
        i -= 1
    df.iloc[i,9] = 0
    df.iloc[i,10] = 0
    df.iloc[i,11] = 0
    i -= 1

df3['매출액성장률'] = list(df['10'])
df3['영업이익성장률'] = list(df['11'])
df3['법인세차감전순이익성장률'] = list(df['12'])
df3.rename(columns={'0':'code', '1':'유동자산', '2':'유동자산-유동부채', '3':'자산총계', '7':'자본금', '8':'이익잉여금', '9':'자본총계', '10':'매출액', '11':'영업이익','12':'법인세차감전순이익', '13':'당기순이익'}, inplace=True)


def add_cap_info (code):             # 재무제표와 주가정보 합치는 함수
    return_df = pd.DataFrame()
    temp_df = df2[df2['코드']==code]
    for i in range(len(temp_df)):
        return_df = pd.concat([return_df, df3[df3['code']==code]])
    return_df.insert(14, '시가', list(temp_df['시가']))
    return_df.insert(15, '시가총액', list(temp_df['시가총액']))
    return return_df

for code in code_list:              # 주가정보 합치기
    final_df = pd.concat([final_df, add_cap_info(code)])


for i in range(1,14):               # 항목들 시가총액으로 나누기
    final_df.iloc[:,i] = final_df.iloc[:,i] / final_df.iloc[:,15]

final_df.drop('시가총액', axis = 1, inplace=True)
lst = list(final_df['code'])
final_df = final_df.iloc[:,1:]
final_df['code'] = lst
final_df['code'] = final_df['code'].apply(lambda x: "'" + str(x)[5:] + "'")
final_df.set_index('유동자산', inplace=True)
final_df.to_csv('test_for_GA.csv')

####################################################################################################################
# 학습용 데이터 각 항목 최댓값, 최솟값 구하기

import pandas as pd

df = pd.read_csv('data_for_GA.csv')
df.set_index('code', inplace=True)

max_list, min_list = list(), list()

for i in range(0,13):
    max_list.append(max(list(df.iloc[:,i])))
    min_list.append(min(list(df.iloc[:,i])))

column_list = list(df.columns)
maxmin_df = pd.DataFrame([max_list,min_list], columns=column_list[:13])
maxmin_df.to_csv('maxmin_data.csv')
