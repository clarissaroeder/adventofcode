from pathlib import Path

class Advent:
    def __init__(self, input_file, part):
        self.input_file = Path(__file__).parent / input_file
        self.part = part
        self.ranges = []
        self.ingredients = []
        self._read_input()

    def _read_input(self):
        with open(self.input_file, 'r') as file:
            for line in file:
                if line.strip() == '': 
                    continue
                elif '-' in line:
                    start, stop = list(map(int, line.strip().split('-')))
                    self.ranges.append(range(start, stop))
                else:
                    self.ingredients.append(int(line.strip()))

    def binary_search(self, ranges, num):
        # i use merged ranges in the binary search because it is simpler
        # sorted ranges can also work but then you need to account for ranges that might
        # be entirely contained by other ranges, which can cause incorrect skips
        left, right = 0, len(ranges) - 1
        while left <= right:
            mid = (left + right) // 2
            # if the number is in the current range, return True
            if ranges[mid].start <= num <= ranges[mid].stop: 
                return True
            # if the number is smaller than the start, go to the left search space
            elif num < ranges[mid].start:
                right = mid - 1
            # if the number is bigger than the start, go to the right search space
            elif num > ranges[mid].stop:
                left = mid + 1
        
        return False
    
    def get_merged_ranges(self):
        sorted_ranges = sorted(self.ranges, key=lambda r: r.start)
        merged_ranges = [sorted_ranges[0]]
        i = 1
        while i < len(sorted_ranges):
            current_range = sorted_ranges[i]
            last_merged_range = merged_ranges[-1]

            if current_range.start <= last_merged_range.stop:
                merged_ranges[-1] = range(last_merged_range.start, max(current_range.stop, last_merged_range.stop))
            else:
                merged_ranges.append(current_range)

            i += 1

        return merged_ranges

    # * Part 1
    def count_fresh_ingredients(self):
        ranges = self.get_merged_ranges()
        count = 0
        for ingredient in self.ingredients:
            if self.binary_search(ranges, ingredient):
                count += 1

        print('Fresh ingredients:', count)

    # * Part 2
    def count_fresh_ingredient_ids(self):
        ranges = self.get_merged_ranges()
        count = sum([len(r) + 1 for r in ranges])
        print('Fresh ingredient IDs:', count)

    def solve(self):
        # self.count_fresh_ingredients()
        self.count_fresh_ingredient_ids()
