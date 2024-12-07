from pathlib import Path

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.data = None
        self.unsolvable = {}
        self.base_operators = ["+", "*"]
        self.extended_operators = ["+", "*", "||"]
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            self.data = {
                int(target): list(map(int, numbers.split()))
                for line in file
                for target, numbers in [line.strip().split(":")]
            }

    def calculate(self, num1, num2, operator):
        if operator == "+":
            return num1 + num2
        elif operator == "*":
            return num1 * num2
        elif operator == "||":
            return int(str(num1) + str(num2))


    def solvable(self, target, numbers, operators):
        def dfs(result, i, operator):
            if i >= len(numbers):
                return result == target
        
            current_result = self.calculate(result, numbers[i], operator)
            if current_result > target:
                return False
   
            for new_operator in operators:
                if dfs(current_result, i + 1, new_operator):
                    return True
                    
            return False

        return any(dfs(numbers[0], 1, operator) for operator in operators)

    def solve(self):
        total1 = sum(t for t, nums in self.data.items() if self.solvable(t, nums, self.base_operators))
        print("part 1:", total1)
        total2 = sum(t for t, nums in self.data.items() if self.solvable(t, nums, self.extended_operators))
        print("part 2:", total2)

