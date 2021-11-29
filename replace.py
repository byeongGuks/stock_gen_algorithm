import random
import env_variable as env

def calc_similarity(gen1, gen2) :
    similarity = 0.0
    for i in range(env.GEN_SIZE) :
        fieldRange = env.FIELD_MAX_VALUE[i] - env.FIELD_MIN_VALUE[i]
        similarity += (gen1[i]-gen2[i])**2 / fieldRange
    return similarity
        

def random_pick_similarity(solutions, children) :
    for child in children :
        replaceCandidate = []
        for i in range(10) :
            randomNum = random.randrange(0, len(solutions))
            while randomNum in replaceCandidate :
                randomNum = random.randrange(0, len(solutions))
            replaceCandidate.append(randomNum)
        changeId = 0 # dump
        minSimilarity = 999999999.0
        for candiID in replaceCandidate :
            candi = solutions[candiID]
            similarity = calc_similarity(candi, child)
            if similarity < minSimilarity :
                minSimilarity = similarity
                changeId = candiID
        solutions[changeId] = child


def elitism(solutions, children) :
    solutions = sorted(solutions,key=lambda l:l[13])
    for i in range(len(children)) :
        solutions[i] = children[i]


#solution = []
#for i in range(10) :
#    sol = []
#    for j in range(13) :
#        sol.append(float(i))
#    solution.append(sol)

#children = []
#for i in range(13) :
#    children.append(5.1)

#print(solution)
#print("------------------")
#random_pick_similarity(solution, [children])

#print(solution)
