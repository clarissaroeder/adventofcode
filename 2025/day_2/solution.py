from pathlib import Path

class Advent:
    def __init__(self, input_file, part):
        self.input_file = Path(__file__).parent / input_file
        self.part = part
        self.data = self._read_input()

    def _read_input(self):
        with open(self.input_file, 'r') as file:
            return[tuple(map(int, range.split('-'))) for range in file.readline().split(',')]

    def is_invalid(self, id):
        id_string = str(id)

        # * Part 1
        if self.part == 1:
            # id is invalid if consisting of digits repeated exactly twice 
            # (no extra digits, just 2 repetitions)
            # odd length cannot be repeated twice
            if len(id_string) % 2 == 1: return False
        
            # half the string and compare the two halves
            middle = len(id_string) // 2
            return id_string[:middle] == id_string[middle:]
        # * Part 2
        else:
            # id is invalid if it only consists of repetitions, minimum 2
            # no repetitions in single digits
            if len(id_string) == 1: return False
            n = len(id_string)
            
            # check all possible sizes: from 1 up until half of the string length 
            # (cause it needs to be repeated at least twice)
            for size in range(1, (n // 2) + 1): 
                # skip sizes that can't be repeated in whole numbers
                if n % size != 0: continue

                candidate = id_string[:size] # repeating pattern candidate
                # multiply the candidate by the number of times the current size fits in the string and compare
                if candidate * (n // size) == id_string:
                    return True
    
    def generate_invalid_ids(self, start, end):
        invalid_ids = set()

        # find the minimum and maximum lengths of the ids
        min_length = len(str(start))
        max_length = len(str(end))

        # for each possible id length (total number of digits)
        for length in range(min_length, max_length + 1):
            # for each possible pattern length
            for pattern_length in range(1, (length // 2) + 1):
                # pattern must divide the id string evenly
                if length % pattern_length != 0: continue

                # calculate number of repetitions for this pattern length
                repetitions = length // pattern_length

                # * Part 1: only exactly 2 repetitions
                if self.part == 1 and repetitions != 2:
                    continue

                # calculate the minimum and maximum digit patterns
                # this gives the smallest number of pattern_length digits (no leading 0s):
                # pattern_length = 1: special case, is 1
                # pattern_length = 2: 10^(2-1) = 10^1 = 10
                # pattern_length = 3: 10^(3-1) = 10^2 = 100
                # pattern_length = 4: 10^(4-1) = 10^3 = 1000
                min_pattern = 10 ** (pattern_length - 1) if pattern_length > 1 else 1

                # this gives the largest number of pattern_length digits:
                # pattern_length = 1: 10^1 - 1 = 10 - 1 = 9
                # pattern_length = 2: 10^2 - 1 = 100 - 1 = 99
                # pattern_length = 3: 10^3 - 1 = 1000 - 1 = 999
                # pattern_length = 4: 10^4 - 1 = 10000 - 1 = 9999
                max_pattern = 10 ** pattern_length - 1 

                for pattern in range(min_pattern, max_pattern + 1):
                    invalid_id = int(str(pattern) * repetitions)
                    # check if in range
                    if start <= invalid_id <= end:
                        invalid_ids.add(invalid_id)

        return invalid_ids

    def solve(self):
        # Approach 1: checks each number in the range for repeating patterns
        id_sum = 0
        # for start, end in self.data:
        #     for id in range(start, end + 1):
        #         if self.is_invalid(id):
        #             id_sum += id

        # Approach 2: generating invalid ids rather than checking all is more efficient
        for start, end in self.data:
            invalid_ids = self.generate_invalid_ids(start, end)
            id_sum += sum(invalid_ids)
        
        print('Sum of invalid IDs:', id_sum)
        
