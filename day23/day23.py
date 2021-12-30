print("--- DAY 23 ---")
print("--- PART 1 ---")

with open("input.txt") as f:
    # Blanks
    f.readline()
    hallway = f.readline().strip().strip("#")
    first_row = f.readline().strip().strip("#").split("#")
    second_row = f.readline().strip().strip("#").split("#")

class Letter:
    def __init__(self, letter, loc):
        """Keep track of the number of moves for a letter"""
        self.letter = letter
        self.loc = loc
        self.nmoves = 0

    def copy(self):
        newletter = Letter(self.letter, loc=self.loc)
        newletter.nmoves = self.nmoves
        return newletter

# Keep track of the Amphipod locations on a board
nrows = 4
class Board:
    def __init__(self):
        self.board = [[None for i in range(nrows + 1)] for j in range(11)]
        #C#A#B#D#
        #D#C#B#A#
        #D#B#A#C#
        #D#C#A#B#
        # PART 2
        self.letters = [Letter("C", (2, 1)), Letter("A", (4, 1)),
                        Letter("B", (6, 1)), Letter("D", (8, 1)),
                        # Second row
                        Letter("D", (2, 2)), Letter("C", (4, 2)),
                        Letter("B", (6, 2)), Letter("A", (8, 2)),
                        # Third row
                        Letter("D", (2, 3)), Letter("B", (4, 3)),
                        Letter("A", (6, 3)), Letter("C", (8, 3)),
                        # Fourth row
                        Letter("D", (2, 4)), Letter("C", (4, 4)),
                        Letter("A", (6, 4)), Letter("B", (8, 4)),

        ]

        # PART 1
        # self.letters = [Letter("C", (2, 1)), Letter("A", (4, 1)),
        #                 Letter("B", (6, 1)), Letter("D", (8, 1)),
        #                 # Second row
        #                 Letter("D", (2, 2)), Letter("C", (4, 2)),
        #                 Letter("A", (6, 2)), Letter("B", (8, 2)),
        # ]
        for letter in self.letters:
            self.board[letter.loc[0]][letter.loc[1]] = letter


        # TEST CASE
        # self.board[2][1] = Letter("B", (2, 1))
        # self.board[2][2] = Letter("A", (2, 2))
        # # B slot
        # self.board[4][1] = Letter("C", (4, 1))
        # self.board[4][2] = Letter("D", (4, 2))
        # # C slot
        # self.board[6][1] = Letter("B", (6, 1))
        # self.board[6][2] = Letter("C", (6, 2))
        # # D slot
        # self.board[8][1] = Letter("D", (8, 1))
        # self.board[8][2] = Letter("A", (8, 2))

        self.energy = 0

        self.multiplier = {"A": 1, "B": 10, "C": 100, "D": 1000}
        self.desired_col = {"A": 2, "B": 4, "C": 6, "D": 8}

    def __str__(self):
        lines = []
        line0 = "#"*13
        lines.append(line0)
        line1 = "".join("." if x[0] is None else x[0].letter for x in self.board)
        line1 = "#" + line1 + "#"
        lines.append(line1)

        for i in range(1, nrows+1):

            line2 = "".join("#" if x[i] is None else x[i].letter for x in self.board)
            line2 = "#" + line2 + "#"
            lines.append(line2)
        line3 = "  " + "#"*9 + "  "
        lines.append(line3)
        return "\n".join(lines)

    def copy(self):
        newboard = Board()
        newboard.board = [[None for i in range(5)] for j in range(11)]
        newboard.letters = [letter.copy() for letter in self.letters]
        for letter in newboard.letters:
            newboard.board[letter.loc[0]][letter.loc[1]] = letter
        newboard.energy = self.energy
        return newboard

    def move(self, loc, pos):
        """Move amphipod from `loc` to `pos`."""
        # if not self.can_move(loc, pos):
        #     return
        # Move the piece
        self.board[pos[0]][pos[1]] = letter = self.board[loc[0]][loc[1]]
        self.board[loc[0]][loc[1]] = None
        # Update the letter position
        letter.loc = tuple((pos[0], pos[1]))

        # Add the energy cost for this move
        cost = abs(pos[0] - loc[0]) + abs(pos[1] - loc[1])
        self.energy += self.multiplier[letter.letter]*cost

        # Increment the count of the letter
        letter.nmoves += 1

    def undo_move(self, loc, pos):
        """Undo the move from `loc` to `pos`."""
        # Move the piece
        self.board[loc[0]][loc[1]] = letter = self.board[pos[0]][pos[1]]
        self.board[pos[0]][pos[1]] = None
        # Update the letter position
        letter.loc = tuple((loc[0], loc[1]))

        # Add the energy cost for this move
        cost = abs(loc[0] - pos[0]) + abs(loc[1] - pos[1])
        self.energy -= self.multiplier[letter.letter]*cost

        # Decrement the count of the letter
        letter.nmoves -= 1

    def can_move(self, loc, pos):
        letter = self.board[loc[0]][loc[1]]
        if letter is None:
            # There isn't an amphipod starting here
            return False
        if letter.nmoves >= 2:
            # Each amphipod can only move twice (once to hallway and once back)
            return False
        if loc[1] == 0 and pos[1] == 0:
            # In the hallway already, so can't move in it again
            return False
        if pos[1] == 0 and pos[0] in (2, 4, 6, 8):
            # Immediately outside a room is not allowed
            return False
        if pos[1] > 0 and pos[0] != self.desired_col[letter.letter]:
            # This isn't the destination for this amphipod
            return False
        # Now iterate over the spots between the dest and loc
        # to see if there is another Amphipod there
        # x
        for i in range(min(loc[0], pos[0]), max(loc[0], pos[0])+1):
            if i == loc[0]:
                # Ignore our current position
                continue
            if self.board[i][0] is not None:
                return False
        # y
        # posx constrains the horizontal coordinate depending on
        # whether we started in the hallway or a column
        posx = pos[0] if loc[1] == 0 else loc[0]
        if loc[1] == 0:
            # Started in a hallway, so check the entire stack up to the
            # position we want to go to
            ilocs = list(range(1, pos[1]+1))
        else:
            # Started in a column
            ilocs = list(range(1, loc[1]+1))
        for i in ilocs:
            if i == loc[1]:
                # Ignore our current position
                continue
            if self.board[posx][i] is not None:
                return False

        return True

    def is_solved(self):
        try:
            for col, letter in zip([2, 4, 6, 8], ["A", "B", "C", "D"]):
                for i in range(1, nrows+1):
                    if self.board[col][i].letter != letter:
                        return False

        except AttributeError:
            # Nonetype means it isn't completely filled
            return False
        return True


