from pathlib import Path
from time import time

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.grid = None
        self.start = None
        self.path = set()
        self.cycles = 0
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            self.grid = [list(line.strip()) for line in file]

    def print_grid(self):
        for row in self.grid:
            print(row)

    def find_start(self):
        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):
                if col == "^":
                    self.start = (i, j)
                    break

    def out_of_bounds(self, position):
        row, col = position
        return row < 0 or col < 0 or row >= len(self.grid) or col >= len(self.grid[0])

    def track_guard(self, obstacle=None):
        turn_right = {"^": ">", ">": "v", "v": "<", "<": "^"}
        offsets = {"^": (-1, 0), ">": (0, 1), "<": (0, -1), "v": (1, 0)}

        visited = set()
        position = self.start
        direction = "^"

        while True:
            state = (position, direction)
            if state in visited:
                self.cycles += 1
                return True
            visited.add(state)

            if obstacle is None:
                self.path.add(position)
        
            offset = offsets[direction]
            next_position = (position[0] + offset[0], position[1] + offset[1])

            if self.out_of_bounds(next_position):
                if obstacle is None:
                    print('Total X:', len(self.path))

                return False

            if next_position == obstacle or self.grid[next_position[0]][next_position[1]] == '#':
                direction = turn_right[direction]
                continue

            position = next_position

    def count_possible_cycles(self):
        for position in self.path:
            i, j = position
            if self.grid[i][j] == "." and (i, j) != self.start:
                self.track_guard(obstacle=(i, j))
        
        print('Cycles:', self.cycles)

    def solve(self):
        self.find_start()
        self.track_guard()
        start_time = time()
        self.count_possible_cycles()
        end_time = time()
        print(f"Execution time: {end_time - start_time:.6f} seconds")


