#! /usr/bin/env python
"""
 Project: Python Chess
 File name: ChessAI.py
 Description:  Contains the AI classes.
    
 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 """
 
from ChessRules import ChessRules
from ChessBoard import ChessBoard,SunpushBoard
from updatevals import update
import random
import time
from collections import OrderedDict, namedtuple
import copy
from numpy import sign
from itertools import count
#import sunpush

class ChessAI:
    def __init__(self,name,color):
        #print "In ChessAI __init__"
        self.name = name
        self.color = color
        self.type = 'AI'
        self.Rules = ChessRules()
        
    def GetName(self):
        return self.name
        
    def GetColor(self):
        return self.color
        
    def GetType(self):
        return self.type
        
    def GetMyPiecesWithLegalMoves(self,board):
        #get list of my pieces
        myPieces = []
        for row in range(8):
            for col in range(8):
                piece = board.squares[row][col]
                if 'w' in piece:
                    if len(list(self.Rules.GetListOfValidMoves(board,(row,col)))) > 0:
                        myPieces.append((row,col))    
        
        return myPieces
        
class ChessAI_random(ChessAI):
    #Randomly pick any legal move.    
    
    def GetMove(self,board):
        #time.sleep(1)
        #print "In ChessAI_random.GetMove"
    
        moves = list( self.Rules.GetAllValidMoveNumbers(board))
        return moves[random.randint(0,len(moves)-1)]

