
print("--- DAY 17 ---")
print("--- PART 1 ---")

with open("input.txt") as f:
    line = f.readline().strip()
    x0, x1 = int(line[15:18]), int(line[20:23])
    y0, y1 = int(line[27:30]), int(line[32:35])

# x0, x1 = 20, 30
# y0, y1 = -10, -5


def step(x, y, vx, vy):
    x += vx
    y += vy
    if vx > 0:
        vx -= 1
    elif vx < 0:
        vx += 1
    vy -= 1
    return x, y, vx, vy


def process_steps(vx, vy):
    """Test this initial vx, vy"""
    x, y = 0, 0
    maxy = 0
    while y > y0:
        # Keep iterating if we are over the bottom row
        x, y, vx, vy = step(x, y, vx, vy)
        maxy = max(maxy, y)
        if  x0 <= x <= x1 and y0 <= y <= y1:
            # Successful velocity
            return True, maxy
    return False, 0


# Brute force approach
maxv = (0, 0)
maxy = 0
for vx in range(100):
    for vy in range(100):
        _, y = process_steps(vx, vy)
        if y > maxy:
            maxv = (vx, vy)
            maxy = y

print(f"Maximum height reached is {maxy} with an initial velocity of {maxv}")

print("--- DAY 17 ---")
print("--- PART 2 ---")

# Brute force approach
vs = list()
for vx in range(0, 300):
    for vy in range(-100, 200):
        success, y = process_steps(vx, vy)
        if success:
            vs.append((vx, vy))

print(f"The number of possiblilities is {len(vs)}.")
