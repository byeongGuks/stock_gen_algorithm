import env_variable as env

def eval (gen) :
    i=0
    cost = 0
    for i in range(env.GEN_SIZE) :
        field = gen[i]
        if i%2 == 0 :
            cost += field*10
        else :
            cost -= field*10
        i += 1
    return cost
