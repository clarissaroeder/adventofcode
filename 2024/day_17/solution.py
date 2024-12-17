from pathlib import Path
import re

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.registers = {}
        self.program = []
        self.pointer = 0
        self.instructions = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv
        }
        self.output = []

        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            data = file.read()

        registers, program = data.split("\n\n")
    
        regex = r"Register\s+(\w+):\s+(\d+)"
        for register in registers.split("\n"):
            match = re.match(regex, register)
            key = match.group(1)
            value = int(match.group(2))

            self.registers[key] = value

        self.program = [int(num) for num in re.findall(r"\d+", program)]

    def get_combo_operand(self, operand):
        if operand == 4: return self.registers["A"]
        if operand == 5: return self.registers["B"]
        if operand == 6: return self.registers["C"]
        if operand == 7: return None
        
        return operand

    def adv(self, literal, combo):
        numerator = self.registers["A"]
        denominator = 2 ** combo
        result = numerator // denominator
        self.registers["A"] = result

    def bxl(self, literal, combo):
        result = self.registers["B"] ^ literal
        self.registers["B"] = result

    def bst(self, literal, combo):
        result = combo % 8
        self.registers["B"] = result

    def jnz(self, literal, combo):
        if self.registers["A"] == 0:
            return
        
        self.pointer = literal
        return True

    def bxc(self, literal, combo):
        result = self.registers["B"] ^ self.registers["C"]
        self.registers["B"] = result

    def out(self, literal, combo):
        result = combo % 8

        # print("Combo:", combo)
        # print("Registers:", self.registers)
        # print("OUT result:", result)
        # print("")
        self.output.append(result)

    def bdv(self, literal, combo):
        numerator = self.registers["A"]
        denominator = 2 ** combo
        result = numerator // denominator
        self.registers["B"] = result

    def cdv(self, literal, combo):
        numerator = self.registers["A"]
        denominator = 2 ** combo
        result = numerator // denominator
        self.registers["C"] = result

    def calculate(self, a=None):
        # Following 2 lines are for part 2 only
        if a: self.registers["A"] = a
        self.reset()

        while self.pointer < len(self.program):
            opcode = self.program[self.pointer]
            operand = self.program[self.pointer + 1]
            combo = self.get_combo_operand(operand)

            skip = self.instructions[opcode](operand, combo)
            if skip: continue

            self.pointer += 2

        return self.output

    def reset(self):
        self.registers["B"], self.registers["C"] = 0, 0
        self.pointer = 0
        self.output = []

    def solve(self):
        # Part 1
        final_output = self.calculate()
        print("Final Output:", ",".join(map(str, final_output)))

        # Part 2
        target = self.program[::-1]
        def find_a(a=0, depth=0):
            # Base case: if depth == length of original programme, we have found all parts of A
            if depth == len(target):
                return a

            # Try every 3-bit number 
            for i in range(8):
                # a * 8 shifts A left by 3 bits, making space for the next 3-bit number
                output = self.calculate(a * 8 + i)
            
                # Check if the first num of the current output matches the target at the current depth
                if output and output[0] == target[depth]:
                    # Recursively find the next part of A
                    result = find_a((a * 8 + i), depth + 1)
                    if result: return result

            # Failure
            return 0

        result = find_a()
        print("Minimum A:", result)
        

# Part 2
# Pointer always resets to 0 creating a loop
# A gets divided by 8 on each loop, until A is 0
# B % 8 is appended to output
# B depends on A on each loop (several operations)

# As smallest part on each loop is cut off and it is on this that B and the output
# is dependent
# To reconstruct A, reverse the output so that we start with the biggest part of A
# i.e. the leftmost digit
# Each digit of A is a 3-bit number (0-7)