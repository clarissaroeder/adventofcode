class Circuit
  TRANSFORMATIONS = {
      "LSHIFT" => "<<",
      "RSHIFT" => ">>",
      "AND" => "&",
      "NOT" => "~",
      "OR" => "|",
      /\b(if|do|in)\b/ => "\\1_"
    }

  def add_wire(line)

    TRANSFORMATIONS.each do |from, to|
      line.gsub!(from, to)
    end

    expression, wire = line.split(" -> ")

    method = "def #{wire}; @#{wire} ||= #{expression}; end"

    # puts method
    instance_eval(method)
  end
end

# Load file
path = "input.txt"
# path = "example.txt"
data = File.readlines(path, chomp: true)

circuit = Circuit.new
data.each { |line| circuit.add_wire(line) }

circuit.add_wire("3176 -> b")
puts "The result is: #{circuit.a}"
