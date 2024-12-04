from pathlib import Path

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.data = None
        self.positions = None
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            self.data = [list(line.strip()) for line in file]

    def find_positions(self, letter):
        self.positions = [(i, j) for i, row in enumerate(self.data) for j, char in enumerate(row) if char == letter]

    def add_offset(self, position, offset):
        return tuple(a + b for a, b in zip(position, offset))
    
    def valid_positions(self, positions):
        max_rows = len(self.data)
        max_cols = len(self.data[0])
        out_of_bounds = [(row, col) for row, col in positions if not (0 <= row < max_rows and 0 <= col < max_cols)]
        return not bool(out_of_bounds)
    
    ### * Part 1
    def check_xmas(self, candidate_positions):
        letters = ['M', 'A', 'S']
                    
        for i, candidate in enumerate(candidate_positions):
            row, col = candidate
            if self.data[row][col] != letters[i]:
                return False
            
        return True

    def count_xmas(self):
        directions = {
            "right": [(0, 1), (0, 2), (0, 3)],
            "left": [(0, -1), (0, -2), (0, -3)],
            "up": [(1, 0), (2, 0), (3, 0)],
            "down": [(-1, 0), (-2, 0), (-3, 0)],
            "right-up": [(1, 1), (2, 2), (3, 3)],
            "right-down": [(-1, 1), (-2, 2), (-3, 3)],
            "left-up": [(1, -1), (2, -2), (3, -3)],
            "left-down": [(-1, -1), (-2, -2), (-3, -3)]
        }

        self.find_positions('X')
        count = 0

        for position in self.positions:
            for offsets in directions.values():
                candidate_positions = [self.add_offset(position, o) for o in offsets]
                # Check for out of bounds
                if not self.valid_positions(candidate_positions):
                    continue

                if self.check_xmas(candidate_positions):
                    count += 1

        print('Total XMASes:', count)

    ### * Part 2
    def check_cross(self, candidate_positions):
        letter1 = self.data[candidate_positions[0][0]][candidate_positions[0][1]]
        letter2 = self.data[candidate_positions[1][0]][candidate_positions[1][1]]

        if (letter1 == 'M' and letter2 == 'S') or (letter1 == 'S' and letter2 == 'M'):
            return True
        
        return False
    
    def count_x_mas(self):
        diagonals = {
            "top-left-to-bottom-right": [(-1, -1), (1, 1)],
            "top-right-to-bottom-left": [(-1, 1), (1, -1)]
        }

        self.find_positions('A')
        count = 0

        for position in self.positions:
            candidate_diagonals = {
                direction: [self.add_offset(position, o) for o in offsets]
                for direction, offsets in diagonals.items()
            }
    
            valid_cross = True
            for candidate_positions in candidate_diagonals.values():
                # Check for out of bounds
                if not self.valid_positions(candidate_positions):
                    valid_cross = False
                    break
                
                if not self.check_cross(candidate_positions):
                    valid_cross = False
                    break
            
            if valid_cross:
                count += 1
        
        print("Total X-MASes:", count)

    def solve(self):
        self.count_xmas()
        self.count_x_mas()

