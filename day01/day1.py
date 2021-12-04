print("--- DAY 1 ---")
print("--- PART 1 ---")

count = 0

with open('input.txt') as f:
    # Get the first measurement
    prev_val = int(f.readline())
    # Now start iterating through the measurements
    for line in f:
        val = int(line)
        if val > prev_val:
            count += 1
        prev_val = val
print(f"The depth increased {count} times.")

print("--- PART II ---")
count = 0
with open('input.txt') as f:
    # Now start iterating through the measurements,
    # keeping track of the location
    # [0, 1, 2] compared to [1, 2, 3]
    # This means we only need to compare 3 to 0 since the
    # middle values are shared, so we don't even need to sum here.
    # Ring buffer?
    val0 = int(f.readline())
    val1 = int(f.readline())
    val2 = int(f.readline())
    for line in f:
        val = int(line)
        # We want to compare the new value to the oldest one
        if val > val0:
            count += 1
        # Now rotate our values out
        val0 = val1
        val1 = val2
        val2 = val

print(f"The depth increased {count} times.")
