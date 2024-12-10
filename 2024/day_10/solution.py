from pathlib import Path

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.grid = []
        self.visited = set()
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            self.grid = [list(map(int, line.strip())) for line in file]

    def out_of_bounds(self, position):
        row, col = position
        return row < 0 or col < 0 or row >= len(self.grid) or col >= len(self.grid[0])

    def trailhead_score(self, row, col):
        def dfs(row, col, score):
            if self.grid[row][col] == 9:
                # * Part 2: comment these 3 lines out
                # if (row, col) in self.visited: 
                #     return score
                
                # self.visited.add((row, col))
                return score + 1
            
            offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for offset in offsets:
                neighbour_row = offset[0] + row
                neighbour_col = offset[1] + col

                if not self.out_of_bounds((neighbour_row, neighbour_col)):
                    if self.grid[neighbour_row][neighbour_col] == self.grid[row][col] + 1:
                        score = dfs(neighbour_row, neighbour_col, score)

            return score
        
        return dfs(row, col, 0)

    def solve(self):
        # self.print_grid()
        total = 0   
        for i, row in enumerate(self.grid):
            for j, value in enumerate(row):
                if value == 0:
                    total += self.trailhead_score(i, j)
                    self.visited = set()
     
        print("Trailhead score sum:", total)
