"""
A Python 3.6 adaptation of Information Set Monte Carlo Tree Search.

See this gist for the original code: https://gist.github.com/kjlubick/8ea239ede6a026a61f4d.
"""
# This is a very simple Python 2.7 implementation of the Information Set Monte Carlo Tree Search algorithm.
# The function ISMCTS(rootstate, itermax, verbose = False) is towards the bottom of the code.
# It aims to have the clearest and simplest possible code, and for the sake of clarity, the code
# is orders of magnitude less efficient than it could be made, particularly by using a
# state.GetRandomMove() or state.DoRandomRollout() function.
#
# An example GameState classes for Knockout Whist is included to give some idea of how you
# can write your own GameState to use ISMCTS in your hidden information game.
#
# Written by Peter Cowling, Edward Powley, Daniel Whitehouse (University of York, UK) September 2012 - August 2013.
#
# Licence is granted to freely use and distribute for any sensible/legal purpose so long as this comment
# remains in any distributed code.
#
# For more information about Monte Carlo Tree Search check out our web site at www.mcts.ai
# Also read the article accompanying this code at ***URL HERE***
import math
import random

from api import State, engine, util

# Strategy to function mapping.
VALUATION_FUNCTIONS = {
    'id': {
        'function': lambda x: x,
        'min': -3.0,
        'max': 3.0,
    },
    'win': {
        'function': lambda x: float(x > 0.0),
        'min': 0.0,
        'max': 1.0,
    },
    'get_at_least_2': {
        'function': lambda x: float(x >= 2.0),
        'min': 0.0,
        'max': 1.0,
    },
    'get_at_least_3': {
        'function': lambda x: float(x >= 3.0),
        'min': 0.0,
        'max': 1.0,
    },
    'prevent_other_player_from_getting_2': {
        'function': lambda x: float(x > -2.0),
        'min': 0.0,
        'max': 1.0,
    },
    'prevent_other_player_from_getting_3': {
        'function': lambda x: float(x > -3.0),
        'min': 0.0,
        'max': 1.0,
    },

}


class Bot:
    __itermax = 5

    def __init__(self, itermax=5):
        self.__itermax = itermax

    def get_move(self, state):
        # type: (State) -> tuple[int, int]
        """
        Oh shit wadup
        :param State state: An object representing the gamestate. This includes a link to
            the states of all the cards, the trick and the points.
        :return: A tuple of integers or a tuple of an integer and None,
            indicating a move; the first indicates the card played in the trick, the second a
            potential spouse.
        """
        best_move = None
        # Return a random choice
        return ISMCTS(state, self.__itermax)
        # # Create player 1
        # player1 = util.load_player("rand")


        # return best_move

class Node:
    """
    A node in the game tree.

    Note wins is always from the viewpoint of playerJustMoved.
    """

    def __init__(
        self, move=None, parent=None, playerjustmoved=None, strategy='id'
    ):
        self.move = move  # the move that got us to this node - "None" for the root node
        self.strategy = strategy
        self.parentNode = parent  # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.avails = 1
        # part of the state that the Node needs later
        self.playerJustMoved = playerjustmoved
        self.valuation_function = VALUATION_FUNCTIONS[self.strategy]['function']
        self._min_value = VALUATION_FUNCTIONS[self.strategy]['min']
        self._max_value = VALUATION_FUNCTIONS[self.strategy]['max']

    def GetUntriedMoves(self, legalmoves):
        """Return the elements of legalmoves for which this node does not have children."""
        # Find all moves for which this node *does* have children
        triedMoves = [child.move for child in self.childNodes]
        # Return all moves that are legal but have not been tried yet
        return [move for move in legalmoves if move not in triedMoves]

    def UCBSelectChild(self, legalmoves, exploration=0.8):
        """
        Use the UCB1 formula to select a child node, filtered by the given list of legal moves.

        `exploration` is a constant balancing between exploitation and exploration.
        """
        # Filter the list of children by the list of legal moves
        legalChildren = [child for child in self.childNodes if
                         child.move in legalmoves]
        # Get the child with the highest UCB score.
        # Rescale wins / visits to the range [0, 1] in case the valuation function doesn't.
        s = max(
            legalChildren,
            key=lambda c:
            (
                float(c.wins) / float(c.visits) - self._min_value
            ) / (self._max_value - self._min_value) +
            exploration * math.sqrt(math.log(c.avails) / float(c.visits))
        )
        # Update availability counts -- it is easier to do this now than during backpropagation
        for child in legalChildren:
            child.avails += 1

        # Return the child selected above
        return s

    def AddChild(self, m, playerJustMoved):
        """
        Add a new child node for the move m.

        Return the added child node.
        """
        n = Node(
            move=m,
            parent=self,
            playerjustmoved=playerJustMoved,
            strategy=self.strategy
        )
        self.childNodes.append(n)
        return n

    def Update(self, terminalState):
        """
        Update this node.

        1. Increment the visit count by one.
        2. increase the win count by the result of terminalState for self.playerJustMoved.
        """
        self.visits += 1
        if self.playerJustMoved is not None:
            self.wins += self.valuation_function(
                terminalState.get_pending_points(self.playerJustMoved))

    def __repr__(self):
        """Represent a node as a string."""
        return '[M:{} E/W/V/A: {:.3f} / {:.2f} / {:6d} / {:6d}]'.format(
            str(self.move).ljust(20),
            (self.wins / self.visits),
            self.wins,
            self.visits,
            self.avails,
        )

    def TreeToString(self, indent):
        """Represent the tree as a string for debugging purposes."""
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
            s += c.TreeToString(indent + 1)
        return s

    def IndentString(self, indent):
        """Indent a string for debugging purposes."""
        s = "\n"
        for i in range(1, indent + 1):
            s += "| "
        return s

    def ChildrenToString(self):
        """Represent children as strings for debugging purposes."""
        s = ""
        for c in self.childNodes:
            s += str(c) + "\n"
        return s


