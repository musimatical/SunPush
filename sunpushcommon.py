
from __future__ import print_function
import re
import s
from itertools import count
from collections import OrderedDict, namedtuple

# The table size is the maximum number of elements in the transposition table.
TABLE_SIZE = 1e6

# This constant controls how much time we spend on looking for optimal moves.
NODES_SEARCHED = 5e3

# Mate value must be greater than 8*queen + 2*(rook+knight+bishop)
# King value is set to twice this value such that if the opponent is
# 8 queens up, but we got the king, we still exceed MATE_VALUE.
MATE_VALUE = 30000


if sys.version_info[0] == 2:
    input = raw_input

# Our board is represented as a 120 character string. The padding allows for
# fast detection of moves that don't stay within the board.
A1, H1, A8, H8 = 91, 98, 21, 28
initial = (
    '         \n'  #   0 -  9
    '         \n'  #  10 - 19
    ' n......n\n'  #  20 - 29
    ' .rbqkbr.\n'  #  30 - 39
    ' .p....p.\n'  #  40 - 49
    ' .pppppp.\n'  #  50 - 59
    ' .PPPPPP.\n'  #  60 - 69
    ' .P....P.\n'  #  70 - 79
    ' .RBQKBR.\n'  #  80 - 89
    ' N......N\n'  #  90 - 99
    '         \n'  # 100 -109
    '          '   # 110 -119
)

###############################################################################
# Move and evaluation tables
###############################################################################

N, E, S, W = -10, 1, 10, -1
directions = {
    'P': (N, N+W, N+E),
    'N': (2*N+E, N+2*E, S+2*E, 2*S+E, 2*S+W, S+2*W, N+2*W, 2*N+W),
    'B': (N+E, S+E, S+W, N+W),
    'R': (N, E, S, W),
    'Q': (N, E, S, W, N+E, S+E, S+W, N+W),
    'K': (N, E, S, W, N+E, S+E, S+W, N+W)
}
alldirections = [2*N+E, N+2*E, S+2*E, 2*S+E, 2*S+W, S+2*W, N+2*W, 2*N+W,N, E, S, W, N+E, S+E, S+W, N+W]


doc = open('PieceValues.txt','r')

PVals = [int(x) for x in doc.readline().partition("[")[2].partition("]")[0].split(', ')]
BVals = [int(x) for x in doc.readline().partition("[")[2].partition("]")[0].split(', ')]
NVals = [int(x) for x in doc.readline().partition("[")[2].partition("]")[0].split(', ')]
RVals = [int(x) for x in doc.readline().partition("[")[2].partition("]")[0].split(', ')]
QVals = [int(x) for x in doc.readline().partition("[")[2].partition("]")[0].split(', ')]
KVals = [int(x) for x in doc.readline().partition("[")[2].partition("]")[0].split(', ')]
#messy, but it gets the job done. Searches for bits between '(' and ')' and converts to int list.
global pst
pst = {
    'P': PVals,
    'B': BVals,
    'N': NVals,
    'R': RVals,
    'Q': QVals,
    'K': KVals
}

