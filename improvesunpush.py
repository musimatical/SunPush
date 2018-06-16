#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

from __future__ import print_function
from random import randint
from sunpush import (Position,bound,search,parse,render,print_pos)


modifier=50
#increment to change score by if it's 'incorrect'

printing = True
#whether to show boards etc as we go

A1, H1, A8, H8 = 91, 98, 21, 28
MATE_VALUE = 30000
###############################################################################
# User interface
###############################################################################


def game(initial):
    pos = Position(initial, 0, 0, initial)
    global nummoves; nummoves = 0
    if printing:
        print_pos(pos)
        print(pst)
    while nummoves<500:
        move, score = search(pos)
        pos = pos.move(move)
        nummoves += 1
        if printing:
            print_pos(pos.rotate())
            print(pst)
        if score <= -MATE_VALUE:
            return 'black',nummoves
            break
        if score >= MATE_VALUE:
            return 'white',nummoves       
            break
        # Fire up the engine to look for a move.
        move, score = search(pos)
        pos = pos.move(move)
        nummoves += 1
        if printing:
            print_pos(pos)
            print(pst)
        if score <= -MATE_VALUE:
            return 'white',nummoves
            break
        if score >= MATE_VALUE:
            return 'black',nummoves    
            break
    return 'draw',nummoves

        # The black player moves from a rotated position, so we have to
        # 'back rotate' the move before printing it.
def RandomInitial():
    score=0
    numpieces=[0,0]
    global pst
    put = lambda board, i, p: board[:i] + p + board[i+1:]
    initial = (
    '         \n' #   0 -  9
    '         \n' #  10 - 19
    ' ........\n' #  20 - 29
    ' ........\n' #  30 - 39
    ' ........\n' #  40 - 49
    ' ........\n' #  50 - 59
    ' ........\n' #  60 - 69
    ' ........\n' #  70 - 79
    ' ........\n' #  80 - 89
    ' ........\n' #  90 - 99
    '         \n' # 100 -109
    '          '  # 110 -119
    )
    pieces = ['R','N','B','Q','K','B','N','R','P','P','P','P','P','P','P','P','p','p','p','p','p','p','p','p','r','n','b','q','k','b','n','r']
    for x in pieces:
        valid = False
        while valid == False:
            place = randint(0,119)
            if initial[place]==' ' and x!='K' and x!='k':
                valid=True
            elif initial[place]=='.' and not (x=='P' and A8<=place<=H8) and not (x=='p' and A1<=place<=H1):
                if x.isupper():
                    score+=pst[x][place]
                    numpieces[0]+=1
                else:
                    score-=pst[x.upper()][119-place]
                    numpieces[1]+=1
                initial = put(initial,place,x)
                valid=True
    return initial,score,numpieces
    
def ValueModify(Initial,score,Result,nummoves,numpieces):
    Expected = True
    global pst
    if score > 0 and Result == 'black':
        if printing:
            print('Black won unexpectedly!')
        Expected = False
        for x in range(119):
            if Initial[x].isupper():
                pst[Initial[x]][x] *= 1-(10/nummoves + abs(score)/10000)/numpieces[0]
            elif Initial[x].islower():
                pst[Initial[x].upper()][x] *= 1+(10/nummoves + abs(score)/10000)/numpieces[1]
    elif score < 0 and Result == 'white':
        if printing:
            print('White won unexpectedly!')
        Expected = False
        for x in range(119):
            if Initial[x].isupper():
                pst[Initial[x]][x] *= 1+(10/nummoves + abs(score)/10000)/numpieces[0]
            elif Initial[x].islower():
                pst[Initial[x].upper()][x] *= 1-(10/nummoves + abs(score)/10000)/numpieces[1]
    elif score > 0 and Result == 'white':
        if printing:
            print('White won (expectedly)')
    elif score < 0 and Result == 'black':
        if printing:
            print('Black won (expectedly)')
    doc = open('PieceValues.txt','w')
    doc.write(str(pst['P'])+'\n'+str(pst['B'])+'\n'+str(pst['N'])+'\n'+str(pst['R'])+'\n'+str(pst['Q'])+'\n'+str(pst['K']))
    doc.close()
    return Expected
    

def main():
    unexpected = 0
    expected = 0
    tooshort = 0
    toolong = 0
    NumberOfGamesToCheck=int(raw_input("How many puzzles would you like to create?"))
    #NODES_SEARCHED=int(raw_input("What level of depth? (suggested 10^2-10^4)"))
    for x in range (NumberOfGamesToCheck):
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
        doc.close()
        #score = 100000
        #while abs(score)>1500:
            #Initial,score = RandomInitial()
        Initial,score,numpieces = RandomInitial()
        Result,nummoves = game(Initial)
        if Result == 'draw':
            toolong+=1
            if printing:
                print('draw (game went on forever)')        
        elif nummoves>4:
            exp = ValueModify(Initial,score,Result,nummoves,numpieces)
            if exp:
                expected+=1
            else:
                unexpected+=1
        else:
            tooshort+=1
            if printing:
                print(Result+' won too quickly')
        print('|exp='+str(expected)+'|unexp='+str(unexpected)+'|long='+str(toolong)+'|short='+str(tooshort)+'|')

if __name__ == '__main__':
    main()
