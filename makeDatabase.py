import csv
import pandas as pd
import OpenDartReader
import time
from pykrx import stock # https://github.com/sharebook-kr/pykrx

api_key = '4d13cb4a55434c1045400dc6e8e6769200ea5dc2'  
dart = OpenDartReader(api_key) 

years = [2021] # 조사할 년도
quarters = [0, 1, 2, 3]
reprtCodes = ['11013', '11012', '11014', '11011'] # 분기별 재무제표 보고서 코드 
quaterStartDays = ['0101', '0401', '0701', '1001']
quarterLastDays = ['0331', '0630', '0930', '1231']
quarterLastMonthStartDays = ['0301', '0601', '0901', '1201']


for year in years :
    for quarter in quarters :
        fw = open(str(year)+str(quarter) + '.csv', 'w', encoding='utf-8', newline='')
        wr = csv.writer(fw)
        print(str(year)+' '+str(quarter))
        reprtCode = reprtCodes[quarter]
        todayStr = str(year)+quarterLastDays[quarter]
        companyList = stock.get_market_ticker_list(todayStr, market="KOSPI") # 해당일자에 코스피 상장된 기업조사
        
        quarterStartDay = str(year) + quaterStartDays[quarter]
        quarterLastDay = str(year) + quarterLastDays[quarter]
        quarterLastMonthStartDay = str(year) + quarterLastMonthStartDays[quarter]
        
        for companyCode in companyList : 
            time.sleep(0.5)
            # 우선주의 경우 배제하기
            if companyCode[5] == '5' or companyCode[5] =='7' or companyCode[5] == '9' or companyCode[5] == 'K' or companyCode[5] == 'L' :
                continue

            # 재무재표 정보
            print(companyCode + ' ' + str(year) + ' ' + reprtCode)
            df = dart.finstate(companyCode, year, reprtCode)
            if (df is None) or (len(df)!=26) : # 재무재표가 없거나 재무재표 필드에 빈 값이 있을 경우
                continue
            
            values = pd.DataFrame(df['thstrm_amount'])
            tdf = values.transpose()
            row =  [str(year)+str(quarter)+companyCode] + tdf.values.tolist()[0]
            
            # 이번 분기 말일 기준 시가 총액 계산
            capInfo = stock.get_market_cap_by_date(quarterStartDay, quarterLastDay, companyCode, 'm') # 구매 시작의 전날 기준으로 구하기
            if capInfo.empty : # 해당 시기에 비상장주식일 경우 
                continue 
            lastIdx = len(capInfo['시가총액'])-1
            marketCap = capInfo['시가총액'][lastIdx]
            
            # 주가 정보
            stockInfo = stock.get_market_ohlcv_by_date(quarterStartDay, quarterLastDay, companyCode) # 영업일만 계산한 수치
            if stockInfo.empty : # 에러처리
                continue
            averageTrading = sum(stockInfo['거래량']) / len(stockInfo['거래량']) 
            averageStartPrice = sum(stockInfo['시가']) / len(stockInfo['시가'])  
            averageClosePrice = sum(stockInfo['종가']) / len(stockInfo['종가'])
            maxPrice = max(stockInfo['고가']) 
            minPrice = min(stockInfo['저가'])
            stockInfoList = [str(marketCap), str(averageTrading), str(averageStartPrice), str(averageClosePrice), str(maxPrice), str(minPrice)]
            row += stockInfoList
            
            # 이차 지표  BPS, PER, PBR, EPS, DIV, DPS
            stockSecondInfo = stock.get_market_fundamental_by_date(quarterLastMonthStartDay, quarterLastDay, companyCode, freq="m")
            if stockSecondInfo.empty :
                continue
            row += stockSecondInfo.iloc[0].to_list()
            
            wr.writerow(row)
        fw.close()
        time.sleep(0.5)
    time.sleep(0.5)

