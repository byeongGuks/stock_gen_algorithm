# para : solutions fitness array 
# output : parent candidate array
import random

# k : selection pressure, k>1
# n : num of new generation => need n*2 parents 
# 부모해를 costs 배열의 인덱스 정보로 리턴
# 선택압이 높을 수록 품질 좋은 해가 살아 남음
def roulette_wheel (costs, k, n) : 
    fitness = list()
    minCost = min(costs)
    maxCost = max(costs)
    for c in costs :
        #f = (maxCost-c) + (c-minCost)/(k-1)
        f = c * 5
        fitness.append(f)
    
    fitnessSubSum = list()
    fitnessSubSum.append(fitness[0])
    for i in range(1, len(fitness)) :
        fitnessSubSum.append(fitnessSubSum[i-1]+fitness[i])
    
    parents = list()
    sumFitness = sum(fitness)
    for i in range(n) :
        picks = [0, 0] # 0:dump data
        for j in range(2) :
            pick = random.uniform(0, sumFitness) # 소수 난수
            pickIdx = 0
            for k in range(len(fitnessSubSum)) :
                if pick < fitnessSubSum[k] :
                    pickIdx = k
                    break
            picks[j] = pickIdx
        parents.append(picks)
    return parents
        
