from pathlib import Path

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.data = None
        self.safe_count = 0
        self.unsafe_reports = []
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            self.data = [line.strip() for line in file]

    def parse_data(self):
        self.data = [list(map(int, line.split())) for line in self.data]

    def count_safe_reports(self):
        for report in self.data:
            if report[0] > report[-1]:
                report.reverse()

            if self.is_safe(report):
                self.safe_count += 1
            else:
                self.unsafe_reports.append(report)


    def is_safe(self, report):
        valid_differences = [1, 2, 3]

        for index in range(len(report) - 1):
            if report[index + 1] < report[index] or (report[index + 1] - report[index]) not in valid_differences:
                return False
            
        return True

    def problem_dampener(self):
        for report in self.unsafe_reports:
            for index in range(len(report)):
                dampenend_report = report[:index] + report[index + 1:]

                if self.is_safe(dampenend_report):
                    self.safe_count += 1
                    break

    def solve(self):
        self.parse_data()
        self.count_safe_reports()
        print("Safe reports:", self.safe_count)
        
        self.problem_dampener()
        print("Safe reports with dampener:", self.safe_count)