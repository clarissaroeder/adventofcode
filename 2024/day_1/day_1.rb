# path = 'input.txt'
path = 'example.txt'

data = File.readlines(path, chomp: true)

def solve(data)
  left, right = [], []

  data.each do |line| 
    num1, num2 = line.split()
    left.push(num1.to_i)
    right.push(num2.to_i)
  end

  left.sort!
  right.sort!
  p left, right

  total = 0
  left.each_index do |i|
    total += (left[i] - right[i]).abs
  end

  puts('total distance:' , total)
end

solve(data)