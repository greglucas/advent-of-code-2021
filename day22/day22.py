print("--- DAY 22 ---")
print("--- PART 1 ---")

steps = list()
with open("input.txt") as f:
    for line in f:
        # Get the "on"/"off" string
        onoff, rest = line.strip().split()
        xs = list()
        for x in rest.split(","):
            # Drop the "x=" portion
            x0, x1 = x[2:].split("..")
            xs.append([int(x0), int(x1)])

        steps.append([onoff, *xs])


class Cube:
    """Storing the bounds of a cube"""
    def __init__(self, xs, ys, zs):
        self.x0 = xs[0]
        self.x1 = xs[1]
        self.y0 = ys[0]
        self.y1 = ys[1]
        self.z0 = zs[0]
        self.z1 = zs[1]

    def intersects(self, cube):
        """Returns whether this cube overlaps or not"""
        # If any of these bounds are past the opposite left/right
        # of their respective axes, then it won't overlap
        if (cube.x1 < self.x0 or cube.x0 > self.x1
            or cube.y1 < self.y0 or cube.y0 > self.y1
            or cube.z1 < self.z0 or cube.z0 > self.z1):
                return False
        return True

    def get_intersection(self, cube):
        """Returns the intersecting cube"""
        # max choice of the left edges
        # min choice of the right edges
        xs = max(self.x0, cube.x0), min(self.x1, cube.x1)
        ys = max(self.y0, cube.y0), min(self.y1, cube.y1)
        zs = max(self.z0, cube.z0), min(self.z1, cube.z1)
        return Cube(xs, ys, zs)

    def volume(self):
        """Calculate the volume of this cube"""
        return ((self.x1 - self.x0 + 1)
                * (self.y1 - self.y0 + 1)
                * (self.z1 - self.z0 + 1))

# Go through each step and create new cubes based on overlaps
# 1) overalpping "on", then we want to add an "off"
#    cube with the overlapping volume to it which will reduce the overall
#    area
# 2) overlapping "off" cubes, then we continue on, as we don't want to
#    double count off regions
# 3) on/off cubes

# Keep track of our on/off cubes as we move along
on_cubes = list()
off_cubes = list()

for step in steps[:20]:
    onoff = step[0]
    cube = Cube(*step[1:])
    # print("STEPS:", cube.volume())
    new_on_cubes = list()
    new_off_cubes = list()

    # Go through the list of cubes we have that are on
    for on_cube in on_cubes:
        if cube.intersects(on_cube):
            # We don't want to double count the "on", so
            # add an "off" cube at the intersection
            # We want to turn off the currently on lights
            c = cube.get_intersection(on_cube)
            new_off_cubes.append(c)

    # Go through the list of cubes we have that are off
    for off_cube in off_cubes:
        if cube.intersects(off_cube):
            # We don't want to double count the "on", so
            # add an "off" cube at the intersection
            # We don't want to double count the off cubes
            c = cube.get_intersection(off_cube)
            new_on_cubes.append(c)

    # Add our full on cube to the list
    # The off cube was handled via intersections and shouldn't be added
    # to any lists
    if onoff == "on":
        on_cubes.append(cube)

    for c in new_on_cubes:
        on_cubes.append(c)
    for c in new_off_cubes:
        off_cubes.append(c)

total_volume = 0
for c in on_cubes:
    total_volume += c.volume()
for c in off_cubes:
    total_volume -= c.volume()

print(f"The total volume of on cubes is {total_volume}")

print("--- DAY 22 ---")
print("--- PART 2 ---")

on_cubes = list()
off_cubes = list()

for step in steps:
    onoff = step[0]
    cube = Cube(*step[1:])
    # print("STEPS:", cube.volume())
    new_on_cubes = list()
    new_off_cubes = list()

    # Go through the list of cubes we have that are on
    for on_cube in on_cubes:
        if cube.intersects(on_cube):
            # We don't want to double count the "on", so
            # add an "off" cube at the intersection
            # We want to turn off the currently on lights
            c = cube.get_intersection(on_cube)
            new_off_cubes.append(c)

    # Go through the list of cubes we have that are off
    for off_cube in off_cubes:
        if cube.intersects(off_cube):
            # We don't want to double count the "on", so
            # add an "off" cube at the intersection
            # We don't want to double count the off cubes
            c = cube.get_intersection(off_cube)
            new_on_cubes.append(c)

    # Add our full on cube to the list
    # The off cube was handled via intersections and shouldn't be added
    # to any lists
    if onoff == "on":
        on_cubes.append(cube)

    for c in new_on_cubes:
        on_cubes.append(c)
    for c in new_off_cubes:
        off_cubes.append(c)

total_volume = 0
for c in on_cubes:
    total_volume += c.volume()
for c in off_cubes:
    total_volume -= c.volume()

print(f"The total volume of on cubes is {total_volume}")
