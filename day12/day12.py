print("--- DAY 12 ---")
print("--- PART 1 ---")

# Store the paths as a dictionary lookup
paths = {}
with open('input.txt') as f:
    for line in f:
        start, end = line.strip().split('-')
        if start not in paths:
            paths[start] = []
        if end not in paths:
            paths[end] = []
        paths[start] += [end]
        paths[end] += [start]


def traverse(node, visited=[]):
    """Walk the structure recursively, keeping track of the paths we've visited"""
    # Try to add the nodes that this one touches to the path list
    # then we will recurse all of them after that
    if node.islower() and node in visited:
        # Remove this path since it isn't viable
        return []
    # Add this as a visited node
    visited += [node]
    if node == 'end':
        return visited
    new_paths = list()
    for to_node in paths[node]:
        out = traverse(to_node, list(visited))
        if out is None or len(out) == 0:
            # This was a dead end
            continue
        new_paths += [out]
        
    return new_paths

full_list = traverse('start')


def unwrap(x, actual_paths):
    """
    Unwrap our nested list of lists with paths in them at
    the lowest level of the list.
    """

    if isinstance(x, str):
        return []
    if isinstance(x, list) and len(x) > 1 and isinstance(x[0], str):
        actual_paths += [x]
        return actual_paths
    
    for xx in x:
        actual_paths = unwrap(xx, list(actual_paths))
    return actual_paths

actual_paths = unwrap(full_list, [])
# for x in actual_paths:
#     print(x)
print(f"There are {len(actual_paths)} unique paths from start to end.")

print("--- DAY 12 ---")
print("--- PART 2 ---")
print("Warning, this takes some time with the current implementation.")


def traverse2(node, visited=[], all_paths=[]):
    """Walk the structure recursively, keeping track of the paths we've visited"""
    # Try to add the nodes that this one touches to the path list
    # then we will recurse all of them after that
    if node.islower() and node in visited:
        if node == 'start':
            return all_paths
        for x in visited:
            if sum([x == y for y in visited if y.islower()]) == 2:
                # Remove this path since we've already
                # visited a lower-case node twice
                return all_paths

    # Add this as a visited node
    visited += [node]
    if node == 'end':
        all_paths += [visited]
        return all_paths
    for to_node in paths[node]:
        all_paths = traverse2(to_node, list(visited), list(all_paths))

    return all_paths

full_list = traverse2('start')
print(f"There are {len(full_list)} unique paths from start to end allowing "
       "for some duplicates.")
