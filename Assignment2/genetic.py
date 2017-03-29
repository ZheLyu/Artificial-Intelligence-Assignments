import random
import sys

import numpy as np

from utils import *


def genetic_algorithm(loc, map, repeat_times, population_number):
    def ga(population, matrix, times):
        result = sys.maxsize
        result_order = []
        while times > 0:
            new_pop = []
            for i in range(len(population)):
                father = population[random_selection(population, matrix)[0]]
                mother = population[random_selection(population, matrix)[1]]
                child = crossover(father, mother)
                swap(child)
                length = cal_length(child, matrix)
                if result > length:
                    result = length
                    result_order = child
                new_pop.append(child)
            population = new_pop
            times -= 1
        return result, result_order

    # Generate initial population
    def generate_pop(loc, num):
        loc = list(range(len(loc)))
        result = []
        for i in range(num):
            random.shuffle(loc)
            result.append(list(loc))
        return result

    # Generate random mutation
    def swap(route):
        num = random.sample(range(len(route)), 2)
        temp = route[num[0]]
        route[num[0]] = route[num[1]]
        route[num[1]] = temp

    # crossover
    def crossover(father, mother):
        s = set()
        num = random.sample(range(len(father)), 2)
        num.sort()
        gene = father[num[0]:num[1]]
        child = []
        for i in gene:
            s.add(i)
        i = 0
        for j in mother:
            while num[0] <= i < num[1]:
                child.append(father[i])
                i += 1
            if j not in s:
                child.append(j)
                i += 1
        return child

    # Select as parent based on the fitness
    def random_selection(population, matrix):
        prob = fitness(population, matrix)
        return np.random.choice(range(len(population)), 2, p=prob)

    # Calculate fitness
    def fitness(population, matrix):
        fitness_list = []
        sum_fitness = 0
        result = []
        for i in population:
            fit = 1 / cal_length(i, matrix)
            fitness_list.append(fit)
            sum_fitness += fit
        for i in fitness_list:
            result.append(i / sum_fitness)
        return result

    return ga(generate_pop(loc, population_number), map, repeat_times)