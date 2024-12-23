from pathlib import Path
from itertools import combinations

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.network = {}
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            data = [list(line.strip().split("-")) for line in file]

        for value1, value2 in data:
            if self.network.get(value1, None):
                self.network[value1].add(value2)
            else:
                self.network[value1] = {value2}

            if self.network.get(value2, None):
                self.network[value2].add(value1)
            else:
                self.network[value2] = {value1}

    def display_network(self):
        for computer, connections in self.network.items():
            print(f"{computer} - {connections}")
        print("\n")

    def party(self, computers):
        pairs = list(combinations(list(computers), 2))
        for c1, c2 in pairs:
            if c2 not in self.network[c1]:
                return False
            
        return True

    # Part 1
    def count_sets_of_three(self):
        parties = set()
        for computer, connections in self.network.items():
            pairs = list(combinations(list(connections), 2))
            for pair in pairs:
                if self.party(pair):
                    parties.add(tuple(sorted(pair + (computer, ))))

        parties = {party for party in parties if any(c.startswith('t') for c in party)}
        print(f'Parties: {len(parties)}')

    # Part 2
    def find_largest_party(self):
        parties = set()
        for computer, connections in self.network.items():
            party_found = False
            for i in range(len(connections) + 1, 2, -1):
                pairs = list(combinations(list(connections), i))
                for pair in pairs:
                    if self.party(pair):
                        party_found = True
                        parties.add(tuple(sorted(pair + (computer,))))
                
                if party_found: break

        largest_party = max(parties, key=len)
        print('Largest party:', ",".join(largest_party))

    def solve(self):
        # self.display_network()
        self.count_sets_of_three()
        self.find_largest_party()


