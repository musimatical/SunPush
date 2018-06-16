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
 
class ChessRules:
    def IsCheckmate(self,board,color):
        #returns true if 'color' player is in checkmate
        #Call GetListOfValidMoves for each piece of current player
        #If there aren't any valid moves for any pieces, then return true
        if color == "black":
            board.Rotate()
        myColor = 'w'
        enemyColor = 'b'

        myColorValidMoves = [];
        for row in range(8):
            for col in range(8):
                #print(board.squares)
                piece = board.squares[row][col]
                if myColor in piece:
                    myColorValidMoves.extend(self.GetListOfValidMoves(board,(row,col)))

        if color == "black":
            board.Rotate()
        if len(myColorValidMoves) == 0:
            return True
        else:
            return False

    def GetListOfValidMoves(self,chessboard,fromTuple,skipCheckTest=False):
          #print(board,color,fromTuple,board[fromTuple[0]][fromTuple[1]])
          List=[]
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

          i=21+10*fromTuple[0]+fromTuple[1]
          p=newboard[i]
          if not p.isupper(): 
              raise TypeError('not an uppercase piece')
          for d in directions[p]:
              for j in count(i+d, d):
                  q = newboard[j]
                  # Stay inside the board
                  if newboard[j].isspace(): break
                  # No friendly captures
                  if q.isupper(): break
                  # Special pawn stuff
                  if p == 'P' and d in (N+W, N+E) and q == '.': break
                  if p == 'P' and d == N and q != '.': break
                  # No king pushes
                  if p == 'K' and q != '.': break
                  if p == 'K':
                      if newboard[j+N] == 'k': break
                      if newboard[j+W] == 'k': break
                      if newboard[j+S] == 'k': break
                      if newboard[j+E] == 'k': break
                      if newboard[j+N+W] == 'k': break
                      if newboard[j+N+E] == 'k': break
                      if newboard[j+S+W] == 'k': break
                      if newboard[j+S+E] == 'k': break
                  # No 'pushbacks'
                  if d == -chessboard.lastdir and chessboard.ToTuple(i) in chessboard.recentsquares: break
                  # Move it
                  if q.islower():
                      pieces=[p,q]
                      squares=[i,j]
                      while pieces[-1].isupper() or pieces[-1].islower():
                          squares.append(squares[-1]+d) 
                          pieces.append(newboard[squares[-1]])
                      for x in range(len(pieces)-1):
                          k=squares[x+1]
                          if pieces[x].lower()=='k' and pieces[x+1]!=' ' and pieces[x+1]!='\n':
                              if newboard[k+N].swapcase() == pieces[x]: break
                              if newboard[k+W].swapcase() == pieces[x]: break
                              if newboard[k+S].swapcase() == pieces[x]: break
                              if newboard[k+E].swapcase() == pieces[x]: break
                              if newboard[k+N+W].swapcase() == pieces[x]: break
                              if newboard[k+N+E].swapcase() == pieces[x]: break
                              if newboard[k+S+W].swapcase() == pieces[x]: break
                              if newboard[k+S+E].swapcase() == pieces[x]: break
                              #checking for king-on-king contact
                          #if d == -chessboard.lastdir and pieces[x].isupper():
                              #if chessboard.oldboard[k] == pieces[x] and newboard[k].islower():
                                  # we have pushback later on in the push                                    
                                  #break
                      else:
                          if not skipCheckTest:
                              if self.DoesMovePutPlayerInCheck(chessboard,'white',fromTuple,chessboard.ToTuple(j)): break
                          List.append(chessboard.ToTuple(j))
                          #all clear, add to list of moves
                      break
                      #don't look any further in this direction, we already hit something
                  else:
                      if not skipCheckTest:
                          if self.DoesMovePutPlayerInCheck(chessboard,'white',fromTuple,chessboard.ToTuple(j)): break
                      List.append(chessboard.ToTuple(j))
                  if p in ('P', 'N', 'K', 'Q'): break #these pieces only move one unit, don't check further
          return List
          
    def DoesMovePutPlayerInCheck(self,board,color,fromTuple,toTuple):
        #return False
        newboard = copy.deepcopy(board)
        newboard.MovePiece((fromTuple,toTuple),color)
        retval = self.IsInCheck(newboard,'white')
        return retval

    def IsInCheck(self,board,color):
        if color=='white':
            board.Rotate()

        check=False
        for row in range(8):
            for col in range(8):
                #print(board.squares)
                piece = board.squares[row][col]
                if 'w' in piece:
                    for move in self.GetListOfValidMoves(board,(row,col),skipCheckTest=True):
                        newboard = copy.deepcopy(board)
                        newboard.MovePiece(((row,col),move),'white')
                        if 'k' not in newboard.board:
                            check=True
                            break

        if color=='white':
            board.Rotate()
        return check

    def IsClearPath(self,board,fromTuple,toTuple):
        #Return true if there is nothing in a straight line between fromTuple and toTuple, non-inclusive
        #Direction could be +/- vertical, +/- horizontal, +/- diagonal
        fromSquare_r = fromTuple[0]
        fromSquare_c = fromTuple[1]
        toSquare_r = toTuple[0]
        toSquare_c = toTuple[1]
        fromPiece = board[fromSquare_r][fromSquare_c]

        if abs(fromSquare_r - toSquare_r) <= 1 and abs(fromSquare_c - toSquare_c) <= 1:
            #The base case: just one square apart
            return True
        else:
            if toSquare_r > fromSquare_r and toSquare_c == fromSquare_c:
                #vertical +
                newTuple = (fromSquare_r+1,fromSquare_c)
            elif toSquare_r < fromSquare_r and toSquare_c == fromSquare_c:
                #vertical -
                newTuple = (fromSquare_r-1,fromSquare_c)
            elif toSquare_r == fromSquare_r and toSquare_c > fromSquare_c:
                #horizontal +
                newTuple = (fromSquare_r,fromSquare_c+1)
            elif toSquare_r == fromSquare_r and toSquare_c < fromSquare_c:
                #horizontal -
                newTuple = (fromSquare_r,fromSquare_c-1)
            elif toSquare_r > fromSquare_r and toSquare_c > fromSquare_c:
                #diagonal "SE"
                newTuple = (fromSquare_r+1,fromSquare_c+1)
            elif toSquare_r > fromSquare_r and toSquare_c < fromSquare_c:
                #diagonal "SW"
                newTuple = (fromSquare_r+1,fromSquare_c-1)
            elif toSquare_r < fromSquare_r and toSquare_c > fromSquare_c:
                #diagonal "NE"
                newTuple = (fromSquare_r-1,fromSquare_c+1)
            elif toSquare_r < fromSquare_r and toSquare_c < fromSquare_c:
                #diagonal "NW"
                newTuple = (fromSquare_r-1,fromSquare_c-1)

        if board[newTuple[0]][newTuple[1]] != 'e':
            return False
        else:
            return self.IsClearPath(board,newTuple,toTuple)
            
if __name__ == "__main__":
    from ChessBoard import ChessBoard
    cb = ChessBoard()
    rules = ChessRules()
    print(rules.IsCheckmate(cb.GetState(),"white"))
    print(rules.IsClearPath(cb.GetState(),(0,0),(5,5)))
    print(rules.IsClearPath(cb.GetState(),(1,1),(5,5)))
