"""
Game of Stonehenge
"""
from game import Game
from game_state import GameState
"""
Represents one cell of the board
"""
class Cell:
    """
    Initialize a new Cell
    """
    def __init__(self, value):
        """
        Initialize a new Cell
        """

        self.value = value
        self.claim = None
        self.right = None
        self.left = None
        self.hori = None

    def __str__(self):
        """
        Returns the value of the Cell
        >>> new_cell = Cell(5)
        >>> str(new_cell)
        'Cell: 5 '
        """
        return "Cell: {} ".format(self.value)

    def copy(self):
        """
        Returns an empty copy of the Cell
        >>> new_cell = Cell(5)
        >>> new_cell.right = Cell(2)
        >>> bruh = new_cell.copy()
        >>> str(bruh.right)
        'Cell: 2 '
        """

        new_cell = Cell(self.value)
        new_cell.claim = self.claim
        new_cell.right = self.right
        new_cell.left = self.left
        new_cell.hori = self.hori
        return new_cell

class StonehengeState(GameState):
    """
    The state of StoneHenge Game in certain time
    """
    def __init__(self, is_p1_turn: bool, board_size) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.
        """

        self.p1_turn = is_p1_turn
        self.board_size = board_size
        self.board = []
        self.leylines = [[], [], []]
        for i in range(len(self.leylines)):
            for _ in range(board_size+1):
                self.leylines[i].append("@")
        counter = 65
        for i in range(board_size+1):
            self.board.append([])
        size = 2
        for i in range(board_size+1):
            for _ in range(size):
                self.board[i].append(Cell(chr(counter)))
                counter += 1
            if size == board_size + 1:
                size -= 1
            else:
                size += 1
        self.init_hori()
        self.init_left()
        self.init_right()

    def init_hori(self):
        """
        Links up the leylines from left to right
        >>> new_state = StonehengeState(True, 2)
        >>> str(new_state.board[0][0].hori)
        'Cell: B '
        """
        for i in range(len(self.board)):
            for b in range(len(self.board[i])-1):
                self.board[i][b].hori = self.board[i][b+1]

    def init_left(self):
        """
        Links up the leylines from top right to bottom left
        >>> new_state = StonehengeState(True, 2)
        >>> str(new_state.board[0][0].left)
        'Cell: C '
        """
        for i in range(len(self.board) - 2):
            self.board[i][0].left = self.board[i+1][0]
        for i in range(1, len(self.board)):
            for b in range(-1 + i, len(self.board) - 2):
                self.board[b][i].left = self.board[b+1][i]
            self.board[len(self.board)-2][i].left =\
                self.board[len(self.board)-1][i-1]

    def init_right(self):
        """
        Links up the leyliens from top left to bottom right
        >>> new_state = StonehengeState(True, 2)
        >>> str(new_state.board[0][0].right)
        'Cell: D '
        """
        for i in range(1, len(self.board)-1):
            self.board[i-1][i].right = self.board[i][i+1]
        for i in range(len(self.board)-1):
            for b in range(i, len(self.board)-2):
                self.board[b][b-i].right = self.board[b+1][b-i+1]
            self.board[len(self.board)-2][len(self.board)- 2 - i].right =\
            self.board[len(self.board)-1][len(self.board)-i-2]


    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.

        >>> new_state = StonehengeState(True, 2)
        >>> new_state = new_state.make_move("A")
        >>> other_state = StonehengeState(True, 2)
        >>> other_state = other_state.make_move("A")
        >>> str(new_state) == str(other_state)
        True

        """
        s = ""

        s += " "*(self.board_size+1-len(self.board[0]))
        s += ("      ")
        #Adjusting Leyline(0-2)
        for i in range(2):
            s += self.leylines[1][i] + "   "
        s += "\n     "
        s += " " * (self.board_size + 1 - len(self.board[0]))
        for i in range(2):
            s += "/" + "   "
        s += "\n"
        for i in range(len(self.board)):
            s += " "*(self.board_size+1-len(self.board[i]))
            s += self.leylines[0][i]
            s += " - "
            for b in range(len(self.board[i])):
                if self.board[i][b].claim is None:
                    s += self.board[i][b].value
                else:
                    s += self.board[i][b].claim
                if b < (len(self.board[i])-1):
                    s += " - "
            if i == len(self.board)-1:
                s += "    " + self.leylines[2][0]
            if i < len(self.board)-2:
                s += "   " + self.leylines[1][i+2]
            s += "\n"
            s += " " * (self.board_size + 1 - len(self.board[i]))
            s += "   "
            for b in range(len(self.board[i])):
                if self.board[i][b].left is not None:
                    s += "/"
                s += " "
                if self.board[i][b].right is not None:
                    s += "\\"
                s += " "
            if i < self.board_size-1:
                s += "/"
            if i == self.board_size-1:
                s += "\\"
            s += "\n"
        #ADJUSTING lEYLINE[2]
        s += " " * (self.board_size + 1 - len(self.board[0]))
        s += "     "
        for i in range(len(self.leylines[2])-1, 0, -1):
            s += self.leylines[2][i] + "   "
        return s

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.
        >>> new_state = StonehengeState(True, 2)
        >>> new_state.get_possible_moves()
        ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        """
        possible_moves = []

        for i in range(len(self.board)):
            for b in range(len(self.board[i])):
                if self.board[i][b].claim is None:
                    possible_moves.append(self.board[i][b].value)

        count1, count2 = 0, 0
        for i in self.leylines:
            for b in i:
                if b == "1":
                    count1 += 1
                elif b == "2":
                    count2 += 1

        if count1 / (len(self.leylines) * len(self.leylines[0])) >= .5 or \
                count2 / (len(self.leylines) * len(self.leylines[0])) >= .5:
            possible_moves = []
        return possible_moves


    def get_current_player_name(self) -> str:
        """
        Return 'p1' if the current player is Player 1, and 'p2' if the current
        player is Player 2.
        >>> new_state = StonehengeState(True, 2)
        >>> new_state.get_current_player_name()
        'p1'
        """
        if self.p1_turn:
            return 'p1'
        return 'p2'

    def check_leylines(self, state, lst, pos):
        """
        Check through the leylines to see if a player has claimed it.
        Helper function to split up code
        """
        for i in range(len(lst)):
            p1, p2, count = 0, 0, 0
            cur_node = lst[i]

            while cur_node is not None:
                count += 1
                if cur_node.claim == "1":
                    p1 += 1
                elif cur_node.claim == "2":
                    p2 += 1
                if pos == 0:
                    cur_node = cur_node.hori
                elif pos == 1:
                    cur_node = cur_node.left
                elif pos == 2:
                    cur_node = cur_node.right


            if (p1 / count) >= .5 and state.leylines[pos][i] == '@':
                state.leylines[pos][i] = "1"
            elif (p2 / count) >= .5 and state.leylines[pos][i] == '@':
                state.leylines[pos][i] = "2"


    def make_move(self, move) -> 'GameState':
        """
        Return the GameState that results from applying move to this GameState.
        >>> new_state = StonehengeState(True, 2)
        >>> state = new_state.make_move("A")
        >>> new_state.board == state.board
        False
        """
        #CREATES A NEW BOARD##
        new_state = StonehengeState(not self.p1_turn, self.board_size)
        #COPIES ALL THE OLD CELLS ONTO THE BOARD
        for i in range(len(self.board)):
            for b in range(len(self.board[i])):
                new_state.board[i][b] = Cell.copy(self.board[i][b])
        #APPLIES THE NEW MOVE TO THE NEW BOARD
        for i in range(len(new_state.board)):
            for b in range(len(new_state.board[i])):
                if new_state.board[i][b].value == move:
                    new_state.board[i][b].claim = \
                        self.get_current_player_name()[1]

        hori_nodes, left_nodes, right_nodes = \
            [], [new_state.board[0][0]], [new_state.board[0][1]]
        #COPYING THE OLD LEYLINES ONTO THE NEW BOARD
        for i in range(len(new_state.leylines)):
            for b in range(len(new_state.leylines[i])):
                new_state.leylines[i][b] = self.leylines[i][b]
        #LINKING THE LEYLINES TOGETHER
        new_state.init_hori()
        new_state.init_left()
        new_state.init_right()
        #ITERATING THROUGH TH EHEADS OF THE BOARD
        for i in range(len(new_state.board)):
            hori_nodes.append(new_state.board[i][0])
        for i in range(len(new_state.board)-1):
            left_nodes.append(new_state.board[i][len(new_state.board[i])-1])
        for i in range(len(new_state.board)-1):
            right_nodes.append(new_state.board[i][0])
        #ITERATING THROUGH HORIZONTALLY AND CHECKING WHETHER IF CELLS
        #ARE CLAIMED IN A LEYLINE
        new_state.check_leylines(new_state, hori_nodes, 0)
        new_state.check_leylines(new_state, left_nodes, 1)
        new_state.check_leylines(new_state, right_nodes, 2)
        return new_state

    def is_valid_move(self, move) -> bool:
        """
        Return whether move is a valid move for this GameState.
        >>> new_state = StonehengeState(True, 2)
        >>> new_state.is_valid_move("BOB")
        False
        """
        return move in self.get_possible_moves()

    def __repr__(self):
        """
        Return a representation of this state (which can be used for
        equality testing).
        >>> new_state = StonehengeState(True, 2)
        >>> new_state = new_state.make_move("A")
        >>> other_state = StonehengeState(True, 2)
        >>> other_state = other_state.make_move("A")
        >>> repr(new_state) == repr(other_state)
        True
        """

        s = ""
        if self.p1_turn:
            s += "p1"
        else:
            s += "p2"
        count = self.captured_leylines(s)
        s += " has claimed {} percent of leylines".format(count)
        return s

    def captured_leylines(self, player):
        """
        Returns the number of captured leyines for a given player
        >>> new_state = StonehengeState(True, 2)
        >>> new_state = new_state.make_move("A")
        >>> new_state = new_state.make_move("B")
        >>> new_state = new_state.make_move("C")
        >>> new_state.captured_leylines("p1")
        0.3333333333333333
        """

        count = 0
        for i in self.leylines:
            for b in i:
                if b == "1" and player == "p1":
                    count += 1
                elif b == "2" and player == "p2":
                    count += 1
        return count/(len(self.leylines)*len(self.leylines[0]))

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.
        >>> new_state = StonehengeState(True, 2)
        >>> new_state.rough_outcome()
        0.0
        """
        if self.get_possible_moves() == []:
            return self.LOSE
        for i in self.get_possible_moves():
            new_state = self.make_move(i)
            for b in new_state.get_possible_moves():
                new_state2 = new_state.make_move(b)
                if new_state2.get_possible_moves() == []:
                    return self.LOSE
            if new_state.get_possible_moves() == []:
                return self.WIN
        return self.captured_leylines(self.get_current_player_name())

