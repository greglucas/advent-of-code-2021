print("--- DAY 20 ---")
print("--- PART 1 ---")

algorithm = []
grid = []

with open("input.txt") as f:
    algorithm = f.readline().strip().replace(".", "0").replace("#", "1")
    # algorithm = [int(x) for x in algorithm]
    f.readline()

    # Read in the grid
    for line in f:
        row = [x for x in line.strip().replace(".", "0").replace("#", "1")]
        grid.append(row)


# Fill out a mapping of pixels
# 0, 1, 2
# 3, 4, 5
# 6, 7, 8


def convolution(grid, step):
    """Apply a 3x3 convolution filter to the input grid"""
    newgrid = []
    def lookup(grid, i, j, step):
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]):
            # The infinite components could jump back and forth between
            # all ones and all zeros
            return algorithm[0] if step % 2 == 0 else algorithm[-1]
        return grid[i][j]

    # i and j keep track of the center location we
    # are interested in
    newgrid = []
    n_extend = 2
    for i in range(-n_extend, len(grid) + n_extend):
        row = []
        for j in range(-n_extend, len(grid[0]) + n_extend):

            # locs keeps track of the 0-9 locations of the filter
            locs = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1), (0, 0), (0, 1),
                    (1, -1), (1, 0), (1, 1)]
            s = "0b"
            for ii, jj in locs:
                s += lookup(grid, i+ii, j+jj, step=step)

            # Now lookup the value in the algorithm
            row.append(algorithm[int(s, 2)])
        newgrid.append(row)
    return newgrid


def print_grid(grid):
    for row in grid:
        print("".join(row).replace("1", "#").replace("0", "."))


n_enhance = 2
for i in range(n_enhance):
    grid = convolution(grid, i+1)

# print_grid(grid)

lit_pixels = sum(x.count("1") for x in grid)
print(f"There are {lit_pixels} light pixels in the image after 2 enhancements.")

print("--- DAY 20 ---")
print("--- PART 2 ---")

# Already done 2 of them
n_enhance = 48
for i in range(n_enhance):
    grid = convolution(grid, i+1)

lit_pixels = sum(x.count("1") for x in grid)
print(f"There are {lit_pixels} light pixels in the image after 50 enhancements.")
