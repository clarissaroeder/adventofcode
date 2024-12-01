# Load file
path = 'example.txt'
# path = 'springs.txt'
with open(path, 'r') as file:
    lines = file.readlines()

rows = []
groups = []

for line in lines:
    row, numbers = line.strip().split(' ')
    rows.append([char for char in row])
    groups.append(list(map(lambda x: int(x), numbers.split(','))))

DAMAGED = "#"
OPERATIONAL = "."
UNKNOWN = "?"

class Solution:
    def __init__(self, rows, groups):
        self.rows = rows
        self.groups = groups

    def solve(self):
        result = 0
        for i in range(len(self.rows)):
            row = self.rows[i]
            group = self.groups[i]

            result += self.possible_arrangements(row, group)

        print(result)
        return result
    
    def possible_arrangements(row, group):
        damaged = '#'
        functional = '.'
        unknown = '?'
        
        # iterate over the springs:
        # if the spring is functional, increase functional count
        # if the spring is damaged, increase damaged count
            # if the max_damaged is exceeded by damaged count, return 0 (no possible way by default)
            # if the max_damaged is met and the next spring is functional, pop the next group
        # if unknown, we are basically at a junction with two ways to go:

        # helper backtracking function:
            # if the end of the row is reached: valid permutation found, return 1

            # for each option of unknown, ie damaged or functional:
                # choose one option
                # continue iterating until the next junction
                    # if backtracking(next junction) leads to the end of the row, return 1 (or some sort of count?)
                    # else return 0
        def backtrack(row, group):


        

Solution(rows, groups).solve()