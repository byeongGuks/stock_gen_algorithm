
from types import BuiltinMethodType

def profit_ratio_simple (log) :
    profitPercentList = []
    for companylog in log :
        buyPrice = 0
        numStock = 0
        sellPrice = 0
        for data in companylog :
            price = data[0]
            val = data[1]
            if(val) :
                buyPrice += price
                numStock += 1
            else :
                sellPrice += price * numStock
                numStock = 0
        if numStock != 0 :
            sellPrice += companylog[len(companylog)-1][0] * numStock
        profitPercent = (sellPrice / buyPrice) * 100
        profitPercentList.append(profitPercent)
    cost = sum(profitPercentList) / len(profitPercentList)
    return cost

def profit_ratio_2d (logs) :
    profitPercentList = []
    buyPrice = 0
    numStock = 0
    sellPrice = 0
    code = logs[0][0]
    for i in range(len(logs)) :
        log = logs[i]
        if code != log[0] :
            code = log[0]
            if(buyPrice==0) :
                profitPercentList.append(0.0)
                continue
            if(sellPrice==0) :
                sellPrice = logs[i-1][1] * numStock
            profitPercent = (sellPrice / buyPrice) * 100
            profitPercentList.append(profitPercent)
            sellPrice=buyPrice=numStock = 0
    cost = sum(profitPercentList) / len(profitPercentList)
    return cost



# test code
logs = [[[10000, 1], [15000, 0]], [[10000, 1], [15000, 0]]]

print(profit_ratio_simple(logs))