from pathlib import Path

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.data = None
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            self.data = [line.strip() for line in file]

    def parse_data(self):
        pass

    def solve(self):
        self.parse_data()

