from pathlib import Path

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.data = None
        self.left = []
        self.right = []
        self.occurrences = {}
        self.total_distance = 0
        self.similarity_score = 0

        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            lines = file.readlines()
        self.data = [line.strip() for line in lines]

    def parse_data(self):
        for line in self.data:
            num1, num2 = map(int, line.split())
            self.left.append(num1)
            self.right.append(num2)

        self.left.sort()
        self.right.sort()

    def calculate_total_distance(self):
        self.total_distance = sum(
            abs(self.right[i] - self.left[i])
            for i in range(len(self.right))
        )

    def calculate_similarity_score(self):
        for value in self.right:
            self.occurrences[value] = self.occurrences.get(value, 0) + 1

        self.similarity_score = sum(
            value * self.occurrences.get(value, 0)
            for value in self.left
        )

    def solve(self):
        self.parse_data()
        self.calculate_total_distance()
        self.calculate_similarity_score()

        print("Total Distance:", self.total_distance)
        print("Similarity Score:", self.similarity_score)
