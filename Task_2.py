import Task_1
import random
from random import randint
from itertools import accumulate

#Пункт 2.1 (Жадный выбор)
def generate_initial_population(items):
    first = []
    sortItem = sorted([(ind, val) for ind, val in enumerate(items)], key=lambda tup: tup[1][2], reverse=True)
    for size in range(200):
        individual = [0 for _ in range(len(items))]
        r = randint(0, len(items) - 1)
        for i in range(0, len(items) - 1):
            modified = individual.copy()
            modified[sortItem[(r + i) % 30][0]] = 1
            if Task_1.fitness_function(modified, items) == 0:
                break
            else:
                individual = modified
        first.append(individual)
    return first

#Пункт 2.2 (Рулетка)
def roulette(population, items):
    count_pairs = int(len(population) / 2)
    parents = []
    sortItem = sorted([[ind, Task_1.fitness_function(val, items), val] for ind, val in enumerate(population)], key=lambda x: x[1], reverse=True)
    for pairs in range(count_pairs):
        pair = []
        for p in range(2):
            wheel = list(accumulate([sortItem[ind][1] for ind in range(len(sortItem))]))
            ball = randint(1, sum(sortItem[ind][1] for ind in range(len(sortItem))))
            for i in range(len(wheel)):
                if ball <= wheel[i] and ball > wheel[i] - sortItem[i][1]:
                    pair.append(sortItem[i][2])
                    del sortItem[i]
                    break
        parents.append(pair)
    return parents

#Пункт 2.3 (Однородный кроссинговер)

# Скрещивание двух особей
def crossover(parents, items):
    children = []
    while len(children) != 2:
        child = [parents[randint(0, 1)][_] for _ in range(len(items))]
        if Task_1.fitness_function(child, items) != 0:
            children.append([parents[randint(0, 1)][_] for _ in range(len(items))])
    return children

# Скрещивание всех пар
def crossover_population(parents, items):
    children = []
    for p in range(len(parents)):
        children.extend(crossover(parents[p], items))
    return children

#Пункт 2.4 (Мутация)
def mutation(population, items):
    # Добавление 1 случайной вещи 10% особей
    count = len(population) / 10
    rand_sequence = random.sample(range(len(population)), len(population))
    for rand in rand_sequence:
        missing_items = [ind for ind, val in enumerate(population[rand]) if val == 0]
        lst = random.sample(range(0, len(missing_items)), len(missing_items))
        for i in lst:
            population[rand][i] = 1
            if (Task_1.fitness_function(population[rand], items), items) == 0:
                population[rand][i] = 0
            else:
                count = count - 1
                break
        if count == 0: break
    return population

#Пункт 2.5 (Новая популяция)
def new_population(parents, children, items):
    sortedParent = sorted([[ind, Task_1.fitness_function(val, items), val] for ind, val in enumerate(parents)], key=lambda x: x[1], reverse=True)
    sortedChild = sorted([[ind, Task_1.fitness_function(val, items), val] for ind, val in enumerate(children)], key=lambda x: x[1], reverse=True)
    #Замена не более 30% худших особей на потомков
    for i in range(int((len(sortedParent) * 30 / 100))):
        if (sortedParent[len(sortedParent) - 1 - i][1]) < sortedChild[i][1]:
            sortedParent[len(sortedParent) - 1 - i] = sortedChild.pop(i)
        else:
            break
    return [sortedParent[_][2] for _ in range(len(sortedParent))]

