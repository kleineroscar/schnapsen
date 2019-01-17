"""
Check that the minmax bot and alpha beta bot return the same judgement, and that alphabeta bot is faster

"""

from api import State, util
import random, time

from bots.alphabeta import alphabeta
from bots.alphabetav2 import alphabetav2

REPEATS = 3
DEPTH = 4

ab = alphabeta.Bot(randomize=False, depth=DEPTH)
abv2 = alphabetav2.Bot(randomize=False, depth=DEPTH)

abv2_time = 0
ab_time = 0

# Repeat
for r in range(REPEATS):
    
    # Repeat some more 
    for r2 in range(REPEATS):

        # Generate a starting state
        state = State.generate(phase=2)

        # Ask both bots their move
        # (and time their responses)

        start = time.time()
        abv2_move = abv2.get_move(state)
        abv2_time += (time.time() - start)

        start = time.time()
        ab_move = ab.get_move(state)
        ab_time += (time.time() - start)


        if abv2_move != ab_move:
            print('Difference of opinion! Alphabetav2 said: {}, alphabeta said: {}. State: {}'.format(abv2_move, ab_move, state))
        else:
            print('Agreed.')

print('Done. time Alphabetav2: {}, time Alphabeta: {}.'.format(abv2_time / REPEATS, ab_time / REPEATS))
print('Alphabetav2 speedup: {} '.format(ab_time / abv2_time))

