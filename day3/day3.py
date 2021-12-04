print("--- DAY 3 ---")
print("--- PART 1 ---")

with open('input.txt') as f:
    # Now start iterating through the directions
    num_lines = 1
    curr_sum = [int(x) for x in f.readline().strip()]
    for line in f:
        num_lines += 1
        curr_sum = [x + int(y) for (x, y) in zip(curr_sum, line.strip())]

gamma = [1 if x > num_lines/2 else 0 for x in curr_sum]
# Epsilon is going to be the opposite
epsilon = [1-x for x in gamma]
# Convert binary to decimal
gamma = sum([x*2**i for i, x in enumerate(gamma[::-1])])
epsilon = sum([x*2**i for i, x in enumerate(epsilon[::-1])])

print(f"The gamma rate is {gamma} and the epsilon rate is {epsilon}.")
print(f"The submission answer is {gamma*epsilon}")

print("--- PART II ---")

# I don't see any way to get around having to read in and
# store all value for this puzzle. So, lets make a list of
# lists to store each binary value. We could potentially even
# store the int and convert back/forth to binary within Python.

with open('input.txt') as f:
    # Populate the list
    data = []

    for line in f:
        data += [[int(x) for x in line.strip()]]


def split_list(data, loc, criteria='oxygen'):
    """
    Split the list into two distinct lists of zeros and ones.
    Then recursively call this function with the new list
    depending on the criteria desired.

    This could run into issues if two values are identical due
    to the return being based on a length-one list.
    """
    if len(data) == 1:
        return data[0]
    if loc == len(data[0]):
        # Wrap the bit around
        loc = 0

    # Iterate over the list separating the zeros and ones
    zeros = []
    ones = []
    for x in data:
        if x[loc] == 0:
            zeros += [x]
        else:
            ones += [x]

    # Decide which list to recursively call with
    if ((criteria == 'oxygen' and len(zeros) <= len(ones)) or
            (criteria == 'co2' and len(zeros) > len(ones))):
        return split_list(ones, loc+1, criteria=criteria)
    return split_list(zeros, loc+1, criteria=criteria)


oxygen = split_list(data, 0, 'oxygen')
# Turn binary into int
oxygen = sum([x*2**i for i, x in enumerate(oxygen[::-1])])
co2 = split_list(data, 0, 'co2')
co2 = sum([x*2**i for i, x in enumerate(co2[::-1])])

print(f"The oxygen generator rating is {oxygen} and the "
      f"CO2 scrubber rating is {co2}.")
print(f"The submission answer is {oxygen*co2}")
