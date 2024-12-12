from pathlib import Path

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.grid = None
        self.fenced = {}
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            self.grid = [list(line.strip()) for line in file]

    def out_of_bounds(self, position):
        row, col = position
        return row < 0 or col < 0 or row >= len(self.grid) or col >= len(self.grid[0])
    
    def get_neighbours(self, position):
        row, col = position
        offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        return [
            (row + drow, col + dcol)
            for drow, dcol in offsets
        ]
    
    def calculate_sides(self, edge_rows, edge_cols):
        total_sides = 0
        for row, plant_rows in edge_rows.items():
            print('plant rows:', plant_rows)

            sides = 0
            for plant_row, cols in plant_rows.items():
                print('plant_row:', plant_row)
                cols.sort()
                sides += 1
                for i in range(len(cols) - 1):
                    if cols[i + 1] != cols[i] + 1:
                        sides += 1
                
            total_sides += sides
            print(f"row {row} has {sides} sides")

        for col, plant_cols in edge_cols.items():
            print('plant cols:', plant_cols)
            
            sides = 0
            for plant_col, rows in plant_cols.items():
                print('plant_col:', plant_col)
                rows.sort()
                sides += 1
                for i in range(len(rows) - 1):
                    if rows[i + 1] != rows[i] + 1:
                        sides += 1

            total_sides += sides
            print(f"col {col} has {sides} sides")

        return total_sides
    
    def get_circumferences(self, region):
        perimeter = 0

        edge_rows = {}
        edge_cols = {}
        # print('REGION:', region)
        # sorted_region = sorted(region)
        # print('SORTED:', sorted_region)
        # print("")

        for plant in region:
            print('CURRENT PLANT:', plant)
            plant_row, plant_col = plant
            
            neighbours = self.get_neighbours(plant)
            shared_sides = 0
            for neighbour in neighbours:
                if neighbour in region:
                    shared_sides += 1
                else:
                    print('edge neighbour:', neighbour)
                    n_row, n_col = neighbour

                    if n_row != plant_row:
                        print(f"plant row {plant_row}: appending edge column {n_col} to edge row {n_row}")
                        print("")
                        if edge_rows.get(n_row, []):
                            if edge_rows[n_row].get(plant_row, []):
                                edge_rows[n_row][plant_row].append(n_col)
                            else:
                                edge_rows[n_row][plant_row] = [n_col]
                        else: 
                            edge_rows[n_row]= { plant_row: [n_col] }

                    if n_col != plant_col:
                        print(f"plant col {plant_col}: appending edge row {n_row} to edge col {n_col}")
                        print("")
                        if edge_cols.get(n_col, []):
                            if edge_cols[n_col].get(plant_col, []):
                                edge_cols[n_col][plant_col].append(n_row)
                            else:
                                edge_cols[n_col][plant_col] = [n_row]
                        else:
                            edge_cols[n_col] = { plant_col: [n_row] }
        

            perimeter += (4 - shared_sides)

        # sorted_region = sorted(region, key=lambda x: (x[1], x[0]))

        # for plant in sorted_region:
        #     print('CURRENT PLANT:', plant)
        #     plant_row, plant_col = plant
            
        #     neighbours = self.get_neighbours(plant)
        #     for neighbour in neighbours:
        #         if neighbour in region:
        #             continue
        #         else:
        #             print('edge neighbour:', neighbour)
        #             n_row, n_col = neighbour

        #             if n_col != plant_col:
        #                 if edge_cols.get(n_col, []):
        #                     edge_cols[n_col].append(n_row)
        #                 else:
        #                     edge_cols[n_col] = [n_row]


        # print("")
        # print('REGION:', region)
        # print('SORTED:', sorted_region)
        print("")
        print('edge rows:', edge_rows)
        print('edge_cols:', edge_cols)
        print("")
        sides = self.calculate_sides(edge_rows, edge_cols)
        return (perimeter, sides)

    def calculate_fence_prices(self):
        def bfs(start_position, plant):
            print(f"plant {plant}")
            queue = [start_position]
            visited = {}

            region = []

            while queue:
                current = queue.pop(0)

                if self.out_of_bounds(current):
                    continue

                if visited.get(current, False):
                        continue
                
                if self.grid[current[0]][current[1]] != plant:
                    continue

                visited[current] = True
                self.fenced[current] = True
                region.append(current)

                neighbours = self.get_neighbours(current)
                queue.extend(neighbours)

            area = len(region)
            perimeter, sides = self.get_circumferences(region)
            print("")
            print('area:', area)
            print('perimeter:', perimeter)
            print('sides:', sides)
            print("------------------------")
            print("")

            return (area * perimeter, area * sides)
        

        total = 0
        total_discounted = 0
        for i, row in enumerate(self.grid):
            for j, plant in enumerate(row):
                if not self.fenced.get((i, j), []):
                    price, discounted_price = bfs((i, j), plant)
                    total += price
                    total_discounted += discounted_price

        print('total fence price:', total)
        print('total discounted fence price:', total_discounted)

    def solve(self):
        self.calculate_fence_prices()


# 975248 too high
# 833505 too high
# 830042 too low