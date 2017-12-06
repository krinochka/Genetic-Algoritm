import Task_1
import Task_2
import json
import requests


def hundred_runs(items):
    population = Task_2.generate_initial_population(items)
    for generations in range(100):
        pairs = Task_2.roulette(population, items)
        children = Task_2.mutation(Task_2.crossover_population(pairs, items), items)
        population = Task_2.new_population(population, children, items)
    res = sorted([val for val in population], key=lambda x: x[1], reverse=True)
    return res[0]

bestResult = hundred_runs(Task_1.items)

answer = {}
answer["1"] = {}
answer["2"] = {}

host = 'https://cit-home1.herokuapp.com/api/ga_homework'
headers = {'content-Type': 'application/json'}

answer["1"]["value"] = sum(val * Task_1.items[ind][2]
                           for ind, val in enumerate(Task_1.genetic_algorithm.best_individual()[1]))
answer["2"]["value"] = sum(val * Task_1.items[ind][2]
                           for ind, val in enumerate(bestResult))
answer["1"]["weight"] = sum(val * Task_1.items[ind][0]
                            for ind, val in enumerate(Task_1.genetic_algorithm.best_individual()[1]))
answer["2"]["weight"] = sum(val * Task_1.items[ind][0]
                            for ind, val in enumerate(bestResult))
answer["1"]["volume"] = int(sum(val * Task_1.items[ind][1]
                                for ind, val in enumerate(Task_1.genetic_algorithm.best_individual()[1])))
answer["2"]["volume"] = int(sum(val * Task_1.items[ind][1]
                                for ind, val in enumerate(bestResult)))
answer["1"]["items"] = [ind + 1
                        for ind, val in enumerate(Task_1.genetic_algorithm.best_individual()[1])
                        if val != 0]
answer["2"]["items"] = [ind + 1
                        for ind, val in enumerate(bestResult)
                        if val != 0]

print(json.dumps(answer, indent=4))
rec = requests.post(host, data=json.dumps(answer), headers=headers)
print(rec)