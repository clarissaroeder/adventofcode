from pathlib import Path

class Node:
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.antinode = False

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.grid = []
        self.signals = {}
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            data = [list(line.strip()) for line in file]

        for i, row in enumerate(data):
            node_row = []
            for j, value in enumerate(row):
                node = Node(value, i, j)
                node_row.append(node)

            self.grid.append(node_row)

    def print_grid(self):
        for row in self.grid:
            for node in row:
                if node.value != ".":
                    print(node.value, end="")
                elif node.antinode:
                    print("#", end="")
                else:
                    print(node.value, end="")
            print("\n")

    def out_of_bounds(self, row, col):
        return row < 0 or col < 0 or row >= len(self.grid) or col >= len(self.grid[0])
    
    def find_antinodes(self, signal, resonant = False):
        antennae = self.signals[signal]
        for i in range(len(antennae) - 1):
            for j in range(i + 1, len(antennae)):
                node1 = self.signals[signal][i]
                node2 = self.signals[signal][j]

                if resonant:
                    node1.antinode = True
                    node2.antinode = True

                delta_row = node2.row - node1.row
                delta_col = node2.col - node1.col

                before_row = node1.row - delta_row
                before_col = node1.col - delta_col

                after_row = node2.row + delta_row
                after_col = node2.col + delta_col

                if resonant:
                    current_row, current_col = before_row, before_col
                    while not self.out_of_bounds(current_row, current_col):
                        self.grid[current_row][current_col].antinode = True
                        current_row = current_row - delta_row
                        current_col = current_col - delta_col

                    current_row, current_col = after_row, after_col
                    while not self.out_of_bounds(current_row, current_col):
                        self.grid[current_row][current_col].antinode = True
                        current_row = current_row + delta_row
                        current_col = current_col + delta_col
                else:
                    if not self.out_of_bounds(before_row, before_col):
                        self.grid[before_row][before_col].antinode = True

                    if not self.out_of_bounds(after_row, after_col):
                        self.grid[after_row][after_col].antinode = True


    def solve(self):
        for row in self.grid:
            for node in row:
                if node.value != ".":
                    if self.signals.get(node.value, []):
                        self.signals[node.value].append(node)
                    else:
                        self.signals[node.value] = [node]

        for signal in self.signals:
            self.find_antinodes(signal)

        total = sum(1 for row in self.grid for node in row if node.antinode)
        print("Total antennae:", total)
        
        for signal in self.signals:
            self.find_antinodes(signal, resonant=True)

        total = sum(1 for row in self.grid for node in row if node.antinode)
        print("Total resonant antennae:", total)


# any two of the same will form a line
# the antinodes are placed on either side with the same distance between them
# antinodes can be placed where antennas are

# find all possible values 
# for each value, find each pair
    # part 2:
    # while inbounds, go the distance in either direction and place an antinode
    # antennas themselves are antinodes

# calculate the i, j distance and go in either direction
# if not out ouf bounds, mark that node as antenna