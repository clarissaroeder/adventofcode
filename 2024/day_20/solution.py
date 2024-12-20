from pathlib import Path
from collections import deque

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.grid = None
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            self.grid = [list(line.strip()) for line in file]

    def print_grid(self):
        for row in self.grid:
            print("".join(row))

    def find(self, target):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == target:
                    return (i, j)

    def wall(self, position):
        row, col = position
        return self.grid[row][col] == "#"
    
    def out_of_bounds(self, position):
        row, col = position
        return row < 0 or col < 0 or row >= len(self.grid) or col >= len(self.grid[0])
    
    def get_neighbours(self, position):
        row, col = position
        offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        return [(row + d_row, col + d_col) for d_row, d_col in offsets]
    
    def bfs(self, start):
        distance = 0
        queue = deque([(start, distance)])
        distances = { start: 0}

        while queue:
            current, distance = queue.popleft()
            
            neighbours = self.get_neighbours(current)
            for neighbour in neighbours:
                if (
                    not self.wall(neighbour) and 
                    not self.out_of_bounds(neighbour) and 
                    neighbour not in distances
                ):
                    queue.append((neighbour, distance + 1))
                    distances[neighbour] = distance + 1

        return distances
    
    def part_1(self, cheat_length=2, min_savings=100):
        track = list(self.distances.keys())

        cheats = 0
        for i in range(len(track)):
            for j in range(len(track)):
                if i == j: continue

                current = track[i]
                cheat = track[j]

                manhattan = abs(current[0] - cheat[0]) + abs(current[1] - cheat[1])
                if manhattan == cheat_length:
                    distance_to_current = self.distances.get(current, -1)
                    distance_to_cheat = self.distances.get(cheat, -1)

                    if distance_to_current == -1 or distance_to_cheat == -1:
                        continue

                    saving = distance_to_cheat - distance_to_current - manhattan
                    if saving >= min_savings:
                        cheats += 1

        print("Total cheats:", cheats)

    def part_2(self, max_cheat_length=20, min_savings=100):
        track = list(self.distances.keys())

        cheats = 0
        for i in range(len(track)):
            for j in range(len(track)):
                if i == j: continue

                current = track[i]
                cheat = track[j]

                manhattan = abs(current[0] - cheat[0]) + abs(current[1] - cheat[1])
                if manhattan <= max_cheat_length:
                    distance_to_current = self.distances.get(current, -1)
                    distance_to_cheat = self.distances.get(cheat, -1)

                    if distance_to_current == -1 or distance_to_cheat == -1:
                        continue

                    saving = distance_to_cheat - distance_to_current - manhattan
                    if saving >= min_savings:
                        cheats += 1

        print("Total cheats:", cheats)

    def solve(self):
        self.start = self.find("S")
        self.end = self.find("E")
        self.distances = self.bfs(self.start)
        self.original_length = self.distances[self.end]

        # self.part_1()
        self.part_2()
