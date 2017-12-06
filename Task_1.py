# В данном задании мы используем библиотеку pyeasyga, а также готовые методы для реализации задачи о ранце

from  pyeasyga import pyeasyga

#Работа с файлом, извлечение данных
with open('23.txt') as File:
    pack = [(int(l[0]), int(l[1])) for l in [next(File).strip().split(' ')]]
    items = [(int(item[0]), float(item[1]), int(item[2])) for line in File for item in [line.strip().split(' ')]]


genetic_algorithm = pyeasyga.GeneticAlgorithm(items)
genetic_algorithm.population_size = 200

#Реализация фитнесс-фун-ции
def fitness_function(individual, data):
    weight, volume, price = 0, 0, 0
    for (selected, item) in zip(individual, data):
        if selected:
            weight += item[0]
            volume += item[1]
            price += item[2]
    if weight > pack[0][0] or volume > pack[0][1]:
        price = 0
    return price

genetic_algorithm.fitness_function = fitness_function
genetic_algorithm.run()