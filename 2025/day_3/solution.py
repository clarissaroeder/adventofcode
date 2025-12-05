from pathlib import Path

class Advent:
    def __init__(self, input_file, part):
        self.input_file = Path(__file__).parent / input_file
        self.part = part
        self.banks = self._read_input()

    def _read_input(self):
        with open(self.input_file, 'r') as file:
            return [list(map(int, list(line.strip()))) for line in file]

    def max_joltage(self, bank, battery_num):
        max_joltage = ''
        max, max_index = float('-inf'), -1
        for num in range(battery_num - 1, -1, -1):
            for index in range(max_index + 1, len(bank) - num):
                battery = bank[index]
                if battery > max: 
                    max, max_index = battery, index
            
            max_joltage += str(max)
            max = float('-inf')

        return int(max_joltage)

    def solve(self):
        sum = 0
        for bank in self.banks:
            sum += self.max_joltage(bank, 12)

        print('Max joltage sum:', sum)