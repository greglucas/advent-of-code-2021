print("--- DAY 10 ---")
print("--- PART 1 ---")

closing_chars = {')': 3, ']': 57, '}': 1197, '>': 25137}
rev = {')': '(', ']': '[', '}': '{', '>': '<'}


def process_line(line):
    """Process a line for syntax errors"""
    # Start by putting the items into a list
    stack = []
    for char in line:
        if char in closing_chars:
            # If it is a closing char it needs to match with the final
            # element of the list
            if len(stack) == 0 or rev[char] != stack[-1]:
                return closing_chars[char]
            # It did match, so pop the closing char
            stack.pop()
        else:
            # Append the character to the stack
            stack.append(char)
    # As long as the line didn't close wrong, then ignore it
    return 0


total = 0
with open('input.txt') as f:
    for line in f:
        total += process_line(line.strip())

print(f"The sum of syntax violations is: {total}.")


print("--- DAY 10 ---")
print("--- PART 2 ---")

# Keep track of the opening braces here instead
# of requiring a closing mapping
completion_val = {'(': 1, '[': 2, '{': 3, '<': 4}


def process_line(line):
    """Process a line for syntax errors"""
    # Start by putting the items into a list
    stack = []
    for char in line:
        if char in closing_chars:
            # If it is a closing char it needs to match with the final
            # element of the list
            if len(stack) == 0 or rev[char] != stack[-1]:
                return None
            # It did match, so pop the closing char
            stack.pop()
        else:
            # Append the character to the stack
            stack.append(char)

    # At this point we have a list of characters that haven't been closed
    total = 0
    for char in stack[::-1]:
        total *= 5
        total += completion_val[char]
    return total


totals = []
with open('input.txt') as f:
    for line in f:
        out = process_line(line.strip())
        if out is not None:
            totals.append(out)

totals = sorted(totals)
print(f"The middle completion value is: {totals[len(totals)//2]}.")
