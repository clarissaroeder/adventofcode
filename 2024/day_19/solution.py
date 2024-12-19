from pathlib import Path

class TrieNode:
    def __init__(self):
        self.children = {}
        self.end_of_towel = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]
        node.end_of_towel = True

    def __str__(self):
        def _str(node, prefix='', is_last=True):
            result = ''
            children = sorted(node.children.items())
            total = len(children)
            for index, (char, child) in enumerate(children):
                is_child_last = (index == total - 1)
                connector = '└── ' if is_child_last else '├── '
                end_marker = " (End)" if child.end_of_towel else ""
                result += f"{prefix}{connector}{char}{end_marker}\n"
                extension = '    ' if is_child_last else '│   '
                result += _str(child, prefix + extension, is_child_last)
            return result
        return _str(self.root)

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.data = None
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            towels, designs = file.read().split("\n\n")

        self.towels = Trie()
        for towel in towels.split(", "):
            self.towels.insert(towel)

        self.designs = designs.split("\n")

    def count_possible_designs(self):
        def backtrack(design, index, cache):
            # End of the design is reached, 1 possible combination found
            if index == len(design):
                return 1
            
            if index in cache:
                return cache[index]
            
            # Combinations from the current index onwards
            combinations = 0
        
            # Start at the root of the towel trie
            current = self.towels.root

            # Iterate over the design starting at the current index
            for i in range(index, len(design)):
                color = design[i]

                # If the current color is not in the current children, no matching towel found
                if color not in current.children:
                    break
                
                current = current.children[color]
                # If a complete towel has been found: add number of combinations from the next index
                if current.end_of_towel:
                    combinations += backtrack(design, i + 1, cache)

            # Cache total combinations for current index
            cache[index] = combinations
            return combinations

        total_possible = 0
        total_combinations = 0
        for design in self.designs:
            cache = {}
            combinations = backtrack(design, 0, cache)

            if combinations: 
                total_possible += 1
                total_combinations += combinations


        print("Possible designs:", total_possible)
        print("Total different combos:", total_combinations)

    def solve(self):
        print(self.towels)
        self.count_possible_designs()
