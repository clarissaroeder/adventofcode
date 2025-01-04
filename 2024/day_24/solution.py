from pathlib import Path
from collections import deque
import re

class Gate:
    def __init__(self, input1, input2, operator, output):
        self.input1 = input1
        self.input2 = input2
        self.operator = operator
        self.output = output

    def __str__(self):
        return f"{self.input1} {self.operator} {self.input2} -> {self.output}"
    
    def __repr__(self):
        return f"{self.input1} {self.operator} {self.input2} -> {self.output}"

class Advent:
    def __init__(self, input_file):
        self.input_file = Path(__file__).parent / input_file
        self.values = {} # key: wire, value: its value once it's been computed (contains only known wire-values)
        self.gates = {}  # key: output wire, value: gate
        self.operator = {
            'AND': lambda x, y: x & y,
            'OR': lambda x, y: x | y,
            'XOR': lambda x, y: x ^ y
        }
        self.queue = deque([])
        self.processed = set()
        self.read_input()

    def read_input(self):
        with open(self.input_file, 'r') as file:
            wire_section, gate_section = [data.split("\n") for data in file.read().split("\n\n")]

        for entry in wire_section:
            wire, value = entry.split(": ")
            self.values[wire] = int(value)

        pattern = r' -> | '
        for entry in gate_section:
            input1, operator, input2, output = re.split(pattern, entry)
            gate = Gate(input1, input2, operator, output)
            self.gates[output] = gate

    def get_binary(self, prefix):
        prefix_wires = { wire: value for wire, value in self.values.items() if wire.startswith(prefix)}
        prefix_keys = sorted(prefix_wires.keys(), key=lambda x: int(x[1:]))
        prefix_keys.reverse()

        binary = ''.join(str(prefix_wires[key]) for key in prefix_keys)
        return binary
    
    # enqueues gates whose inputs are available in the wires and haven't been processed yet
    def enqueue_gates(self):
        for gate in self.gates.values():
            if (
                gate not in self.processed
                and gate.input1 in self.values 
                and gate.input2 in self.values 
                and gate.output not in self.values
            ):
                self.queue.append(gate)
                self.processed.add(gate)

    def calculate(self):
        self.enqueue_gates()
        while self.queue:
            current = self.queue.popleft()
            result = self.operator[current.operator](self.values[current.input1], self.values[current.input2])
            self.values[current.output] = result
            self.enqueue_gates()

    def solve(self):
        # print(self.values)
        # for gate in self.gates.values():
        #     print(gate)
        # print("")

        ### * Part 1
        self.calculate()

        ### * Part 2
        x_binary = self.get_binary('x')
        y_binary = self.get_binary('y')
        expected_z = bin(int(x_binary, 2) + int(y_binary, 2))[2:]

        print(f'X:     {x_binary} - {int(x_binary, 2)}')
        print(f'Y:     {y_binary} - {int(y_binary, 2)}')
        print("----------------------------------------------------------------------")
        print(f'Exp:  {expected_z} - {int(expected_z, 2)}')

        z_binary = self.get_binary('z')
        print(f'Z:    {z_binary} - {int(z_binary, 2)}')


        print("")
        faulty_wires = []
        for output, gate in self.gates.items():
            if output.startswith('z') and gate.operator != 'XOR':
                if output != 'z45':
                    faulty_wires.append(output)

            if (
                not output.startswith('z') 
                and not (gate.input1.startswith('x') or gate.input1.startswith('y')) 
                and not (gate.input2.startswith('x') or gate.input2.startswith('y')) 
                and gate.operator == 'XOR'
            ):
                faulty_wires.append(output)

            if (
                (gate.input1.startswith('x') or gate.input1.startswith('y'))
                and (gate.input2.startswith('x') or gate.input2.startswith('y'))
                and gate.operator == 'OR'
            ):
                faulty_wires.append(output)

            faulty = True
            if (
                gate.operator == 'AND'
                and not (gate.input1.startswith('x00') or gate.input1.startswith('y00')) 
                and not (gate.input2.startswith('x00') or gate.input2.startswith('y00')) 
            ):
                for _, g in self.gates.items():
                    if g.input1 == output or g.input2 == output:
                        if g.operator == 'OR':
                            faulty = False
                    
                if faulty:
                    faulty_wires.append(output)

            faulty = True
            if (
                gate.operator == 'XOR' 
                and (gate.input1.startswith('x') or gate.input1.startswith('y'))
                and (gate.input2.startswith('x') or gate.input2.startswith('y'))
                and not output == 'z00'
            ):
                # print(gate)
                for o, g in self.gates.items():
                    if g.operator == 'XOR':
                        if g.input1 == output or g.input2 == output:
                            # print('found: ', g)
                            faulty = False
                            break

                if faulty:
                    faulty_wires.append(output)

            if (
                (gate.input1.startswith('x') or gate.input1.startswith('y'))
                and (gate.input2.startswith('x') or gate.input2.startswith('y'))
                and output.startswith('z')
                and not output == 'z00'
            ):
                faulty_wires.append(output)


            
 

        print(",".join(sorted(list(set((faulty_wires))))))


### * Part 2
# last layer of gates can only be XOR (except for most significant bit)
# intermediate layer of gates (no x, y inputs and no z output) can only by AND/OR
# this is because XOR doesn't appropriately account for the carry over which is handled by the middle layers
# the last layer - the XOR layer - is only concerned with the correct sum bit, not carry over
    # the sum bit: is 1 if the two operand bits are different, 0 if they are the same 
