import numpy as np
import random 
import matplotlib.pyplot as plt 
from sklearn.utils import shuffle


def initPopulation( pop_size,       # Kích thước quần thể
                    num_weights,    # số lượng gen trên mỗi cá thể
    ):
    population = []
    for i in range(pop_size):
        population.append(np.random.randint(0,2,num_weights))
    return np.array(population)


def variation(
        individual1,    # thực thể 1
        individual2,    # thực thể 2
        code            # kiểu lai
    ):
    individual1_new = individual1.copy()
    individual2_new = individual2.copy()
    if code == 'UX':
        RANDOM = np.random.uniform(0,1,individual1.shape[0])
        for i in range(individual1.shape[0]):
            if RANDOM[i]>=0.5:
                individual1_new[i] = individual2[i]
                individual2_new[i] = individual1[i]
    else:
        RANDOM = random.randint(1,individual1.shape[0]-1)
        individual1_new[RANDOM:] = individual2[RANDOM:]
        individual2_new[RANDOM:] = individual1[RANDOM:]
    return individual1_new, individual2_new


def offspring(
            population,     # quần thể
            code            # kiểu lai
            ):
    count = population.shape[0]//2
    Offspring = []
    i = 0
    for _ in range(count):
        individual1 = population[i]
        individual2 = population[i+1]
        individual1,individual2 = variation(individual1,individual2,code)
        Offspring.append(individual1)
        Offspring.append(individual2)
        i+=2
    return np.array(Offspring)



def POPOP(
    population,     # quần thể cha mẹ
    offspring       # tập hợp các cá thể con sau khi lai
    ):
    return shuffle(np.concatenate((population,offspring),axis=0))

def tournamentSelection(
                    POPOP,              # 
                    function,           # Hàm onemax hay trap
                    size_selection = 4  # Số lượng vòng đấu
                    ):
    # pop_size = POPOP.shape[0]//2
    selection = []
    for i in range(size_selection//2):
        start = 0
        end = size_selection
        while end <= POPOP.shape[0]:
            max_item = 0
            key_item = start
            for j in range(start,end):
                if function == 'onemax':
                    result = onemaxFunction(POPOP[j])
                else:
                    result = trapFunction(POPOP[j])
                if result >= max_item:
                    max_item = result
                    key_item = j
                # print(result)   
            selection.append(POPOP[key_item])
            start += size_selection
            end += size_selection
        # shuffle
        POPOP = shuffle(POPOP)
    return np.array(selection)

def targetFunction(target):                    
    return np.ones(target,dtype=int)

def onemaxFunction(individual):         
    result = 0
    for i in individual:
        if i == 1:
            result+=1
    return result

def trapFunction(individual,k=5):
    if individual.shape[0]%k != 0 :
        print("Tham so khong phai la boi cua so luong gen!")
        exit(0)
    else:
        m = individual.shape[0]//k
        result = 0
        for i in range(m):
            u = 0
            for j in range(k):
                if individual[i*k+j] == 1:
                    u+=1
            if u == k:
                result += 5
            else:
                result += (k-1-u)
    return result

def sGA(pop_size, num_weights, code, target, fitness_function, k = 5):
    population = initPopulation(pop_size,num_weights)
    count = 0

    # hàm kiểm tra quần thể đã hội tụ chưa
    def check1(population):
        for i in population[1:]:
            if sum(i == population[0]) < num_weights:
                return False
        return True

    # Hàm kiểm tra quần thể đã có cá thể cần tìm hay chưa
    def check2(target,population):
        for i in population:
            if sum(i == target) == num_weights:
                return True
        return False
    
    while check1(population) == False and check2(targetFunction(target),population) == False:
        count += 1
        _offspring = offspring(population,code)
        _POPOP = POPOP(population,_offspring)
        selection = tournamentSelection(_POPOP,fitness_function,4)
        population = selection
    # print(population)
    if check2(targetFunction(target),population) == True:
        return True, count*2*pop_size
    return False, count*2*pop_size


def upperMRPS(target,num_weights, code,fitness_function,random_seed = 17521056, N= 4, k = 5):
    success = False
    while(success != True):
        N *= 2
        count = 0
        while(count < 10):
            i = 0
            np.random.seed(random_seed + i)
            result,_ = sGA(N,num_weights,code,target,fitness_function, k = k)
            if result == True:
                count += 1
                i += 1
            else:
                break
        if count == 10:
            success = True
        if N > 8192:
            return N
    return N


def lowerMRPS(N,target,num_weights,code ,fitness_function, random_seed = 17521056, k = 5):
    N_upper = N
    N_lower = N_upper//2
    number_of_evaluations = 0
    success = False
    while (N_upper - N_lower)/N_upper > 0.1:
        N = (N_upper + N_lower )//2
        count = 0
        
        while (count < 10):
            i = 0
            np.random.seed(random_seed + i)
            result,temp = sGA(N,num_weights,code,target,fitness_function,k = k)
            number_of_evaluations += temp
            if result == True:
                count += 1
                i += 1
            else:
                success = False
                break
            success = True
        if success:
            N_upper = N
        else:
            N_lower = N
        if N_upper - N_lower <= 2:
            break
    return N_upper, number_of_evaluations/10

def draw(l,results,name1, name2):
    pass

def bisection(target, num_weights, code, fitness_function, random_seed=17521056, N = 4):

    N = upperMRPS(target,num_weights,code,random_seed=random_seed,N = N, fitness_function = fitness_function)
    if N > 8192:
        return 0,0
    N_upper, avg_number_of_evaluations = lowerMRPS(N,target,num_weights,code,random_seed=random_seed,fitness_function = fitness_function)
    return N_upper,avg_number_of_evaluations
    
def writeResults(code,fitness_function):
    f = open('{}_{}_results.txt'.format(code,fitness_function),'w')
    l = 10
    print('Runing for {}\n'.format(code))
    while (l<=160):
        print('l = {}: ... loading...'.format(l))
        random_seed = 17521056
        num_weights = l
        target = num_weights
        N = 4
        f.write("l = ")
        f.write(str(l))
        f.write('\n')
        for i in range(10):
            MRPS, avg_number_of_evaluations = bisection(target=target, num_weights=num_weights, 
                                                            code=code, random_seed=random_seed,N = N,fitness_function = fitness_function)
            string = 'bisection: ' + str(i) + ', MRPS: '+ str(MRPS) + ', avg_number_of_evaluations: ' + str(avg_number_of_evaluations)+'\n'
            if MRPS == 0: return 0
            f.write(string)
            random_seed += 10
            print('MRPS: ',MRPS)
            print("completed bisection ",i+1)
        print('completed l = {}'.format(l))
        l *= 2

if __name__ == "__main__":
    fitness_functions = ['onemax','trap5']
    codes = ['UX','1X']
    for fitness_function in fitness_functions:
        for code in codes:
            writeResults(code,fitness_function)
    
