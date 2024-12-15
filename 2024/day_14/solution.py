from pathlib import Path
import re
import os

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.robots = []
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            data = [line.strip() for line in file]
            
        p_pattern = r"p=(\d+),(\d+)"
        v_pattern = r"v=(-?\d+),(-?\d+)"

        for line in data:
            p_match = re.search(p_pattern, line)
            v_match = re.search(v_pattern, line)

            robot = { 
                "position": (int(p_match.group(1)), int(p_match.group(2))),
                "velocity": (int(v_match.group(1)), int(v_match.group(2)))
                }

            self.robots.append(robot)

    def print_robots(self, width, height):
        grid = [[0 for _ in range(width)] for _ in range(height)]

        for robot in self.robots:
            col, row = robot["position"]
            grid[row][col] += 1
        
        for row in grid:
            for col in row:
                if col == 0:
                    print(".", end="")
                else:
                    print(col, end="")
                
            print("\n")
        

    def calculate_safety_factor(self, width, height):
        x_middle = width // 2
        y_middle = height // 2
        
        q1, q2, q3, q4 = 0, 0, 0, 0
        for robot in self.robots:
            if robot["position"][0] < x_middle and robot["position"][1] < y_middle:
                q1 += 1
            elif robot["position"][0] < x_middle and robot["position"][1] > y_middle:
                q3 += 1
            elif robot["position"][0] > x_middle and robot["position"][1] < y_middle:
                q2 += 1
            elif robot["position"][0] > x_middle and robot["position"][1] > y_middle:
                q4 += 1

        return (q1 * q2 * q3 * q4)

    def predict_robots(self, width, height, seconds=100):
        for i in range(seconds):
            for robot in self.robots:
                x, y = robot["position"]
                v_x, v_y= robot["velocity"]

                x = (x + v_x) % width
                y = (y + v_y) % height

                robot["position"] = (x, y)
            
            if (i - 61) % 101 == 0:
                print('seconds:', i)
                self.print_robots(width, height)
                input()
                os.system('clear')

        safety_score = self.calculate_safety_factor(width, height)
        print("Safety:", safety_score)
  
    def solve(self):
        self.predict_robots(101, 103, 10403)

# 11 wide, 7 tall
# 101 wide, 103 tall