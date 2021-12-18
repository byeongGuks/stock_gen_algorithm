import selection
import calc_profit
import crossover
import random
import numpy
import replace
import env_variable as env
import matplotlib.pyplot as plt
import pandas as pd
from ctypes import cdll
import ctypes
from numpy.ctypeslib import ndpointer

GEN_SIZE = env.GEN_SIZE
SOLUTION_SIZE = env.SOLUTION_SIZE
FIELD_MAX_VALUE = env.FIELD_MAX_VALUE
FIELD_MIN_VALUE = env.FIELD_MIN_VALUE
NUM_SOLUTIONS = env.NUM_SOLUTIONS
NUM_CHILDREN = env.NUM_CHILDREN
NUM_REPEAT = env.NUM_REPEAT
NUM_CHILDREN = env.NUM_CHILDREN
MUTATION_PERCENT = env.MUTATION_PERCENT

# read data
lib = cdll.LoadLibrary('./x64/Debug/Gen_Operation.dll')

lib.init_data()
eval_gen = lib.eval_gen
eval_gen.restype = None
eval_gen.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS")]

calcProfitPercent = lib.calcProfitPercent
calcProfitPercent.restype = ctypes.c_double
calcProfitPercent.argtypes = []

#create solutions
solutions = list()
#solutions = pd.read_csv('best_solutions/v4F_2000,2000,300-2.csv').to_numpy().tolist()
#print(solutions[0][GEN_SIZE])
for i in range(NUM_SOLUTIONS) :
    sol = [ random.uniform(FIELD_MIN_VALUE[i], FIELD_MAX_VALUE[i]) for i in range(GEN_SIZE) ]
    eval_gen(numpy.array(sol, dtype='float'))
    cost = calcProfitPercent()
    sol.append(cost)
    solutions.append(sol)


numRepeat = 0
optimalSolutionAverages = []
while numRepeat < NUM_REPEAT :
    
    #if numRepeat == 1000 :
        #MUTATION_PERCENT -= 0.05
        #(pd.DataFrame(sol)).to_csv('best_solutions/v4_2000,1000,300-2.csv')
    #if numRepeat == 1500 :
        #MUTATION_PERCENT -= 0.05
        #(pd.DataFrame(sol)).to_csv('best_solutions/v4_2000,1500,300-2.csv')
    
    costs = []
    for sol in solutions :
        costs.append(sol[GEN_SIZE])
     # 현재 해집단의 최적 50개 해의 평균 cost를 저장
    sortedCosts = costs
    sortedCosts.sort(reverse=True)
    optimalSolutionAverages.append(sum(sortedCosts[0:50]) / 50)
    print(optimalSolutionAverages[numRepeat])


    parents = selection.roulette_wheel(costs, 4, NUM_CHILDREN)
    children = []
    for plist in parents :
        parent1 = solutions[plist[0]]
        parent2 = solutions[plist[1]]
        child = crossover.multi_point([parent1, parent2])        
        # 변이 연산
        for i in range(GEN_SIZE) :
            if random.random() > MUTATION_PERCENT :
                continue
            
            v = (FIELD_MAX_VALUE[i]-FIELD_MIN_VALUE[i] / 2)
            q= v - numRepeat*0.003*v*0.1  # 표준편차
            u=0 # 평균
            val = q * numpy.random.randn(1)[0] + u
            child[i] += val
            child[i] = max(child[i], FIELD_MIN_VALUE[i])
            child[i] = min(child[i], FIELD_MAX_VALUE[i])
            
        #cost = temp_evaluate.eval(child)
        # evaluate new gen
        eval_gen(numpy.array(child, dtype='float'))
        cost = calcProfitPercent()
        child.append(cost)
        children.append(child)     
    # replace gen
    #replace.elitism(solutions, children)
   
    solutions = sorted(solutions,key=lambda l:l[GEN_SIZE])
    for i in range(len(children)) :
        solutions[i] = children[i]
    numRepeat += 1
    if(numRepeat % 10 == 0) : 
        print(numRepeat)
    
 # 해집단의 최적 50개 해의 평균 cost의 변화를 그래프로 나타내기
#print(optimalSolutionAverages[999])
solutions = sorted(solutions,key=lambda l:l[GEN_SIZE], reverse=True)
best_sols = []
for i in range(1) :
    print(solutions[i])
for i in range(50) :
    best_sols.append(solutions[i])
(pd.DataFrame(best_sols)).to_csv('best_solutions/v4_1000,1000,150N.csv')
(pd.DataFrame(solutions)).to_csv('best_solutions/v4F_1000,1000,150N.csv')

plt.plot(optimalSolutionAverages)
plt.show()