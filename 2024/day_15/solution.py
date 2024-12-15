from pathlib import Path
import os

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.grid = []
        self.moves = []
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            grid_data, moves_data = file.read().strip().split("\n\n")
        
        self.grid = [list(line) for line in grid_data.splitlines()]
        self.moves = list(moves_data.replace("\n", ""))

    def print_grid(self, grid):
        for row in grid:
            print("".join(row))
        print("")

    def expand_grid(self):
        expanded_grid = []
        for row in self.grid:
            expanded_row = []
            for cell in row:
                if cell == "." or cell == "#":
                    expanded_row.extend([cell, cell])
                elif cell == "@":
                    expanded_row.extend([cell, "."])
                elif cell == "O":
                    expanded_row.extend(["[", "]"])
        
            expanded_grid.append(expanded_row)

        self.grid = expanded_grid

    def find_start(self):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == '@':
                    return (i, j)

    def free(self, row, col):
        return self.grid[row][col] == "."
    
    def wall(self, row, col):
        return self.grid[row][col] == "#"
    
    def box(self, row, col):
        return self.grid[row][col] == "O"
    
    def box_half(self, row, col):
        return self.grid[row][col] == "[" or self.grid[row][col] == "]"
                  
    def calculate_gps_sum(self, symbol):
        total = sum((100 * i + j) for i, row in enumerate(self.grid) 
                    for j, cell in enumerate(row) if cell == symbol)
        
        print("Total GPS Sum:", total)

    def push_single_box(self, current_row, current_col, target_row, target_col, delta_row, delta_col):
        # Find first non-box cell (in case of multiple boxes after one another)
        next_row, next_col = target_row, target_col
        while self.box(next_row, next_col):
            next_row, next_col = next_row + delta_row, next_col + delta_col

        # If the cell after the last box is free, mark it as a box
        # Move robot to target, free up old robot position
        if self.free(next_row, next_col):
            self.grid[next_row][next_col] = "O"
            self.grid[target_row][target_col] = "@"
            self.grid[current_row][current_col] = "."
            return (target_row, target_col)
        
        # If the cell  after the last box is wall, return current position
        if self.wall(next_row, next_col):
            return (current_row, current_col)
        
    def push_horizontal_double(self, current_row, current_col, target_row, target_col, delta_row, delta_col):
        # Find first non-box cell (in case of multiple boxes after one another)
        next_row, next_col = target_row, target_col
        while self.box_half(next_row, next_col):
            next_row, next_col = next_row + delta_row, next_col + delta_col

        # If cell is free, remove it and insert it where the robot was
        if self.free(next_row, next_col):
            self.grid[next_row].pop(next_col)
            self.grid[next_row].insert(current_col, ".")

            return (target_row, target_col)
        
        if self.wall(next_row, next_col):
            return (current_row, current_col)
        
    def push_vertical_double(self, current_row, current_col, target_row, target_col, delta_row, delta_col, move):
        # before making any move, need to check all the boxes that are touched along the way if they can move
        queue = [(target_row, target_col)]
        if self.grid[target_row][target_col] == "[":
            queue.append((target_row, target_col + 1))
        elif self.grid[target_row][target_col] == "]":
            queue.append((target_row, target_col - 1))

        visited = set()

        while queue:
            current_target_row, current_target_col = queue.pop(0)

            if ((current_target_row, current_target_col)) in visited:
                continue

            visited.add((current_target_row, current_target_col))
            next_row, next_col = current_target_row + delta_row, current_target_col + delta_col

            # If any of the next rows are a wall, return current position
            if self.wall(next_row, next_col):
                return (current_row, current_col)

            if self.box_half(next_row, next_col):
                queue.append((next_row, next_col))

                if self.grid[next_row][next_col] == "[":
                    queue.append((next_row, next_col + 1))
                elif self.grid[next_row][next_col] == "]":
                    queue.append((next_row, next_col - 1))

                continue

        visited = sorted(visited)
        if move == "v":
            visited.reverse()

        for row, col in visited:
            next_row, next_col = row + delta_row, col + delta_col
            self.grid[next_row][next_col] = self.grid[row][col]
            self.grid[row][col] = "."

        self.grid[target_row][target_col] = "@"
        self.grid[current_row][current_col] = "."

        return (target_row, target_col)
        
    def push_double_box(self, current_row, current_col, target_row, target_col, delta_row, delta_col, move):
        if move in { ">", "<" }:
            return self.push_horizontal_double(current_row, current_col, target_row, target_col, delta_row, delta_col)
        else:
            return self.push_vertical_double(current_row, current_col, target_row, target_col, delta_row, delta_col, move)

    def attempt(self, position, move):
        offsets = { ">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}
        current_row, current_col = position
        delta_row, delta_col = offsets[move]
        target_row, target_col = current_row + delta_row, current_col + delta_col

        # If target is free, move robot and free up old position
        if self.free(target_row, target_col):
            self.grid[current_row][current_col] = "."
            self.grid[target_row][target_col] = "@"
            return (target_row, target_col)
        
        # If target is wall, return current position
        if self.wall(target_row, target_col):
            return position
        
        if self.box(target_row, target_col):
            return self.push_single_box(current_row, current_col, target_row, target_col, delta_row, delta_col)

        if self.box_half(target_row, target_col):
            return self.push_double_box(current_row, current_col, target_row, target_col, delta_row, delta_col, move)

    def move_robot(self, symbol="O"):
        start = self.find_start()
        current = start
        for move in self.moves:
            current = self.attempt(current, move)

        self.calculate_gps_sum(symbol)

    def solve(self):
        self.move_robot()
        self.read_input()
        self.expand_grid()
        self.move_robot("[")

