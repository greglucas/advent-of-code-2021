print("--- DAY 24 ---")
print("--- PART 1 ---")

instructions = list()
# Keep track of each individual instruction set
instruction_set = None

with open("input.txt") as f:
    for line in f:
        line = line.strip().split()
        instruction = line[0]
        if instruction == "inp":
            # Only one value, so append that to a new list
            if instruction_set is not None:
                instructions.append(instruction_set)
            instruction_set = list()
            instruction_set.append((instruction, line[1]))
            continue
        # The first entry is always a variable, the second could
        # be a variable or an integer
        try:
            line[2] = int(line[2])
        except ValueError:
            pass
        instruction_set.append((instruction, line[1], line[2]))
    
    # Append the final list
    instructions.append(instruction_set)


def add(a, b, register):
    if isinstance(b, str):
        b = register[b]
    register[a] += b


def mul(a, b, register):
    if isinstance(b, str):
        b = register[b]
    register[a] *= b


def div(a, b, register):
    if isinstance(b, str):
        b = register[b]
    if b == 0:
        raise ValueError
    # to round towards zero we can't use //= as that will round towards -inf
    # casting the float to int does work though int(-2.5) == -2
    register[a] = int(register[a]/b)


def mod(a, b, register):
    if isinstance(b, str):
        b = register[b]
    if register[a] < 0 or b <= 0:
        raise ValueError
    register[a] %= b


def eql(a, b, register):
    if isinstance(b, str):
        b = register[b]
    register[a] = 1 if register[a] == b else 0


lookup = {"add": add,
          "mul": mul,
          "div": div,
          "mod": mod,
          "eql": eql}


def run_digit(digit, w, z):
    instruction_set = instructions[digit]
    register = {"w": w, "x": 0, "y": 0, "z": z}
    for instruction in instruction_set:
        if instruction[0] == "inp":
            continue
        # print(f"BEFORE: {register}")
        # print(instruction)
        lookup[instruction[0]](*instruction[1:], register)
    return register["z"]


def recurse(desired, digit=13, digits=dict()):
    """Recurse backwards through the digits"""
    if digit < 0:
        return digits

    # w is our input possibilities
    # Keep a dictionary lookup of output values
    # w -> (z_in, z_out)
    print(digit, " (min, max, length):", min(desired), max(desired), len(desired))
    print("Options:", max(desired)*26 + 26)
    good_zs = []
    w_dict = dict()
    for w in range(9, 0, -1):
        for z in range(max(desired)*26 + 26):
            try:
                zout = run_digit(digit=digit, w=w, z=z)
                if zout in desired:
                    # It was a value that could have gotten here
                    # append it to our list of good values for checking
                    # in the next recursive step
                    good_zs.append(z)
                    if w not in w_dict:
                        # Make the initial list
                        w_dict[w] = list()
                    
                    w_dict[w].append((z, zout))
            except ValueError:
                pass

    digits[digit] = w_dict
    digits = recurse(set(good_zs), digit=digit-1, digits=digits)

    return digits


def test_monad(monad):
    z = 0
    for i in range(14):
        w = monad[i]
        print(f"digit={i}, w={w}, z={z}")
        z = run_digit(digit=i, w=w, z=z)

    return z == 0

# OUTPUT DATA
digits = recurse([0])

# Print the output dictionary for traversing the z values
with open("output_values.txt", 'w') as f:
    for digit in digits:
        print(f"DIGIT {digit}", file=f)
        print(digits[digit], file=f)
        print(file=f)

# # Maximum Value: 96979989692495
# 9: (0, 10)
# 6: (10, 275)
# 9: (275, 7170)
# 7: (7170, 275)
# 9: (275, 7165)
# 9: (7165, 186312)
# 8: (186312, 7165)
# 9: (7165, 186304)
# 6: (186304, 7165)
# 9: (7165, 186301)
# 2: (186301, 7165)
# 4: (7165, 275)
# 9: (275, 10)
# 5: (10, 0)

# # Minimum Value 51316214181141
# 5: (0, 6)
# 1: (6, 166)
# 3: (166, 4330)
# 1: (4330, 166)
# 6: (166, 4328)
# 2: (4328, 112543)
# 1: (112543, 4328)
# 4: (4328, 112537)
# 1: (112537, 4328)
# 8: (4328, 112538)
# 1: (112538, 4328)
# 1: (4328, 166)
# 4: (166, 6)
# 1: (6, 0)

print("Maximum test 96979989692495: ", test_monad([int(x) for x in "96979989692495"]))
print("Minimum test 51316214181141: ", test_monad([int(x) for x in "51316214181141"]))
