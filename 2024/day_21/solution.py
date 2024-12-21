from pathlib import Path
from collections import deque
import heapq

class Keyboard:
    # Mapping direction instructions to movement deltas
    DIRECTIONS = { (0, 1): '>', (0, -1): '<', (1, 0): 'v', (-1, 0): '^'}

    def __init__(self):
        self.keyboard = []

    def get_instructions(self):
        # self.instructions = { key: { every other key: [a shortest sequence of instructions to get there] }}
        self.instructions = {}
        for i, row in enumerate(self.keyboard):
            for j, key in enumerate(row):
                # Skip empty field
                if key == 'X': continue
                inst = self.find_shortest_instruction_sequences((i, j))
                self.instructions[key] = inst

    def out_of_bounds(self, position):
        row, col = position
        return row < 0 or col < 0 or row >= len(self.keyboard) or col >= len(self.keyboard[0])
    
    def reconstruct_path(self, predecessors, goal_state):
        # Reconstruct path
        # print('goal state:', goal_state)
        # print('predecessors:', predecessors)
        path = []
        node, direction = goal_state
        while node:
            path.append(node)
            node, direction = predecessors[(node, direction)]
            # print(node, direction)
            # input()

        path.reverse()
        return path

    def dijkstra(self, start, goal):
        # PQ to always process the node with the least directional changes first
        priority_queue = []
        changes = {} # tracks directional changes for any (position, direction)
        predecessors = {}

        offsets = {"right": (0, 1), "left": (0, -1), "up": (-1, 0), "down": (1, 0)}

        for direction in offsets:
            heapq.heappush(priority_queue, (0, 0, start, direction)) # directional changes, path length, start, current direction
            changes[(start, direction)] = 0
            predecessors[(start, direction)] = (None, direction)

        found_min_path_length = None
        found_min_changes = None 

        while priority_queue:
            current_path_length, current_changes, current_position, current_direction = heapq.heappop(priority_queue)

            if current_position == goal:
                # continue
                goal_state = (current_position, current_direction)
                return self.reconstruct_path(predecessors, goal_state)

            
            row, col = current_position
            for direction, delta in offsets.items():
                d_row, d_col = delta
                neighbour = (row + d_row, col + d_col)
                # if start == (2, 2) and goal == (0, 0):
                #     print('current:', current_position)
                #     print('direction:', direction)
                #     print('neighbour:', neighbour)
                #     input()

                # Skip if out of bounds or empty field
                if (
                    self.out_of_bounds(neighbour) or 
                    self.keyboard[neighbour[0]][neighbour[1]] == 'X'
                ):
                    continue

                # Determine if direction changes
                if direction != current_direction:
                    next_changes = current_changes + 1
                else:
                    next_changes = current_changes

                state = (neighbour, direction)
                if state not in changes or next_changes < changes[state]:
                    changes[state] = next_changes
                    predecessors[state] = (current_position, current_direction)
                    heapq.heappush(priority_queue, (current_path_length + 1, next_changes, neighbour, direction))
                # elif next_changes == changes[state]:
                #     predecessors[state].add((current_position, current_direction))

        # todo: get all best goal states
    

        # return all_best_paths
    
    def convert_path_to_instructions(self, path):
        instructions = []               
        for current in range(len(path) - 1):
            row, col = path[current]
            next_row, next_col = path[current + 1]

            d_row = next_row - row
            d_col = next_col - col

            direction = self.DIRECTIONS[(d_row, d_col)]
            instructions.append(direction)

        return instructions

    def find_shortest_instruction_sequences(self, origin):
        instructions = {}
        for i, row in enumerate(self.keyboard):
            for j, key in enumerate(row):
                # Skip empty space
                if key == 'X': continue
                path = self.dijkstra(origin, (i, j))
                instructions[key] = self.convert_path_to_instructions(path)

        return instructions
    
    def get_instruction(self, origin, goal):
        instruction_sequence = self.instructions[origin][goal]
        return instruction_sequence

    def print_instructions(self):
        for origin, goals in self.instructions.items():
            for goal, instructions in goals.items():
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

class NumericKeyboad(Keyboard):
    def __init__(self):
        super().__init__()
        self.keyboard = [['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], ['X', '0', 'A']]
        self.get_instructions()

class DirectionalKeyboard(Keyboard):
    def __init__(self):
        super().__init__()
        self.keyboard = [['X', '^', 'A'], ['<', 'v', '>']]
        self.get_instructions()


class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            self.codes = [list(line.strip()) for line in file]

    def calculate_complexity(self, code, sequence):
        num_string = ''
        for num in code:
            if num != 'A':
                num_string += num
        
        num = int(num_string)
        complexity = num * len(sequence)
        print("")
        print('num1', num, 'num2:', len(sequence))
        print('Complexity:', complexity)
        print("-------------")

        return complexity

    def find_sequence(self, code):
        print("CODE:", code)
        numeric_kb = NumericKeyboad()
        numeric_kb.instructions['3']['7'] = ["<", "<", "^", "^"]

        directional_kb = DirectionalKeyboard()
        print(numeric_kb)
        numeric_kb.print_instructions()
        # print("")
        # print(directional_kb)
        # directional_kb.print_instructions()
        # input()

        # instruction_sequence = numeric_kb.get_instruction(3, 7)
        # print(f"From {3} to {7}: {instruction_sequence}")
        # input()
        START = 'A'
        current = START

        sequence_1 = []
        for key in code:
            instructions = numeric_kb.get_instruction(current, key)
            sequence_1.extend(instructions)
            sequence_1.append('A') # push the button
            current = key

        print("")
        print('First sequence(instructions for robot 1 to press numeric):', "".join(sequence_1))
        print("----------")

        print(directional_kb)
        current = START
        sequence_2 = []
        for key in sequence_1:
            instructions = directional_kb.get_instruction(current, key)
            sequence_2.extend(instructions)
            sequence_2.append('A') # push the button
            current = key

        print("")
        print('Second sequence(instructions for robot 2 to press dir 1):', "".join(sequence_2))
        print("----------")

        current = START
        sequence_3 = []
        for key in sequence_2:
            instructions = directional_kb.get_instruction(current, key)
            sequence_3.extend(instructions)
            sequence_3.append('A') # push the button
            current = key

        print("")
        print('Third sequence(instructions for robot 3 to press dir 3):', "".join(sequence_3))
        print("----------")

        return self.calculate_complexity(code, sequence_3)

    def solve(self):
        sum = 0
        for code in self.codes:
            sum += self.find_sequence(code)

        print("Total complexity sum:", sum)

# Numerical keyboard: has robot 1 -> gets instructions from first directional keyboard -> SEQUENCE 1
# First directional keyboard: has robot 2 -> gets instructions from second directional keyboard -> SEQUENCE 2
# Second directional keyboard: has robot 3 -> gets instructions from third directional keyboard -> SEQUENCE 3
# Third directional keyboard: has me -> find buttons I need to press to give instructions to second directional keyboard
