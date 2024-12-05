from pathlib import Path
import math
from time import time

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.updates = []
        self.rules = {}
        self.correct_updates = []
        self.incorrect_updates = []
        self.corrected_updates = []
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            data = [line.strip() for line in file]

        split = data.index("")
        for rule in data[:split]:
            x, y = list(map(int, rule.split("|")))
            if self.rules.get(x):
                self.rules[x].append(y)
            else:
                self.rules[x] = [y]

        self.updates = [list(map(int, d.split(","))) for d in data[split + 1:]]

    def categorize_updates(self):
        for update in self.updates:
            valid = True
            for x_index, x in enumerate(update):
                ys = self.rules.get(x, [])

                for y in ys:
                    if y in update[:x_index]:
                        valid = False
                        break
        
            if valid:
                self.correct_updates.append(update)
            else:
                self.incorrect_updates.append(update)

    def sum_middles(self, updates):
        sum = 0
        for update in updates:
            middle_index = math.floor(len(update) / 2)
            sum += update[middle_index]
        
        print("Sum:", sum)

    def order(self, update):
        update = update.copy()
        for x_index, x in enumerate(update):
            ys = self.rules.get(x, [])

            for y in ys:
                if y in update[:x_index]:
                    y_index = update.index(y)
                    update[x_index], update[y_index] = y, x
            
                    return self.order(update)

        return update

    def solve(self):
        self.categorize_updates()
        self.sum_middles(self.correct_updates)

        start_time = time()
        for update in self.incorrect_updates:
            corrected_update = self.order(update)
            self.corrected_updates.append(corrected_update)

        self.sum_middles(self.corrected_updates)
        end_time = time()
        print(f"Execution time: {end_time - start_time:.6f} seconds")