class StonehengeGame(Game):
    """
    Abstract class for a game to be played with two players.
    """
    def __init__(self, p1_starts):

        x = "e"
        while not x.isnumeric():
            x = input("Enter the size of the board")
        x = int(x)
        self.current_state = StonehengeState(p1_starts, x)

    def get_instructions(self) -> str:
        """
        Return the instructions for this Game.
        """
        return "CLAIM LEYLINES TO WIN BY PICKING " \
               "CELLS THAT WORK THE BEST GOOD LUCK!"

    def is_over(self, state: GameState) -> bool:
        """
        Return whether or not this game is over at state.
        """
        count1 = 0
        count2 = 0
        for i in state.leylines:
            for b in i:
                if b == "1":
                    count1 += 1
                elif b == "2":
                    count2 += 1

        if count1/(len(state.leylines)*len(state.leylines[0])) >= .5 or\
            count2/(len(state.leylines)*len(state.leylines[0])) >= .5:
            return True
        return False

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.
        """
        if player == 'p1'and self.current_state.captured_leylines('p1') >= .5:
            return True
        elif player == 'p2' and \
                self.current_state.captured_leylines('p2') >= .5:
            return True
        return False

    def str_to_move(self, string: str):
        """
        Return the move that string represents. If string is not a move,
        return some invalid move.
        """
        if isinstance(string, str) and string.isupper()\
                and not string.isnumeric():
            return string
        return -1


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")