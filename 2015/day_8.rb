# total length - length in memory
# count size - (size - quotes/escape/hex)
# \\, \", \xZZ

class Advent
  def load_file
    # path = "input.txt"
    path = "example.txt"
    @data = File.readlines(path, chomp: true)
  end

  def calculate
    load_file

    code_characters = 0
    memory_characters = 0

    @data.each do |string|
      code_characters += string.length
      evaluated_string = eval(string)
      memory_characters += evaluated_string.length
    end

    puts "Code characters: #{code_characters}"
    puts "Memory characters: #{memory_characters}"
    puts "The result is: #{code_characters - memory_characters}"
  end
end

advent = Advent.new
advent.calculate