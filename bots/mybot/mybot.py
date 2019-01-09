#!/usr/bin/env python
"""
mybot
"""

# Import the API objects
from api import State, util
import random


class Bot:

  def __init__(self):
    pass

  def get_move(self, state):
    # type: (State) -> tuple[int, int]
    """
    Function that gets called every turn. This is where to implement the strategies.
    Be sure to make a legal move. Illegal moves, like giving an index of a card you
    don't own or proposing an illegal mariage, will lose you the game.
     TODO: add some more explanation
    :param State state: An object representing the gamestate. This includes a link to
        the states of all the cards, the trick and the points.
    :return: A tuple of integers or a tuple of an integer and None,
        indicating a move; the first indicates the card played in the trick, the second a
        potential spouse.
    """
    # All legal moves
    moves = state.moves()

    marriage_jack_exchange = self.check_marriage_jack_exchange(state)

    if (marriage_jack_exchange is not None):
      return marriage_jack_exchange

    if (state.get_phase() == 1):
      if (state.whose_turn() == 1):
        #Phase 1 and lead
        return self.worst_non_trump_card(state)
      else:
        suit = str(state)[-2]
        return self.best_same_suit_card(state, suit)
    else:
      # Phase 2
      if (state.whose_turn() == 1):
        trump_play = self.trump_play(state)
        if (trump_play is not None):
          return trump_play
        return self.best_non_trump_card(state)
      else:
        return self.worst_non_trump_card(state)

    # Return a random choice
    return random.choice(moves)

  def worst_non_trump_card(self, state):
    """
    :param state: A state object
    :return: A move tuple representing the lowest rank non-trump move available
    """

    # All legal moves
    moves = state.moves()
    chosen_move = moves[0]

    highest_suit_moves = []

    #Get all moves which are not trump suit or matching the suit of the enemy's card
    for move in moves:

      if move[0] is not None and util.get_suit(move[0]) != state.get_trump_suit():
        highest_suit_moves.append(move)

    if len(highest_suit_moves) == 0:
      lowest_suit_moves = moves

    # Get move with highest rank available, of the subset that we've narrowed down so far
    for move in highest_suit_moves:
      if move[0] is not None and move[0] % 5 >= chosen_move[0] % 5:
        chosen_move = move

    return chosen_move

  def best_non_trump_card(self, state):
    """
    :param state: A state object
    :return: A move tuple representing the highest rank non-trump move available
    """

    # All legal moves
    moves = state.moves()
    chosen_move = moves[0]

    lowest_suit_moves = []

    #Get all moves which are not trump suit or matching the suit of the enemy's card
    for move in moves:

      if move[0] is not None and util.get_suit(move[0]) != state.get_trump_suit():
        lowest_suit_moves.append(move)

    if len(lowest_suit_moves) == 0:
      lowest_suit_moves = moves

    # Get move with highest rank available, of the subset that we've narrowed down so far
    for move in lowest_suit_moves:
      if move[0] is not None and move[0] % 5 <= chosen_move[0] % 5:
        chosen_move = move

    return chosen_move

  def best_same_suit_card(self, state, suit):
    """
    :param state: A state object
    :return: A move tuple representing the highest rank non-trump move available
    """

    # All legal moves
    moves = state.moves()
    chosen_move = moves[0]

    lowest_suit_moves = []

    #Get all moves which are not trump suit or matching the suit of the enemy's card
    for move in moves:

      if move[0] is not None and util.get_suit(move[0]) == suit:
        lowest_suit_moves.append(move)

    if len(lowest_suit_moves) == 0:
      lowest_suit_moves = moves

    # Get move with highest rank available, of the subset that we've narrowed down so far
    for move in lowest_suit_moves:
      if move[0] is not None and move[0] % 5 <= chosen_move[0] % 5:
        chosen_move = move

    return chosen_move

  def check_marriage_jack_exchange(self,state):
    moves = state.moves()
    for move in moves:
      if (move[1] is not None):
        return move
    return None

  def trump_play(self,state):
    moves = state.moves()
    trump_moves = []

    #Get all moves which are trump suit
    for move in moves:

      if move[0] is not None and util.get_suit(move[0]) == state.get_trump_suit():
        trump_moves.append(move)

    if len(trump_moves) > 0:
      # Get move with highest rank available, of the subset that we've narrowed down so far
      chosen_move = trump_moves[0]
      for move in trump_moves:
        if move[0] is not None and move[0] % 5 <= chosen_move[0] % 5:
          chosen_move = move
      return chosen_move
    return None
