from pathlib import Path
import re
# from math import gcd

class ClawMachine:
    def __init__(self, Ax, Ay, Bx, By, prizeX, prizeY):
        self.Ax = Ax
        self.Ay = Ay
        self.Bx = Bx
        self.By = By
        self.prizeX = prizeX
        self.prizeY = prizeY

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.machines = []
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            data = file.read()

        blocks = [block.split("\n") for block in data.strip().split("\n\n")]

        button_pattern = r"X\+(\d+), Y\+(\d+)"
        prize_pattern = r"X=(\d+), Y=(\d+)"
       
        for block in blocks:
            Ax, Ay = self.parse_coordinates(block[0], button_pattern)
            Bx, By = self.parse_coordinates(block[1], button_pattern)
            prizeX, prizeY = self.parse_coordinates(block[2], prize_pattern)

            # * Part 2
            prizeX, prizeY = (prizeX + 10000000000000, prizeY + 10000000000000)#

            self.machines.append(ClawMachine(Ax, Ay, Bx, By, prizeX, prizeY))

    def parse_coordinates(self, line, pattern):
        match = re.search(pattern, line)
        if match:
            return int(match.group(1)), int(match.group(2))

    def calculate_tokens(self, machine):
        # Slope of the line for Button A presses (from origin)
        m1 = machine.Ay / machine.Ax

        # Slope and intercept of the line for reverse Button B presses (from the prize)
        cx, cy = machine.prizeX - machine.Bx, machine.prizeY - machine.By
        m2 = machine.By / machine.Bx
        b2 = cy - m2 * cx 

        # Check for parallel lines (no intersection)
        if m1 == m2:
            return 0

        # Calculate intersection point
        x = round(b2 / (m1 - m2))
        y = round(m1 * x)
        # print(f"Intersection: ({x}, {y})")

        # Verify intersection is cleanly divisible by A
        if x % machine.Ax != 0 or y % machine.Ay != 0:
            return 0

        # Calculate button A presses
        n_A = int(x / machine.Ax)

        # Check remaining distance to the prize
        remaining_x = machine.prizeX - x
        remaining_y = machine.prizeY - y

        # Verify remaining distance is cleanly divisible by B
        if remaining_x % machine.Bx != 0 or remaining_y % machine.By != 0:
            return 0

        # Calculate button B presses
        n_B = int(remaining_x / machine.Bx)

        # Calculate total tokens
        tokens = n_A * 3 + n_B * 1
        return tokens

    def solve(self):
        total = 0
        for machine in self.machines:
            total += self.calculate_tokens(machine)

        print('Total tokens spent:', total)


# Calculate slope of A from origin
# Calculate slope of prize - B 
# The intersection is where you start to press B
# Verify that intersection is divisible by A coords
# Verify that the distance from intersection to prize is divisble by B coords