class Position(namedtuple('Position', 'board score oldd oldboard')):
    """ A state of a chess game
    board -- a 120 char representation of the board
    score -- the board evaluation
    oldd -- the previous direction
    oldboard -- previous board
    """

    def gen_moves(self):
        # For each of our pieces, iterate through each possible 'ray' of moves,
        # as defined in the 'directions' map. The rays are broken e.g. by
        # captures or immediately in case of pieces such as knights.
        for i, p in enumerate(self.board):
            if not p.isupper(): continue
            for d in directions[p]:
                for j in count(i+d, d):
                    q = self.board[j]
                    # Stay inside the board
                    if self.board[j].isspace(): break
                    # No friendly captures
                    if q.isupper(): break
                    # Special pawn stuff
                    if p == 'P' and d in (N+W, N+E) and q == '.': break
                    if p == 'P' and d == N and q != '.': break
                    # No king pushes
                    if p == 'K' and q != '.': break
                    if p == 'K':
                        if self.board[j+N] == 'k': break
                        if self.board[j+W] == 'k': break
                        if self.board[j+S] == 'k': break
                        if self.board[j+E] == 'k': break
                        if self.board[j+N+W] == 'k': break
                        if self.board[j+N+E] == 'k': break
                        if self.board[j+S+W] == 'k': break
                        if self.board[j+S+E] == 'k': break
                    # No 'pushbacks'
                    if d == -self.oldd and self.oldboard[j] == p: break
                    # Move it
                    yield (i, j)
                    # Stop crawlers from sliding
                    if p in ('P', 'N', 'K'): break
                    # No sliding after captures
                    if q.islower(): break

    def rotate(self):
        return Position(
            self.board[::-1].swapcase(), -self.score, -self.oldd, self.oldboard[::-1].swapcase())

    def move(self, move):
        global nummoves
        i = list(move)
        p = [self.board[x] for x in i]
        put = lambda board, i, p: board[:i] + p + board[i+1:]
        # Copy variables and reset ep and kp
        board = self.board
        oldboard = board
        score = self.score + self.value(move)
        # Actual move, including push mechanism
        if 0:
            board = put(board, i[1], board[i])
            board = put(board, i[0], '.')
        if 1:
            dist = i[1]-i[0]
            basedirection = max((x for x in directions[p[0]] if dist % x == 0 and dist//x > 0),key=lambda y: -dist//y )
            #funnel 'outwards' searching for pieces to push, then push them on the way back 'in'
            while p[-1].isupper() or p[-1].islower():
                i.append(i[-1]+basedirection) 
                p.append(self.board[i[-1]])
            for x in range(len(p)-2):
                if not p[x+2].isspace():
                    board = put(board, i[x+2], p[x+1])
            board = put(board, i[1], p[0])
            board = put(board, i[0], '.')
        # Special pawn stuff
        if p[0] == 'P':
            if A8 <= i[1] <= H8:
                board = put(board, i[1], 'Q')
        # We rotate the returned position, so it's ready for the next player
        return Position(board, score, basedirection, oldboard).rotate()

    def value(self, move):
        i = list(move)
        p = [self.board[x] for x in i]
        dist = i[1]-i[0]
        basedirection = (1-2*(i[1]-i[0]<0))*max((abs(x) for x in alldirections if dist % x ==0 and dist//x > 0))
        while p[-1].isupper() or p[-1].islower():
            i.append(i[-1]+basedirection) 
            p.append(self.board[i[-1]])
        # Actual move AND capture
        score = 0
        for x in range(len(i)-1):
            if p[x].isupper():
                score += pst[p[x].upper()][i[x+1]] - pst[p[x].upper()][i[x]]
            if p[x].islower():
                score -= pst[p[x].upper()][i[x+1]] - pst[p[x].upper()][i[x]]
        # Special pawn stuff
        if p == 'P':
            if A8 <= i[1] <= H8:
                score += pst['Q'][i[1]] - pst['P'][i[1]]
        return score

Entry = namedtuple('Entry', 'depth score gamma move')
tp = OrderedDict()


###############################################################################
# Search logic
###############################################################################

nodes = 0
def bound(pos, gamma, depth):
    """ returns s(pos) <= r < gamma    if s(pos) < gamma
        returns s(pos) >= r >= gamma   if s(pos) >= gamma """
    global nodes; nodes += 1

    # Look in the table if we have already searched this position before.
    # We use the table value if it was done with at least as deep a search
    # as ours, and the gamma value is compatible.
    entry = tp.get(pos)
    if entry is not None and entry.depth >= depth and (
            entry.score < entry.gamma and entry.score < gamma or
            entry.score >= entry.gamma and entry.score >= gamma):
        return entry.score

    # Stop searching if we have won/lost.
    if abs(pos.score) >= MATE_VALUE:
        return pos.score

    # Null move. Is also used for stalemate checking
    nullscore = -bound(pos.rotate(), 1-gamma, depth-3) if depth > 2 else pos.score
    #nullscore = -MATE_VALUE*3 if depth > 0 else pos.score
    if nullscore >= gamma:
        return nullscore

    # We generate all possible, pseudo legal moves and order them to provoke
    # cuts. At the next level of the tree we are going to minimize the score.
    # This can be shown equal to maximizing the negative score, with a slightly
    # adjusted gamma value.
    best, bmove = -3*MATE_VALUE, None
    for move in sorted(pos.gen_moves(), key=pos.value, reverse=True):
        # We check captures with the value function, as it also contains ep and kp
        if depth <= 0 and pos.value(move) < 300:
            break
        score = -bound(pos.move(move), 1-gamma, depth-1)
        if score > best:
            best = score
            bmove = move
        if score >= gamma:
            break

    # If there are no captures, or just not any good ones, stand pat
    if depth <= 0 and best < nullscore:
        return nullscore
    # Check for stalemate. If best move loses king, but not doing anything
    # would save us. Not at all a perfect check.
    if depth > 0 and best <= -MATE_VALUE and nullscore > -MATE_VALUE:
        best = 0

    # We save the found move together with the score, so we can retrieve it in
    # the play loop. We also trim the transposition table in FILO order.
    # We prefer fail-high moves, as they are the ones we can build our pv from.
    if entry is None or depth >= entry.depth and best >= gamma:
        tp[pos] = Entry(depth, best, gamma, bmove)
        if len(tp) > TABLE_SIZE:
            tp.popitem()
    return best


def search(pos, maxn=NODES_SEARCHED):
    """ Iterative deepening MTD-bi search """
    global nodes; nodes = 0

    # We limit the depth to some constant, so we don't get a stack overflow in
    # the end game.
    for depth in range(1, 99):
        # The inner loop is a binary search on the score of the position.
        # Inv: lower <= score <= upper
        # However this may be broken by values from the transposition table,
        # as they don't have the same concept of p(score). Hence we just use
        # 'lower < upper - margin' as the loop condition.
        lower, upper = -3*MATE_VALUE, 3*MATE_VALUE
        while lower < upper - 3:
            gamma = (lower+upper+1)//2
            score = bound(pos, gamma, depth)
            if score >= gamma:
                lower = score
            if score < gamma:
                upper = score

        # We stop deepening if the global N counter shows we have spent too
        # long, or if we have already won the game.
        if nodes >= maxn or abs(score) >= MATE_VALUE:
            break

    # If the game hasn't finished we can retrieve our move from the
    # transposition table.
    entry = tp.get(pos)
    if entry is not None:
        return entry.move, score
    return None, score


def parse(c):
    fil, rank = ord(c[0]) - ord('a'), int(c[1]) - 1
    return A1 + fil - 10*rank


def render(i):
    rank, fil = divmod(i - A1, 10)
    return chr(fil + ord('a')) + str(-rank + 1)


def print_pos(pos):
    print()
    uni_pieces = {'R':'♜', 'N':'♞', 'B':'♝', 'Q':'♛', 'K':'♚', 'P':'♟',
                  'r':'♖', 'n':'♘', 'b':'♗', 'q':'♕', 'k':'♔', 'p':'♙', '.':'·'}
    for i, row in enumerate(pos.board.strip().split('\n ')):
        print(' ', 8-i, ' '.join(uni_pieces.get(p, p) for p in row))
    print('    a b c d e f g h \n\n')