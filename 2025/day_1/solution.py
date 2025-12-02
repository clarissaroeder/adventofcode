from pathlib import Path

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.data = None
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            self.data = [int(line.strip().replace('L', '-').replace('R', '')) for line in file]

    def solve(self):
        dial = 50
        count = 0
        
        # * Part 1: count how many times the dial ends up at 0
        # for turn in self.data:
        #     # the outcome of modulo will have the sign of the right argument
        #     # in this case 100 is positive, so always positive
        #     dial = (dial + turn) % 100 
        #     if dial == 0: count += 1

        # * Part 2: count how many times the dial passes 0 while being turned
        for turn in self.data:
            # left turn
            if turn < 0:
                # divmod(x, y) => (x // y, x % y)
                full_turns, remaining_turn = divmod(turn, -100) # -100 because we need to turn left still with the remainder, and the outcome of modulo will have the sign of the right argument
                count += full_turns

                # if the dial is currently at 0, any left turn (that's not full) will not pass 0 again
                # if the dial is not at 0, and the remaining turn goes into the negative, 0 was passed
                if dial != 0 and dial + remaining_turn <= 0:
                    count += 1
            # right turn
            else:
                full_turns, remaining_turn = divmod(turn, 100)
                count += full_turns

                # if the dial is currently at 0, any right turn (that's not full) will not pass 99 (so we don't need to check for dial != 0)
                # if the dial is not at 0, and the remaining turn passes 100, 0 was passed (as the dial goes up to 99 before wrapping)
                if dial + remaining_turn >= 100:
                    count += 1

            dial = (dial + remaining_turn) % 100

        print(count)
        
