#! /usr/bin/env python
"""
 Project: Python Chess
 File name: ChessRules.py
 Description:  Functionality for determining legal chess moves.
    
 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 """  
from itertools import count
from ChessBoard import ChessBoard
import copy
import collections
 
class ChessRules:
    def IsStalemate(self,game):
        # Threefold repetition rule
        if len(game.StateList)>0:
            if max(collections.Counter(game.StateList).values())>2:
                return True
        else:
            #no valid moves but not in check
            return len(list(self.GetAllValidMoveNumbers(game.Board))) == 0 and not self.IsInCheck(game.Board)


    def IsCheckmate(self,chessboard):
        #returns true if 'color' player is in checkmate
        #Call GetListOfValidMoves for each piece of current player
        #If there aren't any valid moves for any pieces, then return true
        return len(list(self.GetAllValidMoveNumbers(chessboard))) == 0 and self.IsInCheck(chessboard)

    #def GetAllValidMoves(self,chessboard,skipCheckTest=False):
    #    for row in range(8):
    #        for col in range(8):
    #        #print(board.squares)
    #            piece = chessboard.squares[row][col]
    #            #Note that this function is just for white, other functions will pre-rotate the board if not.
    #            if 'w' in piece:
    #                for y in self.GetListOfValidMoves(chessboard,(row,col),skipCheckTest):
    #                    if isinstance(y[1],int):
    #                        yield ((row,col),y)
    #                    else:
    #                        yield((row,col),y[0],y[1])

    def GetAllValidMoveNumbers(self,chessboard,skipCheckTest=False):
        for x in xrange(20,100):
            piece = chessboard.board[x]
                #Note that this function is just for white, other functions will pre-rotate the board if not.
            if piece in ['N','Q','K','P','R','B']:
                for y in self.GetListOfValidMoves(chessboard,x,skipCheckTest):
                    if isinstance(y,int):
                        yield (x,y)
                    else:
                        yield(x,y[0],y[1])

    def GetListOfValidMoves(self,chessboard,i,skipCheckTest=False):
          #print(board,color,fromTuple,board[fromTuple[0]][fromTuple[1]])
          A1, H1, A8, H8 = 91, 98, 21, 28
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

          newboard = chessboard.board
          p=newboard[i]
          if not p.isupper(): 
              raise TypeError('not an uppercase piece')
          for d in directions[p]:
              for j in count(i+d, d):
                  q = newboard[j]
                  # Stay inside the board
                  if newboard[j] in [' ','\n']: break
                  # No friendly captures
                  if q.isupper(): break
                  # Special pawn stuff
                  if p == 'P' and d in (N+W, N+E) and q == '.': break
                  if p == 'P' and d == N and q != '.': break
                  # No king pushes
                  if p == 'K' and q != '.': break
                  # No 'pushbacks'
                  if d == -chessboard.lastdir and i in chessboard.recentsquares: break
                  # Move it
                  x0 = i
                  x1 = j
                  piece = chessboard.board[x0]
                  while piece not in [' ','.','\n']:
                      #checking for promotions
                      if (piece == 'P' and A8 <= x1 <= H8) or (piece == 'p' and A1 <= x1 <= H1):
                          for promotionPiece in ['Q','B','R','N']:
                              # No moving into check
                              if skipCheckTest or not self.DoesMovePutPlayerInCheck(chessboard,'white',(i,j,promotionPiece)): 
                                  yield (j,promotionPiece)
                          break
                      #checking for king-on-king contact
                      if piece.lower()=='k' and newboard[x1] not in [' ','\n']:
                          if piece.swapcase() in [newboard[x1+adj] for adj in directions['K']]: break
                      x0 = x1
                      x1 += d
                      piece = chessboard.board[x0]
                  #no king problems or promotions
                  else:
                      # No moving into check
                      if skipCheckTest or not self.DoesMovePutPlayerInCheck(chessboard,'white',(i,j)): 
                          yield j
                      #all clear, add to list of moves
                  if q.islower():
                      break
                  if p in ('P', 'N', 'K', 'Q'): break #these pieces only move one unit, don't check further
          
    def DoesMovePutPlayerInCheck(self,chessboard,color,moveTuple):
        #return False
        newboard = ChessBoard([chessboard.board,chessboard.recentsquares,chessboard.lastdir])
        newboard.MovePiece(moveTuple,skipsq=True)
        retval = self.IsInCheck(newboard)
        return retval

    def IsInCheck(self,chessboard):
        # Now we're checking for any black moves that take the king. We want to consider the opponent of "color"'s moves.
        chessboard.Rotate(skipsq=True)

        check=False
        for move in self.GetAllValidMoveNumbers(chessboard,skipCheckTest=True):
            newboard = ChessBoard([chessboard.board,[],0])
            newboard.MovePiece(move,skipsq=True)
            if 'k' not in newboard.board:
                check=True
                break

        chessboard.Rotate(skipsq=True)
        return check
            
    def ToTuple(self,x):
        return ChessBoard().ToTuple(x)

if __name__ == "__main__":
    from ChessBoard import ChessBoard
    cb = ChessBoard()
    rules = ChessRules()
    print(rules.IsCheckmate(cb.GetState(),"white"))
    print(rules.IsClearPath(cb.GetState(),(0,0),(5,5)))
    print(rules.IsClearPath(cb.GetState(),(1,1),(5,5)))
