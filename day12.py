from wrapper import Wrapper


class Cave:

    def __init__(self, name: str):
        self.name = name
        self.is_big = name.isupper()
        self.neighbours = set()


class CaveSystem:

    def __init__(self, input):
        self.caves = self.parse_input(input)
        self.possible_paths = []

    def parse_input(self, input):
        """Create a map of the cave system."""
        caves = {}
        for line in input:
            name1, name2 = line.split('-')
            cave1 = caves.get(name1, Cave(name1))
            cave2 = caves.get(name2, Cave(name2))
            if name2 != 'start':  # Makes it impossible to return to the starting cave.
                cave1.neighbours.add(cave2)
            if name1 != 'start':  # Ditto.
                cave2.neighbours.add(cave1)
            caves[name1] = cave1
            caves[name2] = cave2
        return caves

    def traverse_system(self, path=[], small_flag=False):

        def find_possible_neighbours(cave, path, small_flag):
            if not small_flag:
                return [n for n in cave.neighbours]
            else:
                return [n for n in cave.neighbours if not (not n.is_big and n in path)]

        current_cave = path[-1] if path else self.caves['start']
        possible_neighbours = find_possible_neighbours(current_cave, path, small_flag)

        for neighbouring_cave in possible_neighbours:
            if neighbouring_cave.name == 'end':
                self.possible_paths.append(path + [neighbouring_cave])
            else:
                if small_flag:
                    small_flag_new = True
                elif not neighbouring_cave.is_big and neighbouring_cave in path:  # Second visit.
                    small_flag_new = True
                else:
                    small_flag_new = False
                self.traverse_system(path + [neighbouring_cave], small_flag_new)


class Solver(Wrapper):

    def __init__(self, day, example):
        super(Solver, self).__init__(day, example)
        self.input = self.load_input()

    def find_paths(self):
        cave_system = CaveSystem(self.input)
        cave_system.traverse_system()
        print(f'There are {len(cave_system.possible_paths)} possible paths.')


example = False
day12 = Solver('12', example)
day12.find_paths()
