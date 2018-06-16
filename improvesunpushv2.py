#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

from __future__ import print_function
from random import randint
from sunpush import (Position,bound,search,parse,render,print_pos)
import numpy as np


modifier=50
#increment to change score by if it's 'incorrect'

printing = True
#whether to show boards etc as we go

A1, H1, A8, H8 = 91, 98, 21, 28
MATE_VALUE = 30000
###############################################################################
# User interface
###############################################################################


def game(initial,message=''):
    pos = Position(initial, 0, 0, initial)
    global nummoves; nummoves = 0
    if printing:
        print_pos(pos)
        print(message)
        print(totalvalues)
    while nummoves<200:
        move, score = search(pos)
        pos = pos.move(move)
        nummoves += 1
        if printing:
            print_pos(pos.rotate())
            print(message)
            print(totalvalues)
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
            print(message)
            print(totalvalues)
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
                valid=False
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
    global totalvalues
    if score > 0 and Result == 'black':
        if printing:
            print('Black won unexpectedly!')
        Expected = False
        for x in range(119):
            if Initial[x].isupper():
                totalvalues[Initial[x]] -= (totalvalues[Initial[x]] * (2000/nummoves + abs(score)/50)/numpieces[0])/1000
            elif Initial[x].islower():
                totalvalues[Initial[x].upper()] += (totalvalues[Initial[x].upper()] *  (2000/nummoves + abs(score)/50)/numpieces[1])/1000
    elif score < 0 and Result == 'white':
        if printing:
            print('White won unexpectedly!')
        Expected = False
        for x in range(119):
            if Initial[x].isupper():
                totalvalues[Initial[x]] += (totalvalues[Initial[x]] * (2000/nummoves + abs(score)/50)/numpieces[0])/1000
            elif Initial[x].islower():
                totalvalues[Initial[x].upper()] -= (totalvalues[Initial[x].upper()] *  (2000/nummoves + abs(score)/50)/numpieces[1])/1000
    elif score > 0 and Result == 'white':
        if printing:
            print('White won (expectedly)')
    elif score < 0 and Result == 'black':
        if printing:
            print('Black won (expectedly)')
    scalefactor = totalvalues['P']/100.0
    for x in totalvalues:
        totalvalues[x] = int(totalvalues[x]/scalefactor)
    totalvalues['K'] = max(60000,9*totalvalues['Q']+2*totalvalues['R']+2*totalvalues['N']+2*totalvalues['B'])
    doc = open('OverallValues.txt','w')
    doc.write(str([totalvalues['P'],totalvalues['B'],totalvalues['N'],totalvalues['R'],totalvalues['Q'],totalvalues['K']]))
    doc.close()
    return Expected
    

def main():
    unexpected = 0
    expected = 0
    tooshort = 0
    toolong = 0
    NumberOfGamesToCheck=int(raw_input("How many puzzles would you like to create?"))
    #NODES_SEARCHED=int(raw_input("What level of depth? (suggested 10^2-10^4)"))
    x=0
    while x < NumberOfGamesToCheck:
        doc = open('InitialOverallValues.txt','r')
        InitVals = [int(x) for x in doc.readline().partition("[")[2].partition("]")[0].split(',')]
        doc.close()
        doc = open('OverallValues.txt','r')
        Vals = [int(x) for x in doc.readline().partition("[")[2].partition("]")[0].split(',')]
        doc.close()
        #messy, but it gets the job done. Searches for bits between '(' and ')' and converts to int list.
        global totalvalues
        totalvalues = {
            'P': Vals[0],
            'B': Vals[1],
            'N': Vals[2],
            'R': Vals[3],
            'Q': Vals[4],
            'K': Vals[5]
        }
        global diffvals
        diffvals = {
            'P': Vals[0]-InitVals[0],
            'B': Vals[1]-InitVals[1],
            'N': Vals[2]-InitVals[2],
            'R': Vals[3]-InitVals[3],
            'Q': Vals[4]-InitVals[4],
            'K': Vals[5]-InitVals[5]
        }
        doc = open('OriginalPieceValues.txt','r')
        PVals = [int(x) for x in doc.readline().partition("[")[2].partition("]")[0].split(', ')]
        BVals = [int(x) for x in doc.readline().partition("[")[2].partition("]")[0].split(', ')]
        NVals = [int(x) for x in doc.readline().partition("[")[2].partition("]")[0].split(', ')]
        RVals = [int(x) for x in doc.readline().partition("[")[2].partition("]")[0].split(', ')]
        QVals = [int(x) for x in doc.readline().partition("[")[2].partition("]")[0].split(', ')]
        KVals = [int(x) for x in doc.readline().partition("[")[2].partition("]")[0].split(', ')]
        #messy, but it gets the job done. Searches for bits between '(' and ')' and converts to int list.
        global pst        
        pst = {
            'P': [np.sign(x)*(x+diffvals['P']) for x in PVals],
            'B': [np.sign(x)*(x+diffvals['B']) for x in BVals],
            'N': [np.sign(x)*(x+diffvals['N']) for x in NVals],
            'R': [np.sign(x)*(x+diffvals['R']) for x in RVals],
            'Q': [np.sign(x)*(x+diffvals['Q']) for x in QVals],
            'K': [np.sign(x)*(x+diffvals['K']) for x in KVals],
        }
        doc.close()
        #score = 100000
        #while abs(score)>1500:
            #Initial,score = RandomInitial()
        Initial,score,numpieces = RandomInitial()
        message = '|exp='+str(expected)+'|unexp='+str(unexpected)+'|long='+str(toolong)+'|short='+str(tooshort)+'|'
        Result,nummoves = game(Initial,message)
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
                x+=1
        else:
            tooshort+=1
            if printing:
                print(Result+' won too quickly')
        #x+=1
if __name__ == '__main__':
    main()
