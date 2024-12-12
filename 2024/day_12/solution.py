from pathlib import Path

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.grid = None
        self.visited = set()
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
        return [(row + d_row, col + d_col) for d_row, d_col in offsets]
    
    def count_sequences(self, indices):
        """
        Count the number of contiguous sequences in a sorted list of indices -> the number of sides.

        Each break in the sequence (i.e., when the next index is not exactly one greater than the current)
        indicates the start of a new contiguous sequence -> a new side is detected.
        """
        sides = 1
        for i in range(len(indices) - 1):
            # If the next index is not consecutive, increment the sequence count
            if indices[i + 1] != indices[i] + 1:
                sides += 1

        return sides
    
    def calculate_total_sides(self, edge_rows, edge_cols):
        """ 
        Calculates the total number of sides.

        For each edge row and edge column, there will be the plant rows/columns from
        which the edge was detected:
    
            - A single edge row can have two edges: from the top or bottom
            - A single edge column can have two edges: from the left or right

        Each edge will have a list representing the indices along which the edge was detected.
        The number of contiguous, incrementing sequences inside this list of indices
        represents the number of sides.
        """
        total_sides = 0

        for edge_row, plant_rows in edge_rows.items():
            # sides = 0
            for plant_row, cols in plant_rows.items():
                # sort the columns to scan for contiguous sequences of columns
                cols.sort()
                total_sides += self.count_sequences(cols)

        for col, plant_cols in edge_cols.items():
            for plant_col, rows in plant_cols.items():
                # sort the rows to scan for contiguous sequences of rows
                rows.sort()
                total_sides += self.count_sequences(rows)


        return total_sides
    
    def get_circumferences(self, region):
        """Calculates perimeter and sides of a given region"""
        perimeter = 0

        edge_rows = {} # Edge rows: {edge_row_index: {plant_row_index: [edge_cols]}} -> plant_row_index = the plant row from which the edge was detected
        edge_cols = {} # Edge columns: {edge_col_index: {plant_col_index: [edge_rows]}} -> plant_col_index = the plant col from which the edge was detected

        for plant in region:
            plant_row, plant_col = plant
            neighbours = self.get_neighbours(plant)
            shared_edges = 0

            for neighbour in neighbours:
                # If neighbour is in the same region, the edge is shared
                if neighbour in region:
                    shared_edges += 1
                # If the neighbour is not in the same region, it's an outside edge
                else:
                    n_row, n_col = neighbour

                    # Horizontal edges
                    if n_row != plant_row:
                        edge_rows.setdefault(n_row, {}).setdefault(plant_row, []).append(n_col)

                    # Vertical edges
                    if n_col != plant_col:
                        edge_cols.setdefault(n_col, {}).setdefault(plant_col, []).append(n_row)
        
            # Each cell contributes 4 sides minus the shared sides to the perimeter
            perimeter += (4 - shared_edges)

        # Calculate total distinct sides
        sides = self.calculate_total_sides(edge_rows, edge_cols)
        return (perimeter, sides)

    def calculate_fence_prices(self):
        def bfs(start_position, plant):
            queue = [start_position]
            visited_local = set()
            region = []

            while queue:
                current = queue.pop(0)

                if self.out_of_bounds(current):
                    continue

                if current in visited_local:
                        continue
                
                if self.grid[current[0]][current[1]] != plant:
                    continue

                self.visited.add(current)
                visited_local.add(current)
                region.append(current)

                neighbours = self.get_neighbours(current)
                queue.extend(neighbours)

            area = len(region)
            perimeter, sides = self.get_circumferences(region)

            return (area * perimeter, area * sides)

        total = 0
        total_discounted = 0
        for i, row in enumerate(self.grid):
            for j, plant in enumerate(row):
                if (i, j) not in self.visited:
                    price, discounted_price = bfs((i, j), plant)
                    total += price
                    total_discounted += discounted_price

        print('Total fence price:', total)
        print('Total discounted fence price:', total_discounted)

    def solve(self):
        self.calculate_fence_prices()
