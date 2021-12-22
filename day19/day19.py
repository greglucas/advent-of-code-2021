print("--- DAY 19 ---")
print("--- PART 1 ---")

def rotation_list():
    rot_list = list()
    for i in (1, -1):
        for j in (1, -1):
            for k in (1, -1):
                rot_list.append(((i, j, k), (0, 1, 2)))
                rot_list.append(((i, j, k), (1, 2, 0)))
                rot_list.append(((i, j, k), (2, 0, 1)))
                rot_list.append(((i, j, k), (0, 2, 1)))
                rot_list.append(((i, j, k), (1, 0, 2)))
                rot_list.append(((i, j, k), (2, 1, 0)))
    return rot_list


def vector_diff(p0, p1):
    """Returns the vector difference between two points"""
    return tuple(p1[k] - p0[k] for k in range(3))


class Scanner:
    """Stores information about each scanner."""

    def __init__(self):
        self.orig_beacons = list()
        self.loc = (0, 0, 0)
        # Orientation of each axes
        self.orientation = (1, 1, 1)
        # Rotation order of the axes
        self.rotation = (0, 1, 2)
        self._beacon_vectors = None
        self.rotation_mapping = rotation_list()
        self.mapping_num = 0

    def beacon_vectors(self):
        """Vectors of the edges from one beacon to another"""
        vs = list()
        for i in range(len(self.beacons)):
            p1 = self.beacons[i]
            sublist = list()
            for j in range(len(self.beacons)):
                p2 = self.beacons[j]
                sublist.append(tuple(p2[k] - p1[k] for k in range(3)))
                
            vs.append(sublist)
        return vs

    def update_mapping(self, num=None):
        """Update the orientation and rotation of this scanner"""
        if num is not None:
            self.mapping_num = num
        self.orientation, self.rotation = self.rotation_mapping[self.mapping_num]
        # Reset the beacons
        beacons = list()
        for beacon in self.orig_beacons:
            # Change the axes orientation
            new_beacon = tuple(self.orientation[i]*beacon[i] for i in range(3))
            # Rotate the scanner axes
            new_beacon = tuple(new_beacon[self.rotation[i]] for i in range(3))
            # Shift this location based on the location of the scanner
            new_beacon = tuple(self.loc[i] + new_beacon[i] for i in range(3))
            beacons.append(new_beacon)
        self.beacons = tuple(x for x in beacons)

    def edges(self):
        """Calculate the edges/vectors between the beacons"""
        # list of list based on the beacons
        vs = list()
        for i in range(len(self.beacons)):
            v1 = list()
            for j in range(len(self.beacons)):
                v = vector_diff(self.beacons[i], self.beacons[j])
                v1.append(v)
            vs.append(v1)
        return vs


scanners = []
with open("input.txt") as f:
    scanner = []
    for line in f:
        if line[:3] == "---":
            # Start a new scanner
            scanner = Scanner()
        elif line == "\n":
            scanner.update_mapping(0)
            scanners.append(scanner)
        else:
            point = tuple(int(x) for x in line.strip().split(","))
            scanner.orig_beacons.append(point)
    # Update the final scanner
    scanner.update_mapping(0)
    scanners.append(scanner)


# Rotate a scanner, then shift so that one of the beacons align, then
# see how many other beacons are also aligned.
def find_scanner_position(s0, s1):
    print("Inside find scanner:", len(s0.beacons), len(s1.beacons))
    for i in range(48):
        for b0 in tuple(s0.beacons):
            for b1 in tuple(s1.beacons):
                # Update the orientation before the subtraction
                s1.loc = (0, 0, 0)
                s1.update_mapping(i)
                s1.loc = tuple(b0[j] - b1[j] for j in range(3))
                # Now update the location with the location shifted
                s1.update_mapping(i)
                
                # How many locations are the same
                count = 0
                for bb1 in s1.beacons:
                    if bb1 in s0.beacons:
                        count += 1
                if count >= 12:
                    # This is the proper orientation
                    return
                # Reset the orientation and location to the original
                s1.loc = (0, 0, 0)
                s1.update_mapping(i)
    # No matches, so reset
    s1.loc = (0, 0, 0)
    s1.update_mapping(0)


