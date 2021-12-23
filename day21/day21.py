print("--- DAY 21 ---")
print("--- PART 1 ---")

with open("input.txt") as f:
    pos1 = int(f.readline().split(":")[1].strip())
    pos2 = int(f.readline().split(":")[1].strip())

orig_pos1 = pos1
orig_pos2 = pos2

def roll(dice, pos, score):
    sum_dice = 0
    for i in range(3):
        dice += 1
        # If we are on zero we want 100
        sum_dice += dice % 100
    # Player lands on this space
    pos = (pos + sum_dice) % 10
    score += pos if pos > 0 else 10
    return dice, pos, score


score1 = 0
score2 = 0

dice = 0

p1_turn = True
while score1 < 1000 and score2 < 1000:
    if p1_turn:
        dice, pos1, score1 = roll(dice=dice, pos=pos1, score=score1)
        p1_turn = False
    else:
        dice, pos2, score2 = roll(dice=dice, pos=pos2, score=score2)
        p1_turn = True


print(f"Number of rolls: {dice}")
print(f"Player 1 score: {score1}")
print(f"Player 2 score: {score2}")
print(f"losing score x number of rolls: {dice*min(score1, score2)}")
print("--- DAY 21 ---")
print("--- PART 2 ---")

pos1 = orig_pos1
pos2 = orig_pos2
score1 = 0
score2 = 0

dice = 0


# The number of outcomes for each possible 3-roll universe split
roll_prob = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

# Take one turn
def roll_dirac(pos1, pos2, score1, score2, turn):
    if score1 >= 21:
        return 1, 0
    if score2 >= 21:
        return 0, 1

    # {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
    return_val = [0, 0]
    if turn == "p1":
        turn = "p2"
        for p in roll_prob:
            new_pos1 = (pos1 + p) % 10
            new_score1 = score1
            new_score1 += new_pos1 if new_pos1 > 0 else 10
            out = roll_dirac(new_pos1, pos2, new_score1, score2, turn)
            # Multiply these outcomes by how many universes went this way
            return_val[0] += out[0]*roll_prob[p]
            return_val[1] += out[1]*roll_prob[p]
    else:
        turn = "p1"
        for p in roll_prob:
            new_pos2 = (pos2 + p) % 10
            new_score2 = score2
            new_score2 += new_pos2 if new_pos2 > 0 else 10
            out = roll_dirac(pos1, new_pos2, score1, new_score2, turn)
            # Multiply these outcomes by how many universes went this way
            return_val[0] += out[0]*roll_prob[p]
            return_val[1] += out[1]*roll_prob[p]
    
    return return_val

nwins1, nwins2 = roll_dirac(pos1, pos2, 0, 0, "p1")

print(f"Universe 1 wins {nwins1} times, and universe 2 wins {nwins2} times.")