class ChessAI_sunpush(ChessAI):
    #For each piece, find its legal moves.
    #Find legal moves for all opponent pieces.
    #Throw out my legal moves that the opponent could get next turn.
    #From remaining moves, if it puts opponent in check by performing the move, take it.
    #Otherwise pick a random remaining move.    
    #Limitation(s): Doesn't include blocking or sacrificial moves of a lesser piece to protect better one.

    def __init__(self,name,color,Difficulty='Medium'):
        ChessAI.__init__(self,name,color)
        Diffs={'Hard':100000,'Medium':10000,'Easy':1000,'VeryEasy':2}
        self.NODES_SEARCHED = Diffs[Difficulty]
        self.TABLE_SIZE = 1e8
        self.MATE_VALUE = 30000
        self.GetPieceValues()
        self.Entry = namedtuple('Entry', 'depth score gamma move')
        self.tp = OrderedDict()
        N, E, S, W = -10, 1, 10, -1
        self.directions = {
              'P': sorted([N, N+W, N+E]),
              'N': sorted([2*N+E, N+2*E, S+2*E, 2*S+E, 2*S+W, S+2*W, N+2*W, 2*N+W]),
              'B': sorted([N+E, S+E, S+W, N+W]),
              'R': sorted([N, E, S, W]),
              'Q': sorted([N, E, S, W, N+E, S+E, S+W, N+W]),
              'K': sorted([N, E, S, W, N+E, S+E, S+W, N+W])
        }        

    def GetPieceValues(self):
        self.pst = update()
        #with open('PieceValues.txt','r') as doc:
        #    PVals = [int(x) for x in doc.readline().partition("[")[2].partition("]")[0].split(', ')]
        #    BVals = [int(x) for x in doc.readline().partition("[")[2].partition("]")[0].split(', ')]
        #    NVals = [int(x) for x in doc.readline().partition("[")[2].partition("]")[0].split(', ')]
        #    RVals = [int(x) for x in doc.readline().partition("[")[2].partition("]")[0].split(', ')]
        #    QVals = [int(x) for x in doc.readline().partition("[")[2].partition("]")[0].split(', ')]
        #    KVals = [int(x) for x in doc.readline().partition("[")[2].partition("]")[0].split(', ')]
        ##with open('OverallValues.txt','r') as doc:
        #    #vals = doc.readline().partition("[")[2].partition("]")[0].split(',')
        #    #Vals = [int(x) for x in vals]
        #    #PVals = [int(Vals[0]) for x in range(120)]
        #    #BVals = [int(Vals[1]) for x in range(120)]
        #    #NVals = [int(Vals[2]) for x in range(120)]
        #    #RVals = [int(Vals[3]) for x in range(120)]
        #    #QVals = [int(Vals[4]) for x in range(120)]

        ##messy, but it gets the job done. Searches for bits between '(' and ')' and converts to int list.
        #self.pst = {
        #    'P': PVals,
        #    'B': BVals,
        #    'N': NVals,
        #    'R': RVals,
        #    'Q': QVals,
        #    'K': KVals
        #}

    def GetMove(self,chessboard):
        pos = SunpushBoard(chessboard.board,chessboard.squares,chessboard.recentsquares,chessboard.lastdir,0)
        pos.GetScore(self.pst)
        move,score = self.search(pos)
        print(score)
        if self.Rules.DoesMovePutPlayerInCheck(chessboard,'white',move):
            return ChessAI_random('','').GetMove(chessboard)
        return move

    #def GetMove(self,board,color):

    def value(self, chessboard, move):
        A1, H1, A8, H8 = 91, 98, 21, 28
        #alldirections = [2*N+E, N+2*E, S+2*E, 2*S+E, 2*S+W, S+2*W, N+2*W, 2*N+W,N, E, S, W, N+E, S+E, S+W, N+W]
        dist = move[1]-move[0]
        for x in self.directions[chessboard.board[move[0]]]:
            if dist % x == 0:
                basedirection = -sign(dist)*x
                break
        score = 0
        x0 = move[0]
        x1 = move[1]
        p = chessboard.board[x0]
        if p not in ['Q','K','N','B','P','R']: raise TypeError('not a valid move')
        while p not in [' ','.','\n']:
            if p in ['Q','K','N','B','P','R']:
                score += self.pst[p][x1] - self.pst[p][x0]
            elif p in ['q','k','n','b','p','r']:
                score -= self.pst[p.upper()][x1] - self.pst[p.upper()][x0]
            if p == 'P':
                if A8 <= x1 <= H8:
                    score += self.pst[move[2]][x1] - self.pst['P'][x0]
            if p == 'p':
                if A1 <= x1 <= H1:
                    score -= self.pst[move[2]][x1] - self.pst['P'][x0]
            x0 = x1
            x1 += basedirection
            p = chessboard.board[x0]
        return score


    def bound(self,pos, gamma, depth):
        """ returns s(pos) <= r < gamma    if s(pos) < gamma
            returns s(pos) >= r >= gamma   if s(pos) >= gamma """
        self.nodes += 1

        # Look in the table if we have already searched this position before.
        # We use the table value if it was done with at least as deep a search
        # as ours, and the gamma value is compatible.
        entry = self.tp.get(pos)
        if entry is not None and entry.depth >= depth and (
                entry.score < entry.gamma and entry.score < gamma or
                entry.score >= entry.gamma and entry.score >= gamma):
            return entry.score

        # Stop searching if we have won/lost.
        if abs(pos.score) >= self.MATE_VALUE:
            return pos.score

        # Null move. Is also used for stalemate checking
        nullscore = -self.bound(pos.Rotate(), 1-gamma, depth-3) if depth > 2 else pos.score
        #nullscore = -MATE_VALUE*3 if depth > 0 else pos.score
        if nullscore >= gamma:
            return nullscore

        # We generate all possible, pseudo legal moves and order them to provoke
        # cuts. At the next level of the tree we are going to minimize the score.
        # This can be shown equal to maximizing the negative score, with a slightly
        # adjusted gamma value.
        best, bmove = -3*self.MATE_VALUE, None
        #If we're on the top layer, make sure not to put in check. otherwise, whatevs.
        for move in sorted(self.Rules.GetAllValidMoveNumbers(pos,skipCheckTest=True), key=lambda move: self.value(pos,move), reverse=True):
            # We check captures with the value function, as it also contains ep and kp
            if depth <= 0 and self.value(pos,move) < 300:
                break
            score = -self.bound(pos.MovePiece(move,self), 1-gamma, depth-1)
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
        #if depth > 0 and best <= -self.MATE_VALUE and nullscore > -self.MATE_VALUE:
            #best = 0

        # We save the found move together with the score, so we can retrieve it in
        # the play loop. We also trim the transposition table in FILO order.
        # We prefer fail-high moves, as they are the ones we can build our pv from.
        if entry is None or depth >= entry.depth and best >= gamma:
            self.tp[pos] = self.Entry(depth, best, gamma, bmove)
            if len(self.tp) > self.TABLE_SIZE:
                self.tp.popitem()
        return best


    def search(self,pos):
        maxn=self.NODES_SEARCHED
        """ Iterative deepening MTD-bi search """
        self.nodes = 0

        # We limit the depth to some constant, so we don't get a stack overflow in
        # the end game.
        for depth in range(1, 99):
            # The inner loop is a binary search on the score of the position.
            # Inv: lower <= score <= upper
            # However this may be broken by values from the transposition table,
            # as they don't have the same concept of p(score). Hence we just use
            # 'lower < upper - margin' as the loop condition.
            lower, upper = -3*self.MATE_VALUE, 3*self.MATE_VALUE
            while lower < upper - 3:
                gamma = (lower+upper+1)//2
                score = self.bound(pos, gamma, depth)
                if score >= gamma:
                    lower = score
                if score < gamma:
                    upper = score

            # We stop deepening if the global N counter shows we have spent too
            # long, or if we have already won the game.
            if self.nodes >= maxn or abs(score) >= self.MATE_VALUE:
                break

        # If the game hasn't finished we can retrieve our move from the
        # transposition table.
        entry = self.tp.get(pos)
        if entry is not None:
            return entry.move, score
        return None, score
        
if __name__ == "__main__":
    
    from ChessBoard import ChessBoard
    cb = ChessBoard(3)
    board = cb.GetState()
    color = 'black'
    
    from ChessGUI_pygame import ChessGUI_pygame
    gui = ChessGUI_pygame()
    gui.Draw(board,highlightSquares=[])
    defense = ChessAI_defense('Bob','black')
    
    myPieces = defense.GetMyPiecesWithLegalMoves(board,color)
    enemyPieces = defense.GetEnemyPiecesWithLegalMoves(board,color)
    protectedMoveTuples = defense.GetProtectedMoveTuples(board,color,myPieces,enemyPieces)
    movesThatPutEnemyInCheck = defense.GetMovesThatPutEnemyInCheck(board,color,protectedMoveTuples)
    print("MyPieces = ", cb.ConvertSquareListToAlgebraicNotation(myPieces))
    print("enemyPieces = ", cb.ConvertSquareListToAlgebraicNotation(enemyPieces))
    print("protectedMoveTuples = ", cb.ConvertMoveTupleListToAlgebraicNotation(protectedMoveTuples))
    print("movesThatPutEnemyInCheck = ", cb.ConvertMoveTupleListToAlgebraicNotation(movesThatPutEnemyInCheck))
    c = raw_input("Press any key to quit.")#pause at the end
