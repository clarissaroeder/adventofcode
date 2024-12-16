from pathlib import Path
import heapq

class Advent:
    DIRECTIONS = ["up", "right", "down", "left"]
    OFFSETS = {"up": (-1, 0), "down": (1, 0), "right": (0, 1), "left": (0, -1)}

    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            self.grid = [list(line.strip()) for line in file]

    def print_grid(self, path=[]):
        for i, row in enumerate(self.grid):
            row_string = []
            for j, cell in enumerate(row):
                if (i, j) in path:
                    row_string.append("O")
                else:
                    row_string.append(cell)
            print("".join(row_string))

    def find(self, target):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == target:
                    return (i, j)
                
    def out_of_bounds(self, position):
        row, col = position
        return row < 0 or col < 0 or row >= len(self.grid) or col >= len(self.grid[0])
                
    def wall(self, position):
        row, col = position
        return self.grid[row][col] == "#"
    
    def get_next_direction(self, direction, turn):
        i = self.DIRECTIONS.index(direction)
        
        if turn == "left":
            return self.DIRECTIONS[(i - 1) % 4]
        
        if turn == "right":
            return self.DIRECTIONS[(i + 1) % 4]

    def reconstruct_paths(self, origins, start_state, goal_state):
        all_paths = []
        current = goal_state

        # Start from goal state backwards: add state and path to the stack
        stack = [(goal_state, [goal_state[0]])]

        while stack:
            current, path = stack.pop()

            # Path completed
            if current == start_state:
                all_paths.append(path)

            # Origins will have a list of predecessors that will have led to the 
            # same minimum score: find path of every predecessor
            for prev in origins[current]:
                stack.append((prev, path + [prev[0]]))

        return all_paths

    def calculate_lowest_score(self, start, goal):
        ### Dijkstra
        # Priority queue to always process the node with the lowest score first
        priority_queue = []
        score = 0
        direction = "right"

        heapq.heappush(priority_queue, (score, start, direction))

        # State tracking: keep track what score is associated with a node and the 
        # direction in which the reindeer has travelled onto that node
        scores = {(start, direction): 0}

        # Path tracking: for each node, keep track of it's unqiue predecessors 
        # (including the direction travelled)
        origins = {(start, direction): set()}

        # Possible directions the reindeer can take
        turns = ["straight", "left", "right"]

        while priority_queue:
            current_score, current, current_direction = heapq.heappop(priority_queue)

            # Part 2: don't break to find all best paths
            if current == goal:
                # break
                continue
            
            x, y = current
            for turn in turns:
                if turn == "straight":
                    next_direction = current_direction
                    cost = 1
                else:
                    next_direction = self.get_next_direction(current_direction, turn)
                    cost = 1001

                dx, dy = self.OFFSETS[next_direction]
                next = (x + dx, y + dy)

                if self.out_of_bounds(next) or self.wall(next):
                    continue

                next_score = current_score + cost

                # If the next state hasn't been explored yet, or a cheaper path has been
                # found, track the score for this state in `scores` and add it to the q
                if (next, next_direction) not in scores or next_score < scores[(next, next_direction)]:
                    scores[(next, next_direction)] = next_score
                    heapq.heappush(priority_queue, (next_score, next, next_direction))
                    origins[(next, next_direction)] = {(current, current_direction)}
                # If a next state has the same score as previously encountered, track
                # the current state as its predecessor to find all best paths
                elif next_score == scores[(next, next_direction)]:
                    origins[(next, next_direction)].add((current, current_direction))

        # Goal state = the state of the goal tile with the lowest score
        goal_state = min((state for state in scores if state[0] == goal), key=scores.get)

        # Reconstruct the paths that lead to the goal state
        best_paths = self.reconstruct_paths(origins, (start, direction), goal_state)
        unique_tiles = set().union(*best_paths)

        return scores[goal_state], len(unique_tiles)


    def solve(self):
        start = self.find("S")
        goal = self.find("E")

        lowest_score, tiles = self.calculate_lowest_score(start, goal)
        print("Lowest score:", lowest_score)
        print("Tiles:", tiles)
