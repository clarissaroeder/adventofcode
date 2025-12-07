from pathlib import Path
from functools import reduce

class Advent:
    def __init__(self, input_file, part):
        self.input_file = Path(__file__).parent / input_file
        self.part = part
        self.data = self._read_input()

    def _read_input(self):
        with open(self.input_file, 'r') as file:
            return [line.strip('\n') for line in file]
        
    def make_calculator(self, operator):
        functions = {
            '+': lambda x, y: x + y,
            '*': lambda x, y: x * y
        }

        return functions[operator]
    
    def math(self):
        data = [line.split() for line in self.data]
        # transpose: first go down the rows of one column, then the next column, etc.
        problems = [[data[i][j] for i in range(len(data))] for j in range(len(data[0]))]

        grand_total = 0
        for problem in problems:
            numbers = list(map(int, problem[:-1]))
            operator = problem[-1]

            calculator = self.make_calculator(operator)
            result = reduce(calculator, numbers)
            grand_total += result

        print('Grand total:', grand_total)

    def cephalopod_math(self):
        data = [list(line) for line in self.data]
        reversed = [[data[i][j] for j in range(len(data[0]) - 1, -1, -1)] for i in range(len(data))]

        grand_total = 0
        calculator = None
        numbers = []
        for j in range(len(reversed[0])):
            number_string = []
            for i in range(len(reversed)):
                cell = reversed[i][j]

                # skip spaces
                if cell == ' ': 
                    continue
                # check for operator: end of operation
                elif cell in ['+', '*']:
                    calculator = self.make_calculator(cell)
                    break
                # else, build the number string
                else:
                    number_string.append(reversed[i][j])

            # if not an empty column, convert the number string to an integer
            if len(number_string) > 0:
                numbers.append(int(''.join(number_string)))

            # if we've reached the end of one block, we have a calculator
            # calculate result and reset
            if calculator:
                grand_total += reduce(calculator, numbers)
                numbers = []
                calculator = None
            

        print('Grand total:', grand_total)

    def homework(self):
        if self.part == 1: 
            return self.math()
        else:
            return self.cephalopod_math()

    def solve(self):
        self.homework()
