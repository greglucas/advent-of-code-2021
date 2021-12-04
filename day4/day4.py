print("--- DAY 4 ---")
print("--- PART 1 ---")

with open('input.txt') as f:
    draws = [int(x) for x in f.readline().strip().split(',')]

    # Now read in each board
    def read_board(in_file):
        """
        Reads a bingo board from the input file and returns
        it as a 5x5 list of lists.
        """
        board = []
        for _ in range(5):
            line = [int(x) for x in f.readline().split()]
            # Add this line to the board
            board += [line]
        return board

    boards = []
    while f.readline():
        board = read_board(f)
        boards += [board]

print(f"There are {len(boards)} bingo boards.")


def check_board(board, number_set):
    """
    Checks a bingo board for a win given the drawn numbers.
    """
    row_valid = [True]*5
    col_valid = [True]*5
    for i in range(5):
        for j in range(5):
            if board[i][j] not in number_set:
                # O(1) lookup
                row_valid[i] = False
                col_valid[j] = False
    
    if any(row_valid) or any(col_valid):
        return True
    return False


winning_board = None
# We know you can't win with less than 5 draws, so start there
current_draw = 5
while winning_board is None and current_draw < len(draws):
    # Iterate through the draws checking each board for wins
    numbers_called = set(draws[:current_draw])
    for i, board in enumerate(boards):
        if check_board(board, numbers_called):
            winning_board = i
    current_draw += 1

# We still incremented current_draw within the while loop
current_draw -= 1
# Now we need to find out the uncalled numbers on the board
called_numbers = set(draws[:current_draw])
drawn_number = draws[current_draw-1]
board = boards[winning_board]


def sum_uncalled(board, numbers_called):
    """
    Sum up all of the uncalled numbers.
    """
    total = 0
    for i in range(5):
        for j in range(5):
            if board[i][j] not in called_numbers:
                total += board[i][j]
    return total


print(f"The winning board is number {winning_board}, "
      f"on draw number {current_draw}, with value {drawn_number}.")
result = drawn_number*sum_uncalled(board, called_numbers)
print(f"The winning score is: {result}")

print("--- DAY 4 ---")
print("--- PART 2 ---")

losing_board = None
# Keep our current_draw from last time as a starting point
# Initialize all boards to False
winning_boards = [False]*len(boards)
while not all(winning_boards) and current_draw < len(draws):
    # Iterate through the draws checking each board for wins
    numbers_called = set(draws[:current_draw])
    for i, board in enumerate(boards):
        if winning_boards[i]:
            # This board has already won, so no need to check it again
            continue
        if check_board(board, numbers_called):
            winning_boards[i] = True
            losing_board = i
    current_draw += 1

# We still incremented current_draw within the while loop
current_draw -= 1
# Now we need to find out the uncalled numbers on the board
called_numbers = set(draws[:current_draw])
drawn_number = draws[current_draw-1]
board = boards[losing_board]

print(f"The losing board is number {losing_board}, "
      f"on draw number {current_draw}, with value {drawn_number}.")
result = drawn_number*sum_uncalled(board, called_numbers)
print(f"The winning score is: {result}")