def ISMCTS(rootstate, itermax, strategy='id', verbose=False):
    """
    Conduct an ISMCTS search for itermax iterations starting from rootstate.

    Return the best move from the rootstate.
    """
    rootnode = Node(strategy=strategy)

    # Create player 1
    player1 = util.load_player("rand")
    # Create player 2
    player2 = util.load_player("rand")
    # Play the game
    # The game loop
    while not mState.finished():
        player = player1 if mState.whose_turn() == 1 else player2
        # We introduce a state signature which essentially obscures the deck's perfect knowledge from the player
        # given_state = state.clone(signature=state.whose_turn()) if state.get_phase() == 1 else state.clone()
        #TODO wadup
        mState.make_assumption()
        move = engine.get_move(mState, player, 5000, False)
        if engine.is_valid(move, player): # check for common mistakes
            mState = mState.next(move)
            if not mState.revoked() is None:
                print('!   Player {} revoked (made illegal move), game finished.'.format(mState.revoked()))
        else:
            mState.set_to_revoked()
    for i in range(itermax):
        node = rootnode

        # Determinize
        state = rootstate.CloneAndRandomize(rootstate.playerToMove)

        # Select
        while state.GetMoves() != [] and node.GetUntriedMoves(state.GetMoves()) == []: # node is fully expanded and non-terminal
            node = node.UCBSelectChild(state.GetMoves())
            state.DoMove(node.move)

        # Expand
        untriedMoves = node.GetUntriedMoves(state.GetMoves())
        if untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(untriedMoves)
            player = state.playerToMove
            state.DoMove(m)
            node = node.AddChild(m, player) # add child and descend tree

        # Simulate
        while state.GetMoves() != []: # while state is non-terminal
            state.DoMove(random.choice(state.GetMoves()))

        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            node.Update(state)
            node = node.parentNode

    # for i in range(itermax):
    #     node = rootnode
    #
    #     # Determinize
    #     # state = rootstate.CloneAndRandomize(rootstate.playerToMove)
    #     mState = rootstate.clone()
    #     # mState.make_assumption()
    #
    #     # Select
    #     # While: node is fully expanded and non-terminal
    #     moves = mState.moves()
    #
    #     while moves != [] and node.GetUntriedMoves(legalmoves=moves) == []:
    #         node = node.UCBSelectChild(legalmoves=moves)
    #         mState.next(move=node.move)
    #
    #     # Expand
    #
    #     untriedMoves = node.GetUntriedMoves(legalmoves=moves)
    #     # if we can expand (i.e. state/node is non-terminal)
    #     if untriedMoves != []:
    #         m = random.choice(untriedMoves)
    #         player = mState.whose_turn()
    #         mState.next(move=m)
    #         node = node.AddChild(
    #             m=m,
    #             playerJustMoved=player
    #         )  # add child and descend tree
    #     # Simulate
    #     # while moves != []:  # while state is non-terminal
    #     #      move=random.choice(moves)
    #     #      mState.next(move)
    #         # moves = mState.moves()
    #     # Create player 1
    #     player1 = util.load_player("rand")
    #     # Create player 2
    #     player2 = util.load_player("rand")
    #
    #     # Play the game
    #     # The game loop
    #     while not mState.finished():
    #         player = player1 if mState.whose_turn() == 1 else player2
    #         # We introduce a state signature which essentially obscures the deck's perfect knowledge from the player
    #         # given_state = state.clone(signature=state.whose_turn()) if state.get_phase() == 1 else state.clone()
    #         #TODO wadup
    #         mState.make_assumption()
    #         print("made assumption")
    #         print(mState)
    #         move = engine.get_move(mState, player, 5000, False)
    #         if engine.is_valid(move, player): # check for common mistakes
    #             mState = mState.next(move)
    #             if not mState.revoked() is None:
    #                 print('!   Player {} revoked (made illegal move), game finished.'.format(mState.revoked()))
    #         else:
    #             mState.set_to_revoked()
    #
    #     # Backpropagate
    #     while node is not None:  # backpropagate from the expanded node and work back to the root
    #         node.Update(mState)
    #         node = node.parentNode


    # Output some information about the tree - can be omitted
    if verbose > 1.0:
        print(rootnode.TreeToString(0))
    elif verbose:
        print(rootnode.ChildrenToString())

    return max(rootnode.childNodes,
               key=lambda c: c.visits).move  # return the most visited move
