from pathlib import Path
from collections import deque

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.size = 70
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            self.bytes = [list(map(int, line.strip().split(","))) for line in file]

        self.grid = [["."] * (self.size + 1) for _ in range(self.size + 1)]

    def corrupt_memory(self, i):
        byte = self.bytes[i]
        col, row = byte
        self.grid[row][col] = "#"

    def print_grid(self):
        for row in self.grid:
            print("".join(row))

    def out_of_bounds(self, position):
        row, col = position
        return row < 0 or col < 0 or row >= len(self.grid) or col >= len(self.grid[0])
    
    def corrupted(self, position):
        row, col = position
        return self.grid[row][col] == "#"

    def get_neighbours(self, position):
        row, col = position
        offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        return [(row + d_row, col + d_col) for d_row, d_col in offsets]
    
    def find_shortest_path(self):
        # bfs
        start = (0, 0)
        goal = (self.size, self.size)

        queue = deque([(start, 0)])
        visited = {start}
        steps = 0

        while queue:
            current, steps = queue.popleft()
            if current == goal: 
                return steps

            neighbours = self.get_neighbours(current)
            for neighbour in neighbours:
                if (
                    not self.out_of_bounds(neighbour) and 
                    not self.corrupted(neighbour) and 
                    neighbour not in visited
                ):
                    queue.append((neighbour, steps + 1))
                    visited.add(neighbour)

        return None
    

    def solve(self):
        ### * Part 1
        for i in range(1024):
            self.corrupt_memory(i)

        # self.print_grid()
        steps = self.find_shortest_path()
        print("Shortest path:", steps)

        ### * Part 2:
        # Could optimise with binary search
        i = 1024
        while True:
            self.corrupt_memory(i)

            if not self.find_shortest_path():
                print("Impossible Byte:", self.bytes[i])
                break

            i += 1
