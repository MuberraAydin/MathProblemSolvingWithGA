import numpy as np

#f(x) = 15x-x^2, 0<x<16

#population_dimension = n
n = 6
crossover_probability = 0.001

def chromosome():
    return [np.random.choice([0,1]) for i in range(4)]

def population(n):
    return np.array([ chromosome() for i in range(n)])


def fitness(y):
    fitnesses = np.array([])
    for z in y:
        text = ""
        for st in z:
            text += str(st)
        x = int(text,2)
        print(x)        
        a = 15*x-(x**2)
        fitnesses = np.append(fitnesses, a)
    return (fitnesses)

def calculate_average(pop1):
    calc = 0
    for i in range(len(pop1)):
        calc += fitness(pop1[i])
    return calc/len(pop1)

def probability(pop, fitness1 = fitness, elitist = True):
    """her bireyin fitness degeri hesaplanip, olasilik degerine dondurulur.
    (fitnesslar) [0.2, 0.2, 0.4, 0.4, 0.8] >> (olasiliklar) [0.1, 0.1, 0.2, 0.2, 0.4]
    
    if elitist == True
        [0.2, 0.2, 0.4, 0.4, 0.8] >>[ 0.10225857,  0.10225857,  0.16859588,  0.16859588,  0.45829111]
    """
    fitnesses = np.array([fitness1(pop)])
    if elitist:
        fitnesses = np.exp(fitnesses / fitnesses.mean()) # ortalamadan kucuk degerler iyice kuculur
    fitnesses = fitnesses / fitnesses.sum()
    return fitnesses


def choice1(fitnesses):
    np.seterr(divide='ignore', invalid='ignore')
    """p=olasiliklara gore bireyler secilir. Olasiligi yuksek olan daha fazla secilir."""
    #print("fitnesses", fitnesses)
    fitnesses = np.asarray(fitnesses).astype(int)
    choice = np.random.choice(len(fitnesses), 2, replace = False, p = fitnesses[0])
    #Normalize ediliyor
    fitnesses = fitnesses / fitnesses.sum()
    return choice

def crossing_over(pop, choice):
    """Basarili 2 birey kisi0 ve kisi1 secilip caprazlanir."""
    person0 = pop[choice[0]]
    person1 = pop[choice[1]]
    n = len(pop[choice[0]])//2
    return np.hstack((person0[:n],person1[n:]))

def mutation(person, p):
    """ p olasilikla kisinin bir biti degistirilir."""
    if np.random.rand() < p:
        m = np.random.choice(len(person))
        if(person[m] == 0): 
            person[m] = 1
        else:
            person[m] = 0


def new_population(pop, fitnesses, mutation1 = mutation, p = 0.001):
    """ Toplumun (basarisiz) yarisi emekli edilip,
    basarili bireylerin cocuklari topluma eklenecek.
    """
    k = len(pop)//2
    old = fitnesses.argsort()[:k] # basarisizlar
    #yeniler = np.zeros((k,pop.shape[1]))
    for i in range(k):
        s = choice1(fitnesses)
        new_person = crossing_over(pop, s)
        mutation(new_person, p) 
        #yeniler[i] = yeni_kisi
        pop[old[i]]= new_person
        
    #pop[emekli] = yeniler
    return pop
    
def the_best(pop, fitnesses):
    best = fitnesses.argsort()[-1]
    print("best", best)
    return pop[best]

pop_first = population(6)
fitnesses = fitness(pop_first)

#prt = calculate_average(pop)

print(pop_first)
print(the_best(pop_first, fitnesses))
print(fitnesses)

print("--------------------------------------\n")
#print(calculate_average(pop_first))

for i in range(10):
    pop_first = new_population(pop_first, fitnesses) 
    fitnesses = probability(pop_first)

print(the_best(pop_first, fitnesses))

print("--------------------------------------\n")