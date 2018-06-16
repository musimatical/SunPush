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

class ChessBoard:
    def __init__(self,setupType=0):
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
            self.squares[0] = ['bR','bT','bB','bQ','bK','bB','bT','bR']
            self.squares[1] = ['e','e','e','e','e','e','e','e']
            self.squares[2] = ['e','e','e','e','e','e','e','e']
            self.squares[3] = ['e','e','e','e','e','e','e','e']
            self.squares[4] = ['e','e','e','e','e','e','e','e']
            self.squares[5] = ['e','e','e','e','e','e','e','e']
            self.squares[6] = ['wP','wP','wP','wP','wP','wP','wP','wP']
            self.squares[7] = ['wR','wT','wB','wQ','wK','wB','wT','wR']

        #Testing IsInCheck, Checkmate
        if setupType == 2:
            self.squares[0] = ['e','e','e','e','e','e','e','e']
            self.squares[1] = ['e','e','e','e','e','e','e','e']
            self.squares[2] = ['e','e','e','e','wK','e','e','e']
            self.squares[3] = ['e','e','e','e','bR','e','e','e']
            self.squares[4] = ['e','e','bB','e','e','e','wR','e']
            self.squares[5] = ['e','e','e','e','e','e','e','e']
            self.squares[6] = ['wB','e','wQ','wR','wP','e','e','e']
            self.squares[7] = ['e','e','e','bK','wQ','e','wT','e']

        #Testing Defensive AI
        if setupType == 3:
            self.squares[0] = ['e','e','e','e','e','e','e','e']
            self.squares[1] = ['e','e','e','e','e','e','e','e']
            self.squares[2] = ['e','e','e','e','bK','e','e','e']
            self.squares[3] = ['e','e','e','e','bR','e','e','e']
            self.squares[4] = ['e','e','bB','e','e','e','wR','e']
            self.squares[5] = ['e','e','e','e','e','e','e','e']
            self.squares[6] = ['e','e','e','e','e','e','e','e']
            self.squares[7] = ['e','e','e','wK','wQ','e','wT','e']    
        self.lastdir = 0
        self.recentsquares = []
        self.board = self.GetPushLayout()
        self.oldboard = self.board
        self.score = 0
            
    def ToTuple(self,x):
        return divmod(x-21,10)

    def GetState(self):
        return self.squares
        
    def ConvertMoveTupleListToAlgebraicNotation(self,moveTupleList):    
        newTupleList = []
        for move in moveTupleList:
            newTupleList.append((self.ConvertToAlgebraicNotation(move[0]),self.ConvertToAlgebraicNotation(move[1])))
        return newTupleList
    
    def ConvertSquareListToAlgebraicNotation(self,list):
        newList = []
        for square in list:
            newList.append(self.ConvertToAlgebraicNotation(square))
        return newList

    def ConvertToAlgebraicNotation(self, pos):
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
        newboard=[' ' for x in range(9)]
        newboard.append('\n')
        newboard.extend(newboard)
        for y in range(8):
            newboard.extend([' '])
            for x in self.squares[y]:
                if x=='e':
                    newboard.append('.')
                elif x[1]=='T':
                    newboard.append('N')
                else:
                    newboard.append(x[1])
                if x[0]=='b':
                    newboard[-1]=newboard[-1].swapcase()
            newboard.extend(['\n'])
        newboard.extend([' ' for x in range(9)])
        newboard.append('\n')
        newboard.extend([' ' for x in range(10)])
        newboard=''.join(newboard)
        return newboard
    
    def GetSquaresLayout(self):
        sq = []
        piece_dict = {'P':'P','N':'T','B':'B','Q':'Q','R':'R','K':'K','.':'e'}
        color_dict = {p:'w' for p in piece_dict}
        color_dict.update({p.lower():'b' for p in piece_dict})
        color_dict.update({'.':''})
        
        for x in self.board:
            if x not in ['\n',' ']:
                piece = color_dict[x] + piece_dict[x.upper()]
                if not sq:
                    sq.append([piece])
                elif len(sq[-1]) < 8:
                    sq[-1].append(piece)
                else:
                    sq.append([piece])
        self.squares = sq
    
    def ValueMove(self, move):
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
        for x in range(len(i)-1):
            if p[x] == 'P':
                if A8 <= i[x+1] <= H8:
                    score += pst['Q'][i[x+1]] - pst['P'][i[x]]
            if p[x] == 'q':
                if A1 <= i[x+1] <= H1:
                    score -= pst['B'][i[x+1]] - pst['P'][i[x]]
        return score
        
    def Rotate(self):
        self.board = self.board[::-1].swapcase()
        self.score = -self.score
        self.lastdir = -self.lastdir
        self.oldboard = self.oldboard[::-1].swapcase()
        self.GetSquaresLayout()
        
    def MovePiece(self,moveTuple,color):
        self.recentsquares = []
        (from_r,from_c),(to_r,to_c) = moveTuple
        fromPiece = self.squares[from_r][from_c]
        toPiece = self.squares[to_r][to_c]
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
        #if 'b' in fromPiece:
                #        raise TypeError('Not your piece')
        #    color = 'black'
        #    moveTuple = tuple(tuple(7-x for x in y) for y in moveTuple)
        #    (from_r,from_c),(to_r,to_c) = moveTuple
        #elif 'w' in fromPiece:
        #    color = 'white'
        #else:
        #    raise TypeError('Not a valid piece here')
            
        board = ''.join([x for x in self.board])
        i = [21 + 10*from_r + from_c,21 + 10*to_r + to_c]
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
            if p[x] == 'P':
                if A8 <= i[x+1] <= H8:
                    board = put(board, i[x+1], 'Q')
            if p[x] == 'p':
                if A1 <= i[x+1] <= H1:
                    board = put(board, i[x+1], 'b')
        if color=='white':
            self.recentsquares = [self.ToTuple(x) for x in i]
        else:
            self.recentsquares = [self.ToTuple(119-x) for x in i]
        self.oldboard = self.board
        self.board = board
        self.lastdir = basedirection
        self.GetSquaresLayout()
        
        fromPiece_fullString = self.GetFullString(fromPiece)
        toPiece_fullString = self.GetFullString(toPiece)
        from_string=self.ConvertToAlgebraicNotation(moveTuple[0])
        to_string=self.ConvertToAlgebraicNotation(moveTuple[1])
        if color=='black':
            fromPiece_fullString=fromPiece_fullString.replace('white','black')
            toPiece_fullString=toPiece_fullString.replace('black','white')
            moveTuple = tuple(tuple(7-x for x in y) for y in moveTuple)
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
