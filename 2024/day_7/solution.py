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
            
            # Try continuing with the same operator
            if dfs(current_result, i + 1, operator):
                return True
            
            # Try other operators
            for new_operator in operators:
                if new_operator != operator:
                    if dfs(current_result, i + 1, new_operator):
                        return True
                    
            return False

        return any(dfs(numbers[0], 1, operator) for operator in operators)


    def solve_part1(self):
        total = 0
        for t, nums in self.data.items():
            if self.solvable(t, nums, self.base_operators):
                total += t
            else:
                self.unsolvable[t] = nums
        print("part 1:", total)
        return total
    
    def solve_part2(self):
        total = sum(t for t, nums in self.unsolvable.items() if self.solvable(t, nums, self.extended_operators))
        return total

    def solve(self):
        sum1 = self.solve_part1()
        sum2 = self.solve_part2()
        print("part 2:", sum1 + sum2)

