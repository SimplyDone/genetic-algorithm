"""GraphHandler.py This class can read .tsp files and build a graph using the corresponding
   data. It also pre-calculates the distance between every vertex to prevent duplicate calculations 
   and to improve efficiency during runtime."""

from math import sqrt


class GraphHandler:
    def __init__(self, tsp_data_file):

        self.name = ""
        self.dist_map = {}
        self.tsp_map = []

        self.read_tsp_file(tsp_data_file)
        self.build_dist_map()

    def read_tsp_file(self, tsp_data_file):
        """This method reads the TSP file"""

        with open(tsp_data_file) as tsp_data:

            line = tsp_data.readline().strip(" \n").split(" ")

            if not line[0] == "NAME:":
                IOError("Invalid file format!")
            else:
                self.name = line[1]
                for line in tsp_data:
                    line = line.strip(" \n").split(" ")
                    if line[0].isdigit():
                        self.tsp_map.append((float(line[1]), float(line[2])))

    def print_tsp_map(self):
        """Returns the TSP map."""
        return self.tsp_map

    def get_individual_map(self, ind):
        return [self.tsp_map[i] for i in ind]

    def get_node(self, i):
        """Returns a node(vertex) of the graph at position i."""
        return self.tsp_map[i]

    def get_num_nodes(self):
        """Returns the number of nodes(vertices)"""
        return len(self.tsp_map)

    def build_dist_map(self):
        """Calculates the distance between every unique pair of nodes"""

        for i in range(self.get_num_nodes()):
            for j in range(i, self.get_num_nodes()):
                node_a = self.tsp_map[i]
                node_b = self.tsp_map[j]

                self.dist_map[str(i) + "_" + str(j)] = sqrt((node_a[0] - node_b[0]) ** 2 + (node_a[1] - node_b[1]) ** 2)

    def get_dist(self, a, b):
        """Returns the distance between two vertices."""

        if b > a:
            return self.dist_map[str(a) + "_" + str(b)]
        else:
            return self.dist_map[str(b) + "_" + str(a)]

    def get_name(self):
        """Returns the "NAME" of the tsp file."""
        return self.name
