import sys
import argparse


from GraphHandler import *
from TSP import *

FILE1 = "berlin52.tsp"
FILE2 = "dj38.tsp"


def main():
    parser = argparse.ArgumentParser(description="run a genetic algorithm to solve the travelling salesman problem")
    req = parser.add_argument_group("required arguments")
    req.add_argument("-i", "--input_file", help="the input .tsp file", required=True)
    parser.add_argument("-o", "--output_file", help="optional output file for the bests and averages", default=None)
    parser.add_argument("-mx", "--max_gen", help="the maximum number of generations to run for (default=1000)",
                        type=int, default=1000)
    parser.add_argument("-ps", "--pop_size", help="the population size (default=50)", default=50, type=int)
    parser.add_argument("-cr", "--cross_rate", help="the crossover rate (default=1.0)", type=float, default=1.0)
    parser.add_argument("-mr", "--mut_rate", help="the mutation rate (default=0.1)", type=float, default=0.1)
    parser.add_argument("-cm", "--cross_mode", help="the mode of crossover, 0 for uox, 1 for pmx  (default=0)",
                        choices=[0, 1], type=int, default=0)
    args = parser.parse_args()

    try:
        fh = GraphHandler(args.input_file)
    except IOError as err:
        print(err)
        sys.exit(0)

    tsp = TSP(fh, args.output_file, args.max_gen, args.pop_size, args.cross_rate, args.mut_rate, args.cross_mode)
    tsp.genetic_algorithm()


main()

#def experiment():
 #   fh = GraphHandler(FILE2)
  #  settings = [[1000, 50, 0.95, 0.15]]

   # for i in range(4):

    #    for j in ["uox","pmx"]:

     #       for z in range(5):

      #          directory = "test5" + j + "\\run" + str(z+1) + ".txt"

       #         tsp = TSP(fh, directory, settings[i][0], settings[i][1], settings[i][2], settings[i][3], {"uox":0,"pmx":1}[j])
        #        tsp.genetic_algorithm()

#experiment()

