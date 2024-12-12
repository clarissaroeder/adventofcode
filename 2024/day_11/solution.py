from pathlib import Path
import math

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.data = None
        self.cache = {}
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            self.data = list(map(int, file.readline().strip().split(" ")))

    def blink(self, stone, count, blinks_left):
        if blinks_left == 0:
            return 1
        
        if self.cache.get(f"{stone}-{blinks_left}", []):
            return self.cache.get(f"{stone}-{blinks_left}")

        if stone == 0:
            count += self.blink(1, count, blinks_left - 1)
        elif len(str(stone)) % 2 == 0:
            num_digits = int(math.log10(stone)) + 1
            half = num_digits // 2
            divisor = 10 ** half
            left = stone // divisor
            right = stone % divisor

            temp_count = count
            count += self.blink(left, temp_count, blinks_left - 1)
            count += self.blink(right, temp_count, blinks_left - 1)
        else: 
            count += self.blink(stone * 2024, count, blinks_left - 1)

        self.cache[(f"{stone}-{blinks_left}")] = count
        return count

    def solve(self):
        sum = 0
        for stone in self.data:
            sum += self.blink(stone, 0, 75)

        print("stones:", sum)
