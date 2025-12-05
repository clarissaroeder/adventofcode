from pathlib import Path
from collections import deque

class Advent:
    def __init__(self, input_file, part):
        self.input_file = Path(__file__).parent / input_file
        self.part = part
        self.data = self._read_input()

    def _read_input(self):
        with open(self.input_file, 'r') as file:
            return [list(line.strip()) for line in file]
        
    def get_neighbours(self, row, col):
        offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return [(row + d_row, col + d_col) for d_row, d_col in offsets]
    
    def inbounds(self, row, col):
        return 0 <= row < len(self.data) and 0 <= col < len(self.data[0])

    def forklift(self):
        visited = set()
        queue = deque([(0, 0)])
        visited.add((0, 0))
        accessible_rolls = []

        while queue:
            row, col = queue.popleft()

            # get all neighbours
            neighbouring_rolls = 0
            neighbours = self.get_neighbours(row, col)
            for n_row, n_col in neighbours:
                # check for out of bounds
                if not self.inbounds(n_row, n_col): continue
                
                # check if neighbour is a roll
                if self.data[n_row][n_col] == '@':
                    neighbouring_rolls += 1

                # check for visited
                if (n_row, n_col) not in visited:
                    visited.add((n_row, n_col)) # ! always add to visited when adding to the queue, not when popping from the queue
                    queue.append((n_row, n_col))

            # after counting all neighbouring rolls, determine if current roll is accessible
            if self.data[row][col] == '@' and neighbouring_rolls < 4:
                accessible_rolls.append((row, col))

        return accessible_rolls

    def solve(self):
        # * Part 1
        accessible_rolls = self.forklift()
        print('Part 1: accessible rolls:', len(accessible_rolls))

        # * Part 2
        rolls_removed = 0
        while accessible_rolls:
            accessible_rolls = self.forklift()

            for row, col in accessible_rolls:
                self.data[row][col] = '.'
                rolls_removed += 1

        print('Part 2: total rolls removed:', rolls_removed)
