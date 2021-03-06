#! /usr/bin/env python
"""
 Project: Python Chess
 File name: ChessBoard.py
 Description:  Board layout; contains what pieces are present
    at each square.
    
 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 """
 
import string

class ChessBoard(object):
    def __init__(self,setupType=4):
        self.squares = [['e','e','e','e','e','e','e','e'],\
                        ['e','e','e','e','e','e','e','e'],\
                        ['e','e','e','e','e','e','e','e'],\
                        ['e','e','e','e','e','e','e','e'],\
                        ['e','e','e','e','e','e','e','e'],\
                        ['e','e','e','e','e','e','e','e'],\
                        ['e','e','e','e','e','e','e','e'],\
                        ['e','e','e','e','e','e','e','e']]
                        
        if setupType == 0:
            self.squares[0] = ['bT','e','e','e','e','e','e','bT']
            self.squares[1] = ['e','bR','bB','bQ','bK','bB','bR','e']
            self.squares[2] = ['e','bP','e','e','e','e','bP','e']
            self.squares[3] = ['e','bP','bP','bP','bP','bP','bP','e']
            self.squares[4] = ['e','wP','wP','wP','wP','wP','wP','e']
            self.squares[5] = ['e','wP','e','e','e','e','wP','e']
            self.squares[6] = ['e','wR','wB','wQ','wK','wB','wR','e']
            self.squares[7] = ['wT','e','e','e','e','e','e','wT']

        #Debugging set-ups
        #Testing IsLegalMove
        if setupType == 1:
            self.squares[0] = ['bT','e','bB','e','e','bB','e','bT']
            self.squares[1] = ['e','bR','e','bQ','bK','e','bR','e']
            self.squares[2] = ['e','bP','e','e','e','e','bP','e']
            self.squares[3] = ['e','bP','bP','bP','bP','bP','bP','e']
            self.squares[4] = ['e','wP','wP','wP','wP','wP','wP','e']
            self.squares[5] = ['e','wP','e','e','e','e','wP','e']
            self.squares[6] = ['e','wR','e','wQ','wK','e','wR','e']
            self.squares[7] = ['wT','e','wB','e','e','wB','e','wT']

        #Testing IsInCheck, Checkmate
        if setupType == 2:
            self.squares[0] = ['e','e','e','e','e','e','wK','e']
            self.squares[1] = ['e','bP','e','e','e','e','e','e']
            self.squares[2] = ['wP','e','e','e','e','e','e','e']
            self.squares[3] = ['e','e','e','e','bR','e','e','e']
            self.squares[4] = ['e','e','bB','e','e','e','wR','e']
            self.squares[5] = ['wB','e','e','e','e','e','e','e']
            self.squares[6] = ['wB','bP','e','wR','wP','e','e','e']
            self.squares[7] = ['e','e','e','bK','wQ','e','wT','e']

        #Testing Defensive AI
        if setupType == 3:
            self.squares[0] = ['e','e','e','e','e','e','e','e']
            self.squares[1] = ['e','e','e','e','e','e','e','e']
            self.squares[2] = ['e','e','bB','e','e','e','e','e']
            self.squares[3] = ['e','e','e','e','e','e','e','e']
            self.squares[4] = ['e','e','e','wK','wP','bK','e','e']
            self.squares[5] = ['e','e','e','e','e','wP','e','e']
            self.squares[6] = ['e','e','e','e','e','e','wP','e']
            self.squares[7] = ['e','e','e','e','e','e','e','wQ']    
        if setupType == 5:
            self.squares[0] = ['e','e','e','e','e','e','e','e']
            self.squares[1] = ['e','wP','e','e','e','e','e','e']
            self.squares[2] = ['e','wK','e','e','e','e','e','e']
            self.squares[3] = ['e','e','e','e','e','e','e','e']
            self.squares[4] = ['e','e','e','e','e','e','e','e']
            self.squares[5] = ['e','bK','e','e','e','e','e','e']
            self.squares[6] = ['e','bP','e','e','e','e','e','e']
            self.squares[7] = ['e','e','e','e','e','e','e','e']
        if isinstance(setupType,list):
            self.board,self.recentsquares,self.lastdir = setupType
        elif setupType != 4:
            self.lastdir = 0
            self.recentsquares = []
            self.board = self.GetPushLayout()
            
    def ToTuple(self,x):
        return divmod(x-21,10)

    def ToNumber(self,Tuple):
        return 21+10*Tuple[0]+Tuple[1]

    def GetState(self):
        return self.squares
        
    def ConvertMoveTupleListToAlgebraicNotation(self,moveTupleList):    
        newTupleList = []
        for move in moveTupleList:
            newTupleList.append((self.ConvertToAlgebraicNotation(move[0]),self.ConvertToAlgebraicNotation(move[1])))
        return newTupleList
    
    def ConvertSquareListToAlgebraicNotation(self,List):
        newList = []
        for square in List:
            newList.append(self.ConvertToAlgebraicNotation(square))
        return newList

    def ConvertToAlgebraicNotation(self, pos):
        if isinstance(pos,int):
            row,col = self.ToTuple(pos)
        else:
            row,col = pos
        #Converts (row,col) to algebraic notation
        #(row,col) format used in Python Chess code starts at (0,0) in the upper left.
        #Algebraic notation starts in the lower left and uses "a..h" for the column.
        return  self.ConvertToAlgebraicNotation_col(col) + self.ConvertToAlgebraicNotation_row(row)
    
    def ConvertToAlgebraicNotation_row(self,row):
        #(row,col) format used in Python Chess code starts at (0,0) in the upper left.
        #Algebraic notation starts in the lower left and uses "a..h" for the column.    
        B = ['8','7','6','5','4','3','2','1']
        return B[row]
        
    def ConvertToAlgebraicNotation_col(self,col):
        #(row,col) format used in Python Chess code starts at (0,0) in the upper left.
        #Algebraic notation starts in the lower left and uses "a..h" for the column.    
        A = ['a','b','c','d','e','f','g','h']
        return A[col]

        
    def GetFullString(self,p):
        if 'b' in p:
            name = "black "
        else:
            name = "white "
            
        if 'P' in p:
            name = name + "pawn"
        if 'R' in p:
            name = name + "rook"
        if 'T' in p:
            name = name + "knight"
        if 'B' in p:
            name = name + "bishop"
        if 'Q' in p:
            name = name + "queen"
        if 'K' in p:
            name = name + "king"
            
        return name
        
    def GetPushLayout(self):
        white_dict = {'P':'P','T':'N','B':'B','Q':'Q','R':'R','K':'K'}
        piece_dict = {'w'+p:white_dict[p] for p in white_dict}
        piece_dict.update({'b'+p:white_dict[p].lower() for p in white_dict})
        piece_dict['e']='.'
        blankrow=[' ' for x in range(9)]+['\n']
        rows = [[' ']+[piece_dict[x] for x in row]+['\n'] for row in self.squares]
        newboard = [x for row in [blankrow]+[blankrow]+rows+[blankrow]+[blankrow] for x in row]
        newboard = ''.join(newboard)
        return newboard
    
    def GetSquaresLayout(self):
        white_dict = {'P':'P','N':'T','B':'B','Q':'Q','R':'R','K':'K'}
        piece_dict = {p:'w'+white_dict[p] for p in white_dict}
        piece_dict.update({p.lower():'b'+white_dict[p] for p in white_dict})
        piece_dict['.']='e'
        rows = [self.board[x:x+10] for x in xrange(20,100,10)]
        self.squares = [[piece_dict[x] for x in row if x not in ['\n',' ']] for row in rows]
    
    def Rotate(self,skipsq=False):
        self.board = self.board[::-1].swapcase()
        self.lastdir = -self.lastdir
        self.recentsquares = [119-x for x in self.recentsquares]
        if skipsq or not isinstance(self,SunpushBoard):
            pass

    def InvertSquare(self,sq):
        return (7-sq[0],7-sq[1])
        
    def MovePiece(self,moveTuple,color='white',skipsq=False,getMessage=False):
        #Note that color only matters for the message component of the function.
        self.recentsquares = []
        if isinstance(moveTuple[0],int):
            i = [moveTuple[0],moveTuple[1]]
        else:
            (from_r,from_c) = moveTuple[0]
            (to_r,to_c) = moveTuple[1]
            i = [21 + 10*from_r + from_c,21 + 10*to_r + to_c]
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
        board = ''.join([x for x in self.board])
        p = [board[j] for j in i]
        put = lambda board, i, p: board[:i] + p + board[i+1:]
        # Copy variables and reset ep and kp
        dist = i[1]-i[0]
        basedirection = max((x for x in directions[p[0]] if dist % x == 0 and dist//x > 0),key=lambda y: -dist//y )
        if not basedirection:
            raise TypeError("Wasn't a valid direction")
        #funnel 'outwards' searching for pieces to push, then push them on the way back 'in'
        while p[-1].isupper() or p[-1].islower():
            i.append(i[-1]+basedirection) 
            p.append(board[i[-1]])
        for x in range(len(p)-2):
            if not p[x+2].isspace():
                board = put(board, i[x+2], p[x+1])
        board = put(board, i[1], p[0])
        board = put(board, i[0], '.')
        # Special pawn stuff
        for x in range(len(p)-1):
            if p[x] == 'P' and A8 <= i[x+1] <= H8:
                board = put(board, i[x+1], moveTuple[2])
            if p[x] == 'p' and A1 <= i[x+1] <= H1:
                board = put(board, i[x+1], moveTuple[2].lower())
        self.recentsquares = i
        self.board = board
        self.lastdir = basedirection

        messageString = None
        if getMessage:
            moveTuple = tuple(self.ToTuple(y) for y in [moveTuple[0],moveTuple[1]])
            fromPiece_fullString = self.GetFullString(p[0])
            toPiece_fullString = self.GetFullString(p[1])
            from_string=self.ConvertToAlgebraicNotation(moveTuple[0])
            to_string=self.ConvertToAlgebraicNotation(moveTuple[1])
            if color=='black':
                fromPiece_fullString=fromPiece_fullString.replace('white','black')
                toPiece_fullString=toPiece_fullString.replace('black','white')
                from_string=self.ConvertToAlgebraicNotation(moveTuple[0])
                to_string=self.ConvertToAlgebraicNotation(moveTuple[1])
            if p[1] == '.':
                messageString = fromPiece_fullString+ " moves from "+from_string+" to "+to_string
            else:
                        messageString = fromPiece_fullString+ " from "+from_string+" pushes "+toPiece_fullString+" at "+to_string
            #capitalize first character of messageString
            messageString = string.upper(messageString[0])+messageString[1:len(messageString)]
            
        return messageString

if __name__ == "__main__":
    
    cb = ChessBoard(0)
    board1 = cb.GetState()
    for r in range(8):
        for c in range(8):
            print(board1[r][c]),
        print("")
        
    print("Move piece test...")
    cb.MovePiece(((4,4),(3,3)))
    board2 = cb.GetState()
    for r in range(8):
        for c in range(8):
            print(board2[r][c]),
        print("")

class SunpushBoard(ChessBoard):
    def __init__(self,board,squares,recentsquares,lastdir,score):
        self.board = board
        self.squares = squares
        self.recentsquares = recentsquares
        self.lastdir = lastdir
        self.score = score

    def Rotate(self):
        selfcopy = self.__copy__()
        super(SunpushBoard,selfcopy).Rotate(skipsq=True)
        selfcopy.score = -selfcopy.score
        return selfcopy

    def __copy__(self):
        return SunpushBoard(self.board,self.squares,self.recentsquares,self.lastdir,self.score)

    def MovePiece(self,move,ai):
        selfcopy = self.__copy__()
        selfcopy.score = self.score + ai.value(selfcopy,move)
        super(SunpushBoard,selfcopy).MovePiece(move)
        return selfcopy.Rotate()

    def GetScore(self,pst):
        self.score = sum([pst[self.board[x]][x] for x in range(20,100) if self.board[x] in ['N','Q','K','P','R','B']]) - sum([pst[self.board[x].upper()][x] for x in range(20,100) if self.board[x] in ['n','q','k','p','r','b']])

