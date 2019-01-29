"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""

import datetime
import random
from math import log, sqrt

# Import the API objects
from api import State


class Bot:
    __states = []  # type : tuple(state)
    __calc_time = 3.5  # type : int
    __max_moves = 10  # type : int
    __wins = {}
    __plays = {}
    __max_depth = 0
    __complexity = 1.4  # larger values will encourage more exploration of the possibilies
    __moves_states = {}
    # __visited_states = set()
    __avg_move_time = 0
    __total_moves = 0
    __avg_sims = 0
    __total_sims = 0

    def __init__(self, **kwargs):
        self.__states = []
        self.__calc_time = datetime.timedelta(seconds=kwargs.get('time', 3.5))
        self.__max_moves = kwargs.get('max_moves', 10)
        self.__wins = {}
        self.__plays = {}
        self.__complexity = kwargs.get('C', 1.4)

    def get_move(self, state):
        # type: (State) -> tuple[int, int]
        new_state = state.make_assumption() if state.get_phase() == 1 else state
        self.__states.append(new_state)
        # self.__max_depth = 0
        last_state = self.__states[-1]
        player = last_state.whose_turn()
        moves = last_state.moves()
        self.__total_moves += 1

        if not moves:
            return
        if len(moves) == 1:
            return moves[0]

        games = 0

        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.__calc_time:
            self.run_sim()
            games += 1

        self.__total_sims += 1
        self.__avg_sims = self.__avg_sims * (
            self.__total_sims - 1) / self.__total_sims + (
                              games / self.__total_sims)

        self.__moves_states = [(m, last_state.next(m)) for m in moves]

        move_time = datetime.datetime.utcnow() - begin
        self.__avg_move_time = self.__avg_move_time * (
            self.__total_moves - 1) / self.__total_moves + (
                                   move_time.total_seconds() / self.__total_moves)

        print(games, move_time)

        # percent_wins, move = self.percent_max(player)
        percent_wins, move = max(
            ((self.__wins.get((player, S), 0) /
             self.__plays.get((player, S), 1),
             p)
            for p, S in self.__moves_states), key=lambda x: x[0]
        )

        # for m,S in self.__moves_states:
        #     percentage = 100 * self.__wins.get((player, S), 0) / self.__plays.get((player, S), 1)
        #     wins = self.__wins.get((player, S), 0)
        #     plays = self.__plays.get((player, S), 0)
        #     print(str(plays) + ": " + str(percentage).format(".2f") + " (" + str(wins) + "/" + str(plays) + ")")
        #
        # Return a random choice
        return move

    def run_sim(self):
        states_copy = self.__states[:]
        last_state = states_copy[-1]
        player = last_state.whose_turn()
        visited_states = set()
        plays = self.__plays
        wins = self.__wins
        # last_state = last_state.make_assumption()

        expand = True
        for i in range(1, self.__max_moves + 1):
            self.__moves_states = [(move, last_state.next(move)) for move in
                                   last_state.moves()]

            if all(plays.get((player, S)) for move, S in
                   self.__moves_states):
                log_total = log(
                    sum(plays[(player, S)] for move, S in
                        self.__moves_states))
                # value, move, last_state = self.value_max(player, log_total, wins, plays)
                value, move, last_state = max(
                    (((wins[(player, S)] / plays[(player, S)]) +
                     self.__complexity * sqrt(log_total / plays[(player, S)]), m, S)
                    for m, S in self.__moves_states), key=lambda x: x[0]
                )
            else:
                move, last_state = random.choice(self.__moves_states)

            # move = random.choice(legal)
            # last_state = last_state.next(move)
            states_copy.append(last_state)

            if expand and (player, last_state) not in plays:
                expand = False
                plays[(player, last_state)] = 0
                wins[(player, last_state)] = 0
                if i > self.__max_depth:
                    print("changed max depth to " + str(self.__max_depth))
                    self.__max_depth = i

            visited_states.add((player, last_state))

            player = last_state.whose_turn()
            winner = states_copy[-1].winner()
            if winner[0] is not None:
                break

        for v_player, v_state in visited_states:
            if (v_player, v_state) not in plays:
                continue
            plays[(v_player, v_state)] += 1
            if v_player == winner[0]:
                wins[(v_player, v_state)] += 1

    def value_max(self, player, log_total, wins, plays):
        best_combo = (-1, None, None)
        for m, S in self.__moves_states:
            value = ((wins[(player, S)] / plays[(player, S)]) +
                     self.__complexity * sqrt(
                    log_total / plays[(player, S)]))
            if value > best_combo[0]:
                best_combo = (value, m, S)
        return best_combo

    def percent_max(self, player):
        best_percent_combo = (-1, None)
        for m, S in self.__moves_states:
            percent = self.__wins.get((player, S), 0) / self.__plays.get(
                (player, S), 1)
            if percent > best_percent_combo[0]:
                best_percent_combo = (percent, m)
        return best_percent_combo

    def debug(self):
        rep = ''
        rep += 'calc time: ' + str(self.__calc_time)
        rep += '\nmax moves: ' + str(self.__max_moves)
        # rep += '\nwins: ' + str(len(self.__wins))
        # rep += '\nplays: ' + str(len(self.__plays))
        rep += '\nmax depth: ' + str(self.__max_depth)
        rep += '\ncomplexity: ' + str(self.__complexity)
        rep += '\nmoves states length: ' + str(len(self.__moves_states))
        rep += '\nstates length: ' + str(len(self.__states))
        # rep += '\nvisited states length: ' + str(len(self.__visited_states))
        rep += '\navg move time: ' + str(self.__avg_move_time)
        rep += '\navg sims: ' + str(self.__avg_sims)
        print(rep)
