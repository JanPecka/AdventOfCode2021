from wrapper import Wrapper

import numpy as np

from queue import PriorityQueue


class Node:

    def __init__(self, distance, index):
        self.distance_from_neighbours = distance  # The distance is the same from all of the nodes' neighbours.
        self.index = index
        self.distance_from_start = np.inf


class Graph:

    def __init__(self, input_arr):
        self.nodes = np.array(
            [[Node(int(x), [i_row, i_col]) for i_col, x in enumerate(row)]
             for i_row, row in enumerate(input_arr)]
        )

    def get_neighbours(self, node: Node):
        r, c = node.index
        indexes = []
        if r < self.nodes.shape[0] - 1:
            indexes.append((r + 1, c))
        if c < self.nodes.shape[1] - 1:
            indexes.append((r, c + 1))
        if r != 0:
            indexes.append((r - 1, c))
        if c != 0:
            indexes.append((r, c - 1))
        return self.nodes[[t[0] for t in indexes], [t[1] for t in indexes]].flatten()

    def get_distances_from_start(self, node_set):
        return [n.distance_from_start for n in node_set]


class PathFinder:

    def __init__(self, graph: Graph, start=None, end=None):
        self.graph = graph
        self.start_index = (0, 0) if start is None else start
        self.end_index = tuple(d - 1 for d in graph.nodes.shape) if end is None else end
        self.nodes_to_visit = set(self.graph.nodes.flatten())
        self.candidates = PriorityQueue()

    def find_shortest_path(self):

        def mark_neighbours(current_node):
            neighbours = self.graph.get_neighbours(current_node)
            for n in neighbours:
                if n not in self.nodes_to_visit:
                    continue
                distance_through_current = (current_node.distance_from_start
                                            + n.distance_from_neighbours)
                if distance_through_current < n.distance_from_start:
                    n.distance_from_start = distance_through_current
                    print(type(distance_through_current))
                    self.candidates.put((distance_through_current, n))
            self.nodes_to_visit.remove(current_node)

        def find_next_node():
            return self.candidates.get()[1]

        def goal_reached():
            return self.graph.nodes[self.end_index] not in self.nodes_to_visit

        current_node = self.graph.nodes[self.start_index]
        current_node.distance_from_start = 0

        while self.nodes_to_visit:
            mark_neighbours(current_node)
            if goal_reached():
                print('Found it!')
                print(f'Shortest path: {self.graph.nodes[self.end_index].distance_from_start}')
                break
            current_node = find_next_node()
            print(f"Visited {1 - len(self.nodes_to_visit) / self.graph.nodes.size:.3%} of all nodes.")


class Solver(Wrapper):

    def __init__(self, day, example):
        super(Solver, self).__init__(day, example)

    def task1(self):
        input = self.load_input_as_array()
        path_finder = PathFinder(Graph(input))
        path_finder.find_shortest_path()

    def task2(self):

        def create_map(input):
            map = np.array(input)
            first_row = np.hstack(map + i for i in range(5))
            map = np.vstack(first_row + i for i in range(5))
            map = np.mod(map, 9)
            map[map == 0] = 9
            return map

        input = self.load_input_as_array()
        duplicated_map = create_map(input)
        path_finder = PathFinder(Graph(duplicated_map))
        path_finder.find_shortest_path()


example = True
day15 = Solver('15', example)
day15.task1()
# day15.task2()
