print("--- DAY 18 ---")
print("--- PART 1 ---")


def explode(line):
    depth = 0
    for i, char in enumerate(line):
        if char == "[":
            depth += 1
            continue
        elif char == "]":
            depth -= 1
            continue
        if (char == "," and depth > 4 and 
                line[i-1] not in '[]' and line[i+1] not in '[]'):
            # We are at a pair that should be exploded

            # left side
            j = i-2
            while j > 0:
                if line[j] not in '[],':
                    # This is our left-most value
                    new_val = int(line[j]) + int(line[i-1])
                    line[j] = str(new_val)
                    break
                j -= 1
            # right side
            j = i+2
            while j < len(line):
                if line[j] not in '[],':
                    # This is our right-most value
                    new_val = int(line[j]) + int(line[i+1])
                    line[j] = str(new_val)
                    break
                j += 1

            # Explode this value and insert 0
            line[i+2] = "0"
            del line[i-2:i+2]
            return line
    return line


def split(line):
    for i, char in enumerate(line):
        if char in "[],":
            continue
        val = int(char)
        if val > 9:
            # Split this number
            left = val // 2
            right = val - left
            del line[i]
            for char in ['[', str(left), ',', str(right), ']'][::-1]:
                line.insert(i, char)
            return line
    return line


def process(line):
    # Recursively go through these methods
    orig_line = list(line)
    line = explode(line)
    if line != orig_line:
        process(line)
    orig_line = list(line)
    line = split(line)
    if line != orig_line:
        process(line)
    return line


def add(line1, line2):
    return ['['] + line1 + [','] + line2 + [']']


def magnitude(line):
    for i, char in enumerate(line):
        if char == '[':
            continue
        if char == "," and line[i-1] not in '[]' and line[i+1] not in '[]':
            # This is a pair
            left = int(line[i-1])
            right = int(line[i+1])
            val = 3*left + 2*right
            line[i+2] = str(val)
            del line[i-2:i+2]
            return magnitude(line)
    return int(line[0])


# line = list("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
# line = list("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
# line = list("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]")

with open("input.txt") as f:
    line1 = list(f.readline().strip())
    for line in f:
        line2 = list(line.strip())
        newline = add(line1, line2)
        line1 = process(newline)

print(f"The magnitude of our list is: {magnitude(line1)}")


print("--- DAY 18 ---")
print("--- PART 2 ---")

# Now we need to keep all lines
lines = list()
with open("input.txt") as f:
    for line in f:
        lines.append(list(line.strip()))

max_sum = 0
for line1 in lines:
    for line2 in lines:
        newline = add(line1, line2)
        newline = process(newline)
        mag = magnitude(newline)
        max_sum = max(max_sum, mag)

print(f"The maximum sum of any two numbers is: {max_sum}.")

# -----------------------
# unused binary tree work
# -----------------------

class Node:
    def __init__(self, parent=None, left=None, right=None, value=None):
        self.parent = parent
        self.left = left
        self.right = right
        self.value = value

    def __str__(self):
        if self.value:
            return str(self.value)
        s = '['
        if self.left is not None:
            s += str(self.left)
        s += ','
        if self.right is not None:
            s += str(self.right)
        s += ']'
        return s


def create_tree(line):
    head = Node(None, None, None)
    curr = head
    for char in line:
        if char == "[":
            curr.left = Node(parent=curr)
            curr.right = Node(parent=curr)
            curr = curr.left
        elif char == ",":
            # Switch over to the right side
            curr = curr.parent.right
        elif char == "]":
            # Go up a level
            curr = curr.parent
        else:
            # It is a number
            curr.value = int(char)
    return head


line = "[[1,2],3]"
line = "[[[[[9,8],1],2],3],4]"

tree = create_tree(line)