master_scanner = Scanner()
master_scanner.orig_beacons = scanners[0].orig_beacons
master_scanner.update_mapping()

scanners_to_consider = scanners[1:]
while len(scanners_to_consider) > 0:
    print("TESTING", len(scanners_to_consider))
    print("Master:", len(master_scanner.beacons))
    s1 = scanners_to_consider.pop(0)
    find_scanner_position(master_scanner, s1)
    if s1.loc == (0, 0, 0):
        print("No match")
        # No matching location was found, so add it back into the list for later
        scanners_to_consider.append(s1)
        # scanners_to_consider.insert(0, s1)
    else:
        print("Good scanner", s1.loc)
        # This scanner was good, so add it's beacons to the master list
        for b in s1.beacons:
            if b in master_scanner.orig_beacons:
                continue
            master_scanner.orig_beacons.append(b)
            master_scanner.update_mapping(0)

print(f"The number of beacons is {len(set(master_scanner.orig_beacons))}")

print("--- DAY 19 ---")
print("--- PART 2 ---")

manhattan_dist = 0
for i, scanner in enumerate(scanners):
    print(f"Scanner {i}: {scanner.loc}")
    for j, scanner1 in enumerate(scanners):
        dist = sum([abs(scanner.loc[k] - scanner1.loc[k]) for k in range(3)])
        manhattan_dist = max(manhattan_dist, dist)

print(f"The largest manhattan distance of scanners is: {manhattan_dist}")


# ------------------------------
# Extra code that I started with
# ------------------------------

# s0 = scanners[0]
# for s1 in scanners[1:]:
#     find_scanner_position(s0, s1)
#     # it wasn't solved for
#     if s1.loc == (0, 0, 0):
#         continue
#     # Otherwise test this one out as well
#     for s2 in scanners[1:]:
#         if s1 is s2:
#             continue
#         find_scanner_position(s1, s2)



# def similar_edges(s0, s1):
#     """Count the number of similar edges"""
#     count = 0
#     v0 = s0.edges()
#     nv0 = len(v0)
#     v1 = s1.edges()
#     nv1 = len(v1)
#     for i in range(nv0):
#         for j in range(nv0):
#             if i == j:
#                 continue
#             for ii in range(nv1):
#                 for jj in range(nv1):
#                     if ii == jj:
#                         continue
#                     if v0[i][j] == v1[ii][jj]:
#                         count += 1
#     return count

# found = False
# i = 0
# while i < 24 and not found:
#     scanners[1].update_mapping(i)
#     nsimilar = similar_edges(scanners[0], scanners[1])
#     if nsimilar >= 12*11:
#         found = True
#     i += 1


# def find_scanner_loc(s0, s1):
#     """Find the scanner location that matches the beacons between scanners."""
#     # The loc needs to be updated by moving an edge (beacon0 - beacon1)
#     # which will place the scanner at that location
#     for b0 in list(s0.beacons):
#         for b1 in list(s1.beacons):
#             # update location of the scanner and beacons
#             # print(b1, b0)
#             s1.loc = tuple(b0[i] - b1[i] for i in range(3))
#             s1.loc = (68,-1246,-43)
#             s1.update_mapping(s1.mapping_num)

#             count = 0
#             for bb0 in s0.beacons:
#                 for bb1 in s1.beacons:
#                     if bb0 == bb1:
#                         count += 1
#                         print(bb0, bb1)
#                         print("SUCCESS", count)
#             # Reset it
#             s1.loc = (0, 0, 0)
#             s1.update_mapping(s1.mapping_num)
#             if count > 11:
#                 print("SUCCESS", count)
#                 return

# print(scanners[1].loc, scanners[1].orientation, scanners[1].rotation)
# find_scanner_loc(scanners[0], scanners[1])
# print(scanners[1].loc, scanners[1].orientation, scanners[1].rotation)



