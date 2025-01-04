from pathlib import Path

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.locks= []
        self.keys = []
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            data = [
                    [list(line) for line in block.split("\n")]
                    for block in file.read().split("\n\n")
                ]

        for block in data:
            transposed_block = [list(row) for row in zip(*block)]
            if '#' in block[0]:
                self.locks.append(transposed_block)
            elif '.' in block[0]:
                self.keys.append(transposed_block)

    def find_heights(self):
        self.lock_heights = []

        for lock in self.locks:
            heights = []
            for row in lock:
               height = row.index('.') - 1
               heights.append(height)

            self.lock_heights.append(heights)

        self.key_heights = []

        for key in self.keys:
            heights = []
            for row in key:
                height = row.index('#') - 1
                heights.append(height)

            self.key_heights.append(heights)

    def count_fitting_keys(self):
        counter = 0
        for lock in self.lock_heights:
            # print('Lock:', lock)
            
            overlap = False
            for key in self.key_heights:
                # print('Key: ', key)

                for i in range(len(lock)):
                    # print(f'Index {i}:')
                    # print(f'Lock height   : {lock[i]}')
                    # print(f'Key free space: {key[i]}')
                    # print("")
                    if key[i] < lock[i]:
                        # print('Overlap detected!\n')
                        overlap = True
                        break
                
                if not overlap:
                    counter += 1

                overlap = False # reset

        print('Count:', counter)

    def solve(self):
        # print('Locks:\n')
        # for lock in self.locks:
        #     for row in lock:
        #         print("".join(row))
        #     print("\n")

        # print('Keys:\n')
        # for key in self.keys:
        #     for row in key:
        #         print("".join(row))
        #     print("\n")

        self.find_heights()
        self.count_fitting_keys()
