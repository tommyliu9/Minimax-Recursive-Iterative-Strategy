"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any
import copy
from stack import Stack
from tree import Tree



# TODO: Adjust the type annotation as needed.
def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move


# TODO: Implement a recursive version of the minimax strategy.
def minimax_recursive_strategy(game: Any) -> Any:
    """
    Recursively finds the best possible move for the player
    """

    moves = game.current_state.get_possible_moves()
    dope = []
    for i in moves:
        new_game = copy.deepcopy(game)
        current_player = new_game.current_state.get_current_player_name()
        new_state = game.current_state.make_move(i)
        new_game.current_state = new_state
        x = go_through(new_game, new_state, current_player)
        dope.append(x)

    for i in range(len(moves)):
        if dope[i] == 1:
            return moves[i]
    for i in range(len(moves)):
        if dope[i] == 0:
            return moves[i]
    for i in range(len(moves)):
        if dope[i] == -1:
            return moves[i]

    return None

def go_through(game, state, current_player):
    """
    Helper function for the minimax_recursive_strategy
    """
    game.current_state = state
    if game.is_over(state):
        if game.is_winner(current_player):
            return state.WIN
        elif not game.is_winner(current_player):
            return state.LOSE
        return state.DRAW
    new_game = copy.deepcopy(game)
    return -1*max([go_through(new_game, state.make_move(i),\
                              state.get_current_player_name()) \
                   for i in state.get_possible_moves()])

def minimax_iterative_strategy(game: Any) -> Any:
    """
    Iteratively finds the best possible move for the player
    """

    moves = game.current_state.get_possible_moves()
    x = iterative_helper(game)
    lst = []
    for i in range(len(x.children)):
        lst.append(x.children[i].score)
    for i in range(len(x.children)):
        if x.children[i].score == -1:
            return moves[i]
    for i in range(len(x.children)):
        if x.children[i].score == 0:
            return moves[i]
    for i in range(len(x.children)):
        if x.children[i].score == 1:
            return moves[i]
    return None
def iterative_helper(game):
    """
    Finds the best possible moves through a stack and a tree
    """
    new_game = copy.deepcopy(game)
    stack = Stack()
    first_item = Tree(new_game)
    first_item.is_p1_turn = True
    stack.add(first_item)
    last_item = 0
    while not stack.is_empty():
        item = stack.remove()
        last_item = item
        if item.children != []:
            item.score = max([i.score*-1 for i in item.children])
        if item.value.is_over(item.value.current_state):
            if item.value.is_winner\
                        (item.value.current_state.get_current_player_name()):
                item.score = item.value.current_state.WIN
            elif not item.value.is_winner\
                        (item.value.current_state.get_current_player_name()):
                item.score = item.value.current_state.LOSE
            else:
                item.score = item.value.current_state.DRAW
        elif item.children == []:
            temp = []
            for i in item.value.current_state.get_possible_moves():
                state = item.value.current_state.make_move(i)
                new_game1 = copy.deepcopy(item.value)
                new_game1.current_state = state
                state = Tree(new_game1)
                temp.append(state)
            item.children = temp
            stack.add(item)
            for i in temp:
                stack.add(i)
    return last_item

# TODO: Implement an iterative version of the minimax strategy.

if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")