# found = False
# i = 0
# s0 = scanners[0]
# s1 = scanners[1]
# while i < len(s0.beacons) and not found:
#     s1.loc = tuple(-x for x in s1.beacons[i])
#     s1.update_mapping(s1.mapping_num)
#     count = 0
#     for p0 in s0.beacons:
#         for p1 in s1.beacons:
#             print(p0, p1)
#             if p0 == p1:
#                 print("COUNT")
#                 count += 1
#     if count >= 12:
#         print("12 count!")
#         found = True
#     i += 1

# print(s1.loc)
# print(s1.beacons[-1])
# print(scanners[1].orig_beacons)
# print("----")
# print(scanners[1].beacons)

# print(scanners[0].beacons)
# scanners[0].update_mapping(3)
# print(scanners[0].edges())
# def beacon_vectors(s1):
#     """Vectors from one beacon to another."""
#     vs = list()
#     for i in range(len(s1)):
#         p1 = s1[i]
#         sublist = list()
#         for j in range(len(s1)):
#             p2 = s1[j]
#             sublist.append(tuple(p2[k] - p1[k] for k in range(3)))
            
#         vs.append(sublist)

#     return vs


# def combos(p):
#     """Return all of the possible combinations of this point."""
#     points = list()
#     for i in (-1, 1):
#         for j in (-1, 1):
#             for k in (-1, 1):
#                 p0 = (i*p[0], j*p[1], k*p[2])
#                 p1 = (j*p[1], k*p[2], i*p[0])
#                 p2 = (k*p[2], i*p[0], j*p[1])
#                 points.append(p0)
#                 points.append(p1)
#                 points.append(p2)
#     return points


# def orientation(p, num):
#     """Return a specific orientation of the point"""
#     return combos(p)[num]


# v0 = beacon_vectors(scanners[0])
# v1 = beacon_vectors(scanners[1])

# beacon_vectors produces a square matrix of vector distances
# from A -> B
# We want to see which beacon vectors are the same in scanner
# one as scanner two. We also need to allow for the rotation of
# scanner two.
# def same_edges(v0, v1):
#     nv0 = len(v0)
#     nv1 = len(v1)
#     mappings = dict()
#     for i in range(nv0):
#         for j in range(i+1, nv0):
#             b1 = v0[i][j]
#             for ii in range(nv1):
#                 for jj in range(ii+1, nv1):
#                     bb1 = v1[ii][jj]
#                     for vtest in combos(bb1):
#                         if vtest == b1:
#                             if i not in mappings:
#                                 mappings[i] = list()
#                             mappings[i].append(ii)
#                             mappings[i].append(jj)
#                             if j not in mappings:
#                                 mappings[j] = list()
#                             mappings[j].append(ii)
#                             mappings[j].append(jj)

#                             # mappings[(i, j)] = (ii, jj)

#     return mappings


# mappings = same_edges(v0, v1)
# def get_mapping(mappings):
#     final_mapping = dict()
#     for x in mappings:
#         vals = mappings[x]
#         # It has to be the first or second value, so see which
#         # which one is repeated in the latter part of the list
#         if vals[0] in vals[2:]:
#             final_mapping[x] = vals[0]
#         else:
#             final_mapping[x] = vals[1]
#     return final_mapping


# def vector_diff(p0, p1):
#     """Returns the vector difference between two points"""
#     return tuple(p1[k] - p0[k] for k in range(3))


# def transform(s0, s1, mappings):
#     """Turns s1 values into the coordinate system of the s0 scan."""
#     # We need to reorient the sensor, use the mappings to figure out
#     # what the proper orientation needs to be
#     possible_combos = list()
#     for map in mappings:
#         possible_combos2 = list()
#         possible_combos.append(possible_combos2)
#         p0 = s0[map]
#         p1 = s1[mappings[map]]
#         for c in combos(p1):
#             possible_combos2.append(vector_diff(p0, c))
#     for i in range(24):
#         # Check whether all values are the same, all vectors should
#         # be the same if the rotation is correct.
#         if all(x[i] == x[0] for x in possible_combos):
#             return i


# print(len(mappings))
# final_mapping = get_mapping(mappings)
# print(transform(scanners[0], scanners[1], final_mapping))
