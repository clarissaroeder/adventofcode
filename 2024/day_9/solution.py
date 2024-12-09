from pathlib import Path
from time import time

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.data = None
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            self.data = list(file.readline().strip())

    def get_fileblocks(self):
        fileblocks = []
        file_index = 0
        for i, value in enumerate(self.data):
            count = int(value)
            if i % 2 == 0:
                fileblocks.extend([file_index] * count)
                file_index += 1
            else:
                fileblocks.extend(["."] * count)

        return fileblocks

    def checksum(self, fileblocks):
        checksum = 0
        for i, value in enumerate(fileblocks):
            if value != ".":
                checksum += (i * value)

        print("Checksum:", checksum)

    ### * Part 1
    def move_fileblocks(self, fileblocks):
        start = 0
        end = len(fileblocks) - 1

        while start < end:
            if fileblocks[end] == ".":
                end -= 1
                continue

            if fileblocks[start] != ".":
                start += 1
                continue

            if fileblocks[start] == ".":
                fileblocks[start] = fileblocks[end]
                fileblocks[end] = "."
                start += 1
                end -= 1

        self.checksum(fileblocks)

    ### * Part 2
    def move_files(self, fileblocks):
        # for each file starting from the right side, try moving it as far left as possible
        # start = 0
        end = len(fileblocks) - 1
        file_id = None
        while end > 0:
            # move end pointer in if free space is encountered
            if fileblocks[end] == ".":
                end -= 1
                continue
            
            # if a file is detected at the end
            if fileblocks[end] != ".":
                if not file_id:
                    # set file id
                    file_id = fileblocks[end]

                    # record the starting index
                    file_index = end
                    file_length = 0

                    # move pointer inwards until file is complete and count length
                    while fileblocks[end] == file_id:
                        file_length += 1
                        end -= 1

                    # now that a complete file has been found, check for free space:
                    start = 0
                    # check fileblocks up until the current file id (to ensure to stay on the left)
                    while fileblocks[start] != file_id:
                        if fileblocks[start] != ".":
                            start += 1
                            continue

                        free_index = start
                        free_length = 0

                        # move pointer inwards until the the free space is complete and count length
                        while fileblocks[start] == ".":
                            free_length += 1
                            start += 1

                        # compare free vs file length
                        if file_length <= free_length:
                            # move file
                            for _ in range(file_length):
                                fileblocks[free_index] = file_id
                                free_index += 1

                            # free previous space
                            for _ in range(file_length):
                                fileblocks[file_index] = "."
                                file_index -= 1

                            # break out of the loop if file has been moved
                            break
                        
                        # try the next free space
                            
                    # reset file_id
                    file_id = None
                    continue

        self.checksum(fileblocks)

    def solve(self):
        start_time = time()
        fileblocks = self.get_fileblocks()
        
        # * Part 1
        # self.move_fileblocks(fileblocks)

        # * Part 2
        self.move_files(fileblocks)
        end_time = time()
        print(f"Execution time: {end_time - start_time:.6f} seconds")




# 2333133121414131402
# 00...111...2...333.44.5555.6666.777.888899

# two pointers going from either side
# count the free spaces
# compare to file block length
    # third and maybe 4th pointer over the original input to check lengths?
    # split original input into files and free?
# if enough space: move, else move end to next file blcok and start over from beginning with start

# maybe do something with the lengths from input