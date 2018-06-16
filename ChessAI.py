#! /usr/bin/env python
"""
 Project: Python Chess
 File name: ChessAI.py
 Description:  Contains the AI classes.
    
 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 """
 
from ChessRules import ChessRules
from ChessBoard import ChessBoard
import random
import time
from collections import OrderedDict, namedtuple
import sunpush

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
                    if len(self.Rules.GetListOfValidMoves(board,(row,col))) > 0:
                        myPieces.append((row,col))    
        
        return myPieces
        
class ChessAI_random(ChessAI):
    #Randomly pick any legal move.    
    
    def GetMove(self,board,color):
        time.sleep(1)
        #print "In ChessAI_random.GetMove"
        if color == "black":
            board.Rotate() #rotate it so that chessrules can understand it
    
        myPieces = self.GetMyPiecesWithLegalMoves(board)
        
        #pick a random piece, then a random legal move for that piece
        fromTuple = myPieces[random.randint(0,len(myPieces)-1)]
                #fromTuple = myPieces[0]
        legalMoves = self.Rules.GetListOfValidMoves(board,fromTuple)
        toTuple = legalMoves[random.randint(0,len(legalMoves)-1)]
                #toTuple = legalMoves[0]
        
        moveTuple = (fromTuple,toTuple)
        if color == "black":
            board.Rotate() #rotate it back
            #moveTuple = tuple(tuple(7-x for x in y) for y in moveTuple)
        
        return moveTuple
                                
Entry = namedtuple('Entry', 'depth score gamma move')
tp = OrderedDict()
        
class ChessAI_sunpush(ChessAI):

    #For each piece, find it's legal moves.
    #Find legal moves for all opponent pieces.
    #Throw out my legal moves that the opponent could get next turn.
    #From remaining moves, if it puts opponent in check by performing the move, take it.
    #Otherwise pick a random remaining move.    
    
    #Limitation(s): Doesn't include blocking or sacrificial moves of a lesser piece to protect better one.
    
    def __init__(self,name,color,protectionPriority=("queen","rook","bishop","knight","pawn")):
        self.piecePriority = protectionPriority
        ChessAI.__init__(self,name,color)
        Difficulty='Medium' #Easy, Medium or Hard. Harder = noticeably slower.
        Diffs={'Hard':100000,'Medium':10000,'Easy':1000}
        sunpush.NODES_SEARCHED = Diffs[Difficulty]
    
    def GetMove(self,board,color):
        if color == 'black':
            board.Rotate()
        pos = sunpush.Position(board.board, 0, board.lastdir, board.oldboard)
        move,score = sunpush.search(pos)
        if color == 'black':
            board.Rotate()
        return tuple(board.ToTuple(j) for j in move)
        
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
