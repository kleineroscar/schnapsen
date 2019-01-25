"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""

# Import the API objects
from api import State
import datetime
import random
from math import log, sqrt

class Bot:

    __states = [] # type : tuple(state)
    __calc_time = 4 # type : int
    __max_moves = 100 # type : int
    __wins = {}
    __plays = {}
    __max_depth = 0
    __C = 1.4 # larger values will encourage more exploration of the possibilies

    def __init__(self, **kwargs):
        self.__states = []
        self.__calc_time = datetime.timedelta(seconds = kwargs.get('time', 4))
        self.__max_moves = kwargs.get('max_moves', 100)
        self.__wins = {}
        self.__plays = {}
        self.__C = kwargs.get('C', 1.4)

    def get_move(self, state):
        # type: (State) -> tuple[int, int]
        self.__states.append(state)
        self.__max_depth = 0
        last_state = self.__states[-1]
        player = last_state.whose_turn()
        moves = last_state.moves()

        if not moves:
            return
        if len(moves) == 1:
            return moves[0]

        games = 0

        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.__calc_time:
            self.run_sim()
            games += 1

        moves_states = [(m, last_state.next(m)) for m in moves]

        print(games, datetime.datetime.utcnow() - begin)

        percent_wins, move = max(
            (self.__wins.get((player, S), 0) /
             self.__plays.get((player, S), 1),
            m)
            for m, S in moves_states
        )

        for x in sorted(
            ((100 * self.__wins.get((player, S), 0) /
              self.__plays.get((player, S), 1),
              self.__wins.get((player, S), 0),
              self.__plays.get((player, S), 0), m)
            for m, S in moves_states),
            reverse=True
        ):
            print("{3}: {0:.2f}% ({1} / {2})").format(*x)

        print("Maximum depth searched: ", self.__max_depth)
        # Return a random choice
        return move

    def run_sim(self):
        plays, wins = self.__plays, self.__wins

        visited_states = set()
        states_copy = self.__states[:]
        last_state = states_copy[-1]
        player = last_state.whose_turn()

        expand = True
        for i in range(1, self.__max_moves + 1):
            moves_states = [(move, last_state.next(move)) for move in last_state.moves()]

            if all(plays.get((player, S)) for move, S in moves_states):
                log_total = log(
                    sum(plays[(player, S)] for move, S in moves_states))
                value, move, last_state = max(
                    ((wins[(player, S)] / plays[(player, S)]) +
                     self.__C * sqrt(log_total / plays[(player, S)]), move, S)
                    for move, S in moves_states
                )
            else:
                move, state = random.choice(moves_states)

            # move = random.choice(legal)
            # last_state = last_state.next(move)
            states_copy.append(last_state)

            if expand and (player, last_state) not in plays:
                expand = False
                plays[(player, last_state)] = 0
                wins[(player, last_state)] = 0
                if i > self.__max_depth:
                    self.__max_depth = i

            visited_states.add((player, last_state))

            player = last_state.whose_turn()

            winner = last_state.winner()
            if winner != [None,None]:
                break

        for player, state in visited_states:
            if (player, states_copy) not in plays:
                continue
            plays[(player, states_copy)] += 1
            if player == winner:
                wins[(player, last_state)] += 1
