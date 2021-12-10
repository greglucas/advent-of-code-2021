print("--- DAY 8 ---")
print("--- PART 1 ---")

# Keep track of the left/right of the pipe
left = []
right = []
with open('input.txt') as f:
    for line in f:
        l, r = line.strip().split('|')
        left.append(l.split())
        right.append(r.split())

# Unique digits (1, 4, 7, 8)
lookup = {2: 1, 4: 4, 3: 7, 7: 8}

unique_count = 0
for line in right:
    for digit in line:
        if len(digit) in lookup:
            unique_count += 1

print(f"There are {unique_count} unique numbers on the right.")


print("--- DAY 8 ---")
print("--- PART 2 ---")

# Now we need to be able to decode each line
# The length two item are the two spots on the right column
# Then if we look at the length-3 item, we can deduce that
# the top item is the new character that appears

# The unique lengths give us 1, 4, 7, 8
# other numbers have lengths:
# 0: 6
# 2: 5
# 3: 5
# 5: 5
# 6: 6
# 9: 6

# How many times does each letter appear?
# a: 8
# b: 6
# c: 8
# d: 7
# e: 4
# f: 9
# g: 7

# For each line we will calculate which characters are mapped
# to the original map. Then use that to determine the numbers.

lookup = {'abcefg': 0, 'cf': 1, 'acdeg': 2, 'acdfg': 3,
          'bcdf': 4, 'abdfg': 5, 'abdefg': 6, 'acf': 7,
          'abcdefg': 8, 'abcdfg': 9}
total_sum = 0


def generate_character_map(unique_nums):
    """
    Creates a mapping of characters from the input numbers
    into the original character locations.
    """
    character_map = dict()
    # Initialize
    character_sum = {x: 0 for x in 'abcdefg'}

    # num is a string representing a number
    for num in unique_nums:
        if len(num) == 2:
            n2 = set(num)
        if len(num) == 3:
            n3 = set(num)
        elif len(num) == 4:
            n4 = set(num)
        elif len(num) == 7:
            n7 = set(num)
        for char in num:
            character_sum[char] += 1

    # a is the unique character between 2/3
    a_char = list(n3 - n2)[0]
    character_map[a_char] = 'a'

    for char, val in character_sum.items():
        if val == 6:
            character_map[char] = 'b'
            # d is the unique character in length-4 string
            # after b is solved for
            d_char = list(n4 - n2 - set(char))[0]
            character_map[d_char] = 'd'
        elif val == 4:
            character_map[char] = 'e'
        elif val == 9:
            character_map[char] = 'f'

    # Get the reverse mapping
    rev_map = {y: x for x, y in character_map.items()}
    # at this point we have abdef solved for
    c = list(n4 - set(rev_map['b'] + rev_map['d'] + rev_map['f']))[0]
    character_map[c] = 'c'
    g = list(n7 - set(character_map.keys()))[0]
    character_map[g] = 'g'

    return character_map


for line, answer in zip(left, right):
    character_map = generate_character_map(line)

    # We have the character map, so now replace the characters
    # in the answer line
    line_value = ''
    for num in answer:
        actual_chars = ''
        for char in num:
            actual_chars += character_map[char]
        # We need to sort the characters for our
        # lookup dictionary
        actual_chars = ''.join(sorted(actual_chars))
        line_value += str(lookup[actual_chars])
    total_sum += int(line_value)

print(f"The total of all lines is {total_sum}.")
