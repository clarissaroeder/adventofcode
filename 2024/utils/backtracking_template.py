def some_problem(input):
    def backtrack(input, candidate, result):
        if "<<success condition>>":
            result.append(candidate.copy())
            return
    
        for elem in input: # if you need the index use `enumerate`
            if True:  # replace True with the dead-end condition
                continue
        
            candidate.append(elem)  # take
            backtrack(input, candidate, result)  # explore
            candidate.pop()  # clean up
    result = []
    candidate = []
    backtrack(input, candidate, result)
    return result

print(some_problem([1, 2, 3]))