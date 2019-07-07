"""TSP.py This class can perform the genetic algorithm for the travelling salesman problem including
    mutation, uox, and pmx."""

import time
import sys
import random


class TSP:
    ELITISM = 2  # the top two members of the population are seeded into the next generation
    MODE = {0: "uox", 1: "pmx"}

    def __init__(self, fh, output=None, max_gen=500, pop_size=50, cross_rate=1, mut_rate=0.10, cross_mode=0):

        self.num_nodes = fh.get_num_nodes()
        self.fitness = []
        self.fh = fh
        self.max_gen = max_gen
        self.pop_size = pop_size
        self.mut_rate = mut_rate
        self.cross_rate = cross_rate
        self.cross_mode = cross_mode
        self.population = self.generate_population()

        self.bests = []
        self.averages = []
        self.output = output

    def get_fitness(self, ind):

        sum_of_dist = 0
        for i in range(self.num_nodes):
            if i + 1 < self.num_nodes:
                b = i + 1
            else:
                b = 0

            sum_of_dist = sum_of_dist + self.fh.get_dist(ind[i], ind[b])

        return sum_of_dist

    def generate_individual(self):
        """Returns a new random individual"""
        a = [i for i in range(self.num_nodes)]
        random.shuffle(a)
        return a

    def generate_population(self):
        """Returns a new population of random individuals"""
        return [self.generate_individual() for i in range(self.pop_size)]

    # Performs a tournament selection on the population with binary selection as default
    def tournament_selection(self, k=2):
        """Returns the most fit member of the population from a random subset of k individuals"""

        best = None
        for i in range(k):
            potential = random.randint(0, self.pop_size - 1)

            if best is None:
                best = potential
            elif self.fitness[potential] < self.fitness[best]:
                best = potential
        return self.population[best]

    # Transfers any missing genes from the second parent to the child after uox or pmx
    def crossover_transfer(self, child, parent):
        """Adds any missing genes to a child from its second parent"""

        i, j = 0, 0
        while child.__contains__(-1):

            if child[i] != -1:
                i += 1
            else:

                if not child.__contains__(parent[j]):
                    child[i] = parent[j]
                    i += 1

                j += 1
        return child

    def pmx_crossover_transfer(self, child, parent1, parent2):

        for i in range(self.num_nodes):

            if child[i] == -1 and not child.__contains__(parent1[i]):
                child[i] = parent1[i]

        child = self.crossover_transfer(child, parent2)

    # Performs a uox and generates two children
    def uox_crossover(self, parent1, parent2):
        """Returns two children after a uox"""

        uox = [random.randint(0, 1) for h in range(self.num_nodes)]
        child1 = []
        child2 = []

        for i in range(self.num_nodes):
            if uox[i] == 1:
                child1.append(parent1[i])
                child2.append((parent2[i]))

            else:
                child1.append(-1)
                child2.append(-1)

        child1 = self.crossover_transfer(child1, parent2)
        child2 = self.crossover_transfer(child2, parent1)

        return child1, child2

    def pmx_crossover(self, parent1, parent2):
        """Returns two children after a pmx"""

        cut_point1 = random.randint(0, self.num_nodes - 1)
        cut_point2 = random.randint(cut_point1, self.num_nodes)

        child1, child2 = [-1 for i in range(self.num_nodes)], [-1 for i in range(self.num_nodes)]

        for i in range(cut_point1, cut_point2):
            child1[i] = parent2[i]
            child2[i] = parent1[i]

        self.pmx_crossover_transfer(child1, parent1, parent2)
        self.pmx_crossover_transfer(child2, parent2, parent1)

        return child1, child2

    def mutate(self, child):
        """Mutates a child by by randomly swapping two distinct genes"""

        if random.random() >= 1 - self.mut_rate:
            rand1 = random.randint(0, self.num_nodes - 1)
            while True:
                rand2 = random.randint(0, self.num_nodes - 1)
                if rand1 != rand2: break
            child[rand1], child[rand2] = child[rand2], child[rand1]

    def get_best(self, n):
        """Returns the best member of the population"""
        return [self.population[i] for i in sorted(range(len(self.fitness)), key=lambda j: self.fitness[j])[:n]]

    def evaluate_fitness(self):
        """Evaluates the fitness for the population"""
        self.fitness = [self.get_fitness(self.population[j]) for j in range(self.pop_size)]

    def write_output(self):
        """Writes the bests and averages to a file if one is provided"""

        if self.output is not None:

            best = self.get_best(1)[0]
            _map = self.fh.get_individual_map(best)

            with open(self.output, "w+") as output_file:

                output_file.write("NAME: " + self.fh.get_name() + "\n")
                output_file.write("NUMBER OF GENERATIONS: " + str(self.max_gen) + "\n")
                output_file.write("POPULATION SIZE: " + str(self.pop_size) + "\n")
                output_file.write("CROSSOVER RATE: " + str(self.cross_rate) + "\n")
                output_file.write("MUTATION RATE: " + str(self.mut_rate) + "\n")
                output_file.write("CROSSOVER MODE: " + self.MODE[self.cross_mode] + "\n")

                output_file.write("\n" + "BEST SOLUTION FITNESS: " + str(self.bests[self.max_gen]) +"\n")
                output_file.write("[BEST_SOLUTION]" + "\n")
                for i in range(self.num_nodes):
                    output_file.write(str(_map[i][0]) + " " + str(_map[i][1]) + "\n")

                output_file.write(str(_map[0][0]) + " " + str(_map[0][1]) + "\n")

                output_file.write("\n" + "[BESTS_AND_AVERAGES]" + "\n")
                for i in range(len(self.bests)):
                     output_file.write(str(self.bests[i]) + " " + str(self.averages[i]) + "\n")

    def genetic_algorithm(self):

        print("-----------------------------",
              "\n-----------------------------",
              "\nRunning Travelling Salesman:",
              "\nPopulation Size:", self.pop_size,
              "\nCrossover Rate:", self.cross_rate,
              "\nMutation Rate:", self.mut_rate,
              "\nCrossover Mode:", self.MODE[self.cross_mode])

        #time.sleep(2)

        for i in range(self.max_gen):

            self.evaluate_fitness()

            self.bests.append(min(self.fitness))
            self.averages.append(sum(self.fitness) / len(self.fitness))
            print("----------------------------- Generation", i, "-----------------------------",
                  "\nBest Fitness:", self.bests[i],
                  "\nAverage Fitness:", self.averages[i],
                  "\nWorst Fitness:", max(self.fitness))

            best = self.get_best(self.ELITISM)
            next_pop = []

            while len(next_pop) < self.pop_size - self.ELITISM:

                parent1 = self.tournament_selection()
                parent2 = self.tournament_selection()

                if random.random() >= 1 - self.cross_rate:
                    if self.cross_mode == 0:
                        child1, child2 = self.uox_crossover(parent1, parent2)
                    elif self.cross_mode == 1:
                        child1, child2 = self.pmx_crossover(parent1, parent2)
                else:
                    child1, child2 = parent1, parent2

                self.mutate(child1)
                self.mutate(child2)

                next_pop.extend([child1, child2])

            next_pop.extend(best)
            self.population = next_pop

        self.evaluate_fitness()
        self.bests.append(min(self.fitness))
        self.averages.append(sum(self.fitness) / len(self.fitness))

        print("----------------------------- Generation", self.max_gen, "-----------------------------",
              "\nBest Fitness:", self.bests[self.max_gen],
              "\nAverage Fitness:", self.averages[self.max_gen],
              "\nWorst Fitness:", max(self.fitness))

        self.write_output()


    def test(self):
        i = self.generate_individual()
        print(i)
        map = self.fh.print_tsp_map()
        print(map)

        x = []
        for j in i:
            x.append(map[j])

        for z in range(len(x)):
            print(x[z][0],x[z][1])

