from pathlib import Path
from collections import deque
from itertools import product
class Keyboard:
    def __init__(self, keyboard):
        self.keyboard = keyboard
        self.compute_instructions()
        self.compute_lengths()

    def out_of_bounds(self, position):
        row, col = position
        return row < 0 or col < 0 or row >= len(self.keyboard) or col >= len(self.keyboard[0])

    def get_neighbours(self, position):
        row, col = position
        offsets = [(0, -1, '<'), (0, 1, '>'), (-1, 0, '^'), (1, 0, 'v')]
        return [(row + d_row, col + d_col, d_move) for d_row, d_col, d_move in offsets]
    
    def manhattan_distance(self, point1, point2):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def compute_instructions(self):
        key_positions = {} # { 7: (0,0), ...}
        for i in range(len(self.keyboard)):
            for j in range(len(self.keyboard[i])):
                if self.keyboard[i][j] != 'X': 
                    key_positions[self.keyboard[i][j]] = (i, j)

        self.instructions = {} # { (x, y): ['<vA', 'v<A'], ...}
        # for every key on the pad find instructions to every key on the pad
        for x in key_positions:
            for y in key_positions:
                if x == y: 
                    self.instructions[(x, y)] = ['A'] # from any key to itself: single A to press it
                    continue

                # bfs
                sequences = [] # find all the best sequences
                moves_taken = ""
                manhattan = self.manhattan_distance(key_positions[x], key_positions[y])
                queue = deque([(key_positions[x], moves_taken)])

                while queue:
                    (row, col), moves = queue.popleft()

                    # don't find paths that are longer than manhattan distance to only find direct paths
                    if len(moves) > manhattan:
                        break

                    # goal reached
                    if self.keyboard[row][col] == y:
                        sequences.append(moves + 'A') # current possible sequence: all moves taken, plus the neigbhbour move + press button
                    
                    neighbours = self.get_neighbours((row, col)) # neighbour = (row, col, move to get there)
                    for neighbour in neighbours:
                        n_row, n_col, n_move = neighbour
                        # validity checks: out of bounds and empty key
                        if self.out_of_bounds((n_row, n_col)) or self.keyboard[n_row][n_col] == 'X':
                            continue

                        queue.append(((n_row, n_col), moves + n_move))

                self.instructions[(x, y)] = sequences

    def compute_lengths(self):
        self.lengths = {pair: len(instruction[0]) for pair, instruction in self.instructions.items()}

    def print_instructions(self):
        for (origin, goal), instructions in self.instructions.items():
            print(f'From {origin} to {goal}: {instructions}')

    def __str__(self):
        lines = []
        for row in self.keyboard:
            top = ('+' + '---') * len(row) + '+'
            lines.append(top)
            middle = '|' + '|'.join([f" {key} " for key in row]) + '|'
            lines.append(middle)

        bottom = ('+' + '---') * len(self.keyboard[0]) + '+'
        lines.append(bottom)

        return '\n'.join(lines)

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.read_input()
        self.numeric_kb = Keyboard([['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], ['X', '0', 'A']])
        self.directional_kb = Keyboard([['X', '^', 'A'], ['<', 'v', '>']])
        self.cache = {}

    def read_input(self):
        with open(self.input_file, 'r') as file:
            self.codes = [line.strip() for line in file]

    def calculate_complexity(self, code, length):
        code_num = int(code[:-1])
        complexity = code_num * length
        # print(f"Code: {code} - Min length: {length}\nComplexity: {complexity}")
        # print("--------------------\n")
        return complexity

    # gets all instruction sequences for a given string on the given keyboard
    def get_instructions(self, string, keyboard):
        # get each consecutive pair, starting at 'A'
        pairs = list(zip('A' + string, string))

        # get the instruction options for each pair
        options = [keyboard.instructions[(pair)] for pair in pairs]

        # to get all possible combinations, take cartesian product
        instructions = ["".join(product) for product in product(*options)]
        return instructions
    
    # returns length of shortest instruction sequence between two points at a certain depth
    def compute_length(self, x, y, depth=25):
        key = (x, y, depth)
        if key in self.cache:
            return self.cache.get(key)

        # depth 1 will not need further computation as that is the instructions we
        # need to give to the last robot, and we don't movement instructions ourselves
        if depth == 1:
            min_length = self.directional_kb.lengths[(x, y)]
            self.cache[(x, y, depth)] = min_length
            return min_length

        min_length = float('inf')
        for sequence in self.directional_kb.instructions[(x, y)]:
            pairs = list(zip('A' + sequence, sequence))
            length = 0
            for x, y in pairs:
                result = self.compute_length(x, y, depth - 1)
                length += result

            if length < min_length: 
                min_length = length 

        self.cache[key] = min_length
        return min_length

    def solve(self):
        sum = 0
        for code in self.codes:
            # get the instruction sequences for the numeric keyboard first
            robot1 = self.get_instructions(code, self.numeric_kb)

            ### * Part 1: Iteration
            # current_robot = robot1
            # for i in range(2):
            #     next_robot = []
            #     for sequence in current_robot:
            #         next_robot.extend(self.get_instructions(sequence, self.directional_kb))
                
            #     min_length = min(map(len, next_robot))
            #     current_robot = [seq for seq in next_robot if len(seq) ==  min_length]

            ### * Part 2: Change to recursion
            min_length = float('inf')
            for sequence in robot1:
                pairs = list(zip('A' + sequence, sequence))
                length = 0
                for x, y in pairs:
                    result = self.compute_length(x, y)
                    length += result

                if length < min_length: 
                    min_length = length

            sum += self.calculate_complexity(code, min_length)

        print("Total Complexity:", sum)
