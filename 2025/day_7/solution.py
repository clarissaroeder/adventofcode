from pathlib import Path
from collections import deque

SPLITTER = '^'
EMPTY_SPACE = '.'
START = 'S'

class Advent:
    def __init__(self, input_file, part):
        self.input_file = Path(__file__).parent / input_file
        self.part = part
        self.data = self._read_input()

    def _read_input(self):
        with open(self.input_file, 'r') as file:
            return [list(line.strip()) for line in file]
        
    def tachyon(self):
        # * Part 1: Find the split counts
        # Find the start: find 'S' in the first row
        # Define a split count = 0
        # Track the seen splitters
        # Perform a DFS:
            # Pass in the starting position of any beam
            # Find the next start positions:
                # Send the beam downwards until you find the next splitter:
                    # While the row is smaller than len(self.data):
                        # Check if the current position is a splitter, if yes:
                            # Check if the splitter has already been visited
                            # If yes, return
                            # If no, add splitter to visited, and capture the next starting points
                            # Increment the split count
                            # Break
                        # Increment the row

                # For each new starting position:
                    # Perform the dfs
    
        start = (0, self.data[0].index('S'))
        split_count = 0
        seen = set()

        def dfs(position):
            nonlocal split_count
            
            row, col = position
            next_starts = []
            while row < len(self.data):
                if self.data[row][col] == SPLITTER:
                    # check for visited:
                    if (row, col) in seen: return

                    # add to visited:
                    seen.add((row, col))

                    next_starts.append((row, col - 1))
                    next_starts.append((row, col + 1))
                    split_count += 1
                    break

                row += 1
            
            for start in next_starts:
                dfs(start)


        dfs(start)
        print('Split count:', split_count)

    def quantum_tachyon(self):
        # * Part 2: Find all the possible paths (dynamic programming)
        # A timeline ends when it exits the grid
        # The last start position has 1 timeline
        # The previous start position has a total timeline count of all the start
        # positions that come below it: the problem can be split into identical subproblems

        # Perform the dfs like before, but because a splitter can be hit from 
        # multiple timelines, don't track the seen splitters anymore
        # To avoid processing the same start positions multiple times, keep a cache that
        # tracks how many possible timelines each start position has
        start = (0, self.data[0].index('S'))
        memo = {}

        def dfs(position):
            # check if the current start position is cached
            if position in memo:
                return memo[position]
            
            row, col = position
            while row < len(self.data):
                if self.data[row][col] == SPLITTER:
                    count = dfs((row, col - 1)) + dfs((row, col + 1))
                    memo[position] = count
                    return count

                row += 1

            # base case: end of grid = one timeline complete
            return 1

        timeline_count = dfs(start)
        print('Timeline count:', timeline_count)

    def solve(self):
        self.tachyon()
        self.quantum_tachyon()

