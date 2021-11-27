import random
import env_variable as env

# 자름선이 짝수 일 때가 스키마 생존확률이 더 높아짐
NUM_CUTTING_LINE = 2 

# crossover parents[0], parents[1]
def multi_point (parents) :
    # 자름선 정하기
    forPick = [i for i in range(env.GEN_SIZE)]
    cuttingLines = []
    for i in range (NUM_CUTTING_LINE) :
        idx = random.randrange(0, len(forPick))
        cuttingLines.append(forPick[idx])
        del forPick[idx]
    cuttingLines.sort()
    
    child = []
    st = 0
    p = 0
    for ed in cuttingLines :
        child += parents[p][st:ed]
        st = ed
        p = (p+1) % 2
    child += parents[p][ed:(env.GEN_SIZE)]
    return child

# test code
gen1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
gen2 = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

print(multi_point([gen1, gen2]))