board = Board()
# Keep track of the order we want to search in, going out from the middle
# which will hopefully speed up the search by getting the result sooner
# and being able to ignore some end points
hall_order = [5, 3, 7, 1, 9, 0, 10]

def recurse(board, loc, pos, min_energy=200000):
    """Recursively try to move the pieces of the board around."""
    if board.energy >= min_energy:
        return min_energy
    if not board.can_move(loc, pos):
        return min_energy

    # print(board)
    
    # Make this move
    board.move(loc, pos)
    if board.is_solved():
        # print("SOLVED:", board.energy)
        # Store energy for the return before the undo move
        energy = board.energy
        # Undo the move before we exit
        board.undo_move(loc, pos)
        return energy

    # Now recursively call new board moves
    for letter in board.letters:
        if letter.nmoves >= 2:
            # We have already moved this letter as many times as possible
            continue
        # Recursively move each letter
        if letter.loc[1] == 0:
            # We are in the hallway, only check for placement in the slots
            # it can actually go to
            col = board.desired_col[letter.letter]
            rows = list(range(1, nrows+1))
            all_clear = True
            for row in rows:
                if getattr(board.board[col][row], "letter", letter.letter) != letter.letter:
                    # There is a different letter in this row
                    all_clear = False
            if not all_clear:
                # If we found a bad spot, continue on with our other letters
                continue
            # Now iterate through from the bottom to test placements
            i = nrows
            while i > 0:
                if board.board[col][i] is None:
                    outcome = recurse(board, letter.loc, (col, i), min_energy)
                    break
                i -= 1
            min_energy = min(min_energy, outcome)
        else:
            # We are in a slot
            # Make sure we can get out of the slot
            col = board.desired_col[letter.letter]
            rows = list(range(1, loc[1]))
            all_clear = True
            for row in rows:
                if board.board[loc[0]][row] is not None:
                    # There is a letter in this row
                    all_clear = False
            if not all_clear:
                # If we found a bad spot, continue on with our other letters
                continue
            # test all hallway positions
            for ii in hall_order:
                if board.board[ii][0] is not None:
                    # Something else is already there, so don't bother checking
                    continue
                outcome = recurse(board, letter.loc, (ii, 0), min_energy=min_energy)
                min_energy = min(min_energy, outcome)

    # Undo the move before we exit
    board.undo_move(loc, pos)
    return min_energy


min_energy = 200000
# Only consider the first 4 elements since those are the ones that can move
for letter in board.letters[:4]:
    for ii in hall_order:
        print(f"Testing Letter {letter.letter}, {ii}: {min_energy}")
        outcome = recurse(board, letter.loc, (ii, 0), min_energy=min_energy)
        min_energy = min(min_energy, outcome)
print(min_energy)


print("--- DAY 23 ---")
print("--- PART 2 ---")
