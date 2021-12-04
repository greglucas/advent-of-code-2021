print("--- DAY 2 ---")
print("--- PART 1 ---")

# horizontal, depth
position = [0, 0]

with open('input.txt') as f:
    # Now start iterating through the directions
    for line in f:
        direction, val = line.split()
        val = int(val)
        if direction == 'forward':
            position[0] += val
        else:
            if direction == 'up':
                # Depth is actually decreasing here
                val *= -1
            position[1] += val


print(f"The submarine is at position {position}, multiplied to give: "
      f"{position[0]*position[1]}.")

print("--- PART II ---")

# horizontal, depth, aim
position = [0, 0, 0]
with open('input.txt') as f:
    # Now start iterating through the directions
    for line in f:
        direction, val = line.split()
        val = int(val)
        if direction == 'forward':
            position[0] += val
            # Change depth based on the aim
            position[1] += val * position[2]
        else:
            if direction == 'up':
                # Aim is actually decreasing here
                val *= -1
            # Modify the aim this time
            position[2] += val

print(f"The submarine is at position {position}, multiplied to give: "
      f"{position[0]*position[1]}.")
