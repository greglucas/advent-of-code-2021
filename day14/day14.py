print("--- DAY 14 ---")
print("--- PART 1 ---")

rules = {}
with open('input.txt') as f:
    template = list(f.readline().strip())
    f.readline()
    for line in f:
        pair, insertion = line.strip().split(' -> ')
        # Keep track of the insertion character mapping
        rules[tuple(pair)] = insertion


def step(line):
    newline = [line[0]]
    # Considering two elements at a time
    for i in range(len(line) - 1):
        pair = tuple(line[i:i+2])
        if pair in rules:
            newline += [rules[pair], pair[1]]
        else:
            newline += list(pair[0])
    return newline


line = template
for i in range(10):
    line = step(line)

char_dict = {}
for char in line:
    if char in char_dict:
        char_dict[char] += 1
    else:
        char_dict[char] = 1

diff = max(char_dict.values()) - min(char_dict.values())
print(f"The difference between the min and max characters is {diff}.")


print("--- DAY 14 ---")
print("--- PART 2 ---")

# We aren't going to be able to grow our list without bounds.
# Lets try to keep track of all of the pairs in a new dict
# and how many times those occur. In the first example, NNCB
# will produce new pairs:
# NN -> NC, NB

rules = {}
with open('input.txt') as f:
    template = list(f.readline().strip())
    f.readline()
    for line in f:
        pair, insertion = line.strip().split(' -> ')
        # Keep track of the new pairs that are created
        rules[tuple(pair)] = ((pair[0], insertion), (insertion, pair[1]))


# Now we want the template to be a dictionary of pairs and their counts
pair_dict = dict()
for i in range(len(template) - 1):
    pair = tuple(template[i:i+2])
    if pair in pair_dict:
        pair_dict[pair] += 1
    else:
        pair_dict[pair] = 1

def step(pair_dict):
    new_pairs = dict()
    for pair, val in pair_dict.items():
        if pair in rules:
            for p in rules[pair]:
                if p in new_pairs:
                    new_pairs[p] += val
                else:
                    new_pairs[p] = val
        else:
            if pair in new_pairs:
                new_pairs[pair] += val
            else:
                new_pairs[pair] = val
    return new_pairs


for i in range(40):
    pair_dict = step(pair_dict)

# Keep track of characters, adding one for the final
# one of the template
char_dict = {template[-1]: 1}
for p, val in pair_dict.items():
    # Only keep track of the first character of the pair
    if p[0] in char_dict:
        char_dict[p[0]] += val
    else:
        char_dict[p[0]] = val

diff = max(char_dict.values()) - min(char_dict.values())
print(f"The difference between the min and max characters is {diff}.")
