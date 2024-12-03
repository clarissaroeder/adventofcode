from pathlib import Path
import re

# Add up all results of the multiplication
class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.data = None
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            self.data = [line.strip() for line in file]

    def sum_multiplications(self):
        memory = []
        for line in self.data:
            matches = re.findall(r'mul\(\d{1,3},\d{1,3}\)', line)
            memory.extend(matches)

        sum = 0
        for instruction in memory:
            match = re.search(r'\((\d{1,3}),(\d{1,3})\)', instruction)
            num1, num2 = match.groups()
            sum += (int(num1) * int(num2))

        print("Sum of multiplications:", sum)

    def sum_with_conditionals(self):
        memory = []
        for line in self.data:
            matches = re.findall(r"mul\(\d{1,3},\d{1,3}\)|(?:do|don't)\(\)", line)
            memory.extend(matches)

        sum = 0
        multiply = True
        for instruction in memory:
            if instruction == "don't()":
                multiply = False
                continue
            elif instruction == "do()":
                multiply = True
                continue

            if multiply:
                match = re.search(r'\((\d{1,3}),(\d{1,3})\)', instruction)
                num1, num2 = match.groups()
                sum += (int(num1) * int(num2))

        print("Sum of multiplications with conditionals:", sum)

    def solve(self):
        self.sum_multiplications()
        self.sum_with_conditionals()