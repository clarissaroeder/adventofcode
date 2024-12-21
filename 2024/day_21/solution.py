from pathlib import Path
from collections import deque
import heapq
import itertools

class Keyboard:
    # Mapping direction instructions to movement deltas
    DIRECTIONS = { (0, 1): '>', (0, -1): '<', (1, 0): 'v', (-1, 0): '^'}

    def __init__(self):
        self.keyboard = []

    def get_instructions(self):
        # self.instructions = { key: { every other key: [[sequence 1], [sequence 2], all possible sequences ] }}
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

    def get_neighbours(self, position):
        row, col = position
        offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        return [(row + d_row, col + d_col) for d_row, d_col in offsets]
    
    def manhattan_distance(self, point1, point2):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def backtrack(self, current, path, result, goal, manhattan):
        if current == goal:
            if len(path) - 1 == manhattan:
                result.append(path.copy())
            return
        
        for neighbour in self.get_neighbours(current):
            if neighbour in path or self.out_of_bounds(neighbour) or self.keyboard[neighbour[0]][neighbour[1]] == 'X':
                continue

            remaining_manhattan = self.manhattan_distance(neighbour, goal)
            steps_taken = len(path)
            
            if (steps_taken + remaining_manhattan) > manhattan:
                continue

            path.append(neighbour)
            self.backtrack(neighbour, path, result, goal, manhattan)
            path.pop()

    def convert_paths_to_instructions(self, paths):
        instructions = []       
        for path in paths:
            current_instructions = []        
            for current in range(len(path) - 1):
                row, col = path[current]
                next_row, next_col = path[current + 1]

                d_row = next_row - row
                d_col = next_col - col

                direction = self.DIRECTIONS[(d_row, d_col)]
                current_instructions.append(direction)

            instructions.append(current_instructions)
        return instructions

    def find_shortest_instruction_sequences(self, origin):
        instructions = {}
        for i, row in enumerate(self.keyboard):
            for j, key in enumerate(row):
                # Skip empty space
                if key == 'X': continue
                manhattan = self.manhattan_distance(origin, (i, j))
                result = []
                path = [origin]
                self.backtrack(origin, path, result, (i, j), manhattan)
                instructions[key] = self.convert_paths_to_instructions(result)

        return instructions
    
    def get_instruction(self, origin, goal):
        instruction_sequences = self.instructions[origin][goal]
        return instruction_sequences

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
        print("-------------------------")

        return complexity

    def find_sequence(self, code):
        print("CODE:", code)
        numeric_kb = NumericKeyboad()
        directional_kb = DirectionalKeyboard()

        START = 'A'

        # min_sequence_length = float('inf')
        # best_sequence_1 = []
        current = START
        first_sequences = []
        for key in code:
            instructions = numeric_kb.get_instruction(current, key)
            new_sequences = []
            for instruction in instructions:
                if len(first_sequences) == 0:
                    current_sequence = []
                    current_sequence.extend(instruction)
                    current_sequence.append('A') # push the button
                    new_sequences.append(current_sequence)
                else:
                    for sequence in first_sequences:
                        current_sequence = sequence.copy()
                        current_sequence.extend(instruction)
                        current_sequence.append('A') # push the button
                        new_sequences.append(current_sequence)

            first_sequences = new_sequences
            current = key

        second_sequences = []
        for sequence_1 in first_sequences:
            current = START
            temp_sequences = []
            # print('current first sequence:', sequence_1)
            for key in sequence_1:
                instructions = directional_kb.get_instruction(current, key)
                new_sequences = []
                # print('possible instruction sequences:', instructions)
                for instruction in instructions:
                    if len(temp_sequences) == 0:
                        current_sequence = []
                        current_sequence.extend(instruction)
                        current_sequence.append('A') # push the button
                        new_sequences.append(current_sequence)
                    else:
                        for sequence in temp_sequences:
                            current_sequence = sequence.copy()
                            current_sequence.extend(instruction)
                            current_sequence.append('A') # push the button
                            new_sequences.append(current_sequence)

                temp_sequences = new_sequences
                current = key
            
            second_sequences.extend(temp_sequences)

        # print('second sequences:')
        # for seq in second_sequences:
        #     print(len(seq))
        #     print(seq)
        # input()


        third_sequences = []
        for sequence_2 in second_sequences:
            current = START
            temp_sequences = []
            # print('current second sequence:', sequence_2)
            for key in sequence_2:
                instructions = directional_kb.get_instruction(current, key)
                new_sequences = []
                # print('possible instruction sequences:', instructions)
                for instruction in instructions:
                    if len(temp_sequences) == 0:
                        current_sequence = []
                        current_sequence.extend(instruction)
                        current_sequence.append('A') # push the button
                        new_sequences.append(current_sequence)
                    else:
                        for sequence in temp_sequences:
                            current_sequence = sequence.copy()
                            current_sequence.extend(instruction)
                            current_sequence.append('A') # push the button
                            new_sequences.append(current_sequence)

                temp_sequences = new_sequences
                current = key
            
            third_sequences.extend(temp_sequences)

        shortest = min(third_sequences, key=len)
        print(shortest)
        print(len(shortest))
        return self.calculate_complexity(code, shortest)

        # print('thir sequences:')
        # for seq in third_sequences:
        #     print(seq)
        # input()

        # print("")
        # print('First sequence(instructions for robot 1 to press numeric):', "".join(sequence_1))
        # print("----------")

        # print(directional_kb)
        # current = START
        # sequence_2 = []
        # for key in sequence_1:
        #     instructions = directional_kb.get_instruction(current, key)
        #     sequence_2.extend(instructions)
        #     sequence_2.append('A') # push the button
        #     current = key

        # print("")
        # print('Second sequence(instructions for robot 2 to press dir 1):', "".join(sequence_2))
        # print("----------")

        # current = START
        # sequence_3 = []
        # for key in sequence_2:
        #     instructions = directional_kb.get_instruction(current, key)
        #     sequence_3.extend(instructions)
        #     sequence_3.append('A') # push the button
        #     current = key

        # print("")
        # print('Third sequence(instructions for robot 3 to press dir 3):', "".join(sequence_3))
        # print("----------")

        # return self.calculate_complexity(code, sequence_3)

    def solve(self):
        sum = 0
        for code in self.codes:
            sum += self.find_sequence(code)

        print("Total complexity sum:", sum)

# Numerical keyboard: has robot 1 -> gets instructions from first directional keyboard -> SEQUENCE 1
# First directional keyboard: has robot 2 -> gets instructions from second directional keyboard -> SEQUENCE 2
# Second directional keyboard: has robot 3 -> gets instructions from third directional keyboard -> SEQUENCE 3
# Third directional keyboard: has me -> find buttons I need to press to give instructions to second directional keyboard
