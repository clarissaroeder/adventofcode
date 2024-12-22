from pathlib import Path

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.data = None
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            self.data = [int(line.strip()) for line in file]

    def mix(self, secret, result):
        return secret ^ result
    
    def prune(self, secret):
        return secret % 16777216

    def generate_next_secret(self, secret):
        result = secret * 64
        secret = self.mix(secret, result)
        secret = self.prune(secret)

        result = secret // 32
        secret = self.mix(secret, result)
        secret = self.prune(secret)

        result = secret * 2048
        secret = self.mix(secret, result)
        secret = self.prune(secret)

        return secret
    
    def find_second(self, prices, target):
        count = 0
        for index, price in enumerate(prices):
            if price == target: 
                count += 1
            if count == 2: return index

        return -1

    def solve(self):
        # Part 1
        secret_sum = 0
        buyers = {}
        for number in self.data:
            current_secret = number
            current_price = number % 10

            prices = [current_price]
            changes = [None]
            for _ in range(2000):
                next_secret = self.generate_next_secret(current_secret)
                next_price = next_secret % 10
                change = next_price - current_price
                changes.append(change)
                prices.append(next_price)
                
                current_secret = next_secret
                current_price = next_price

            buyers[number] = { 'prices': prices, 'changes': changes }
            secret_sum += current_secret
        
        print('Secret sum:', secret_sum)

        # Part 2
        total_bananas = {}
        for b in buyers:
            sequences = set()
            prices = buyers[b]['prices']
            changes = buyers[b]['changes']

            for i in range(len(changes) - 4 + 1):
                seq = tuple(changes[i:i + 4])
                selling_price = prices[i + 4 - 1]

                # Can only use the first time the sequence occurs
                if seq in sequences:
                    continue

                sequences.add(seq)
                if seq in total_bananas:
                    total_bananas[seq] += selling_price
                else:
                    total_bananas[seq] = selling_price

        optimal_sequence = max(total_bananas, key=total_bananas.get)
        max_bananas = total_bananas[optimal_sequence]
        print(f"Optimal sequence: {optimal_sequence}")
        print(f"Total bananas earned: {max_bananas}")



# 1. Multiply the secret number by 64. Then, mix this result into the secret number. 
# Finally, prune the secret number.
# 2. Divide the secret number by 32. Round the result down to the nearest integer. 
# Then, mix this result into the secret number. Finally, prune the secret number.
# 3. Multiply the secret number by 2048. Then, mix this result into the secret number. 
# Finally, prune the secret number.

# Mix: bitwise XOR secrex ^ result
# Prune: secret % 16777216