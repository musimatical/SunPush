#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
from __future__ import print_function
import pickle
from random import randint
from numpy import sign
from sunpush import (Position,bound,search,parse,render,print_pos)
from updatevals import (update,upd)


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
    maxn = 1000;
    global nummoves; nummoves = 0
    if printing:
        print_pos(pos)
        print(message)
    while nummoves<200:
        move, score = search(pos,maxn)
        pos = pos.move(move)
        nummoves += 1
        if printing:
            print_pos(pos.rotate())
            print(message)
        if score <= -MATE_VALUE:
            return 'black',nummoves
            break
        if score >= MATE_VALUE:
            return 'white',nummoves       
            break
        # Fire up the engine to look for a move.
        move, score = search(pos,maxn)
        pos = pos.move(move)
        nummoves += 1
        if printing:
            print_pos(pos)
            print(message)
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
    
def ValueModify(Initial,score,newscore,numpieces):
    global modifier
    f=open('PieceValues.pckl','rb')
    P1,P2,P3,P4,P5,P6,P7,P8,Pa,Pb,Pc,Pd,K11,K12,K13,K14,K22,K23,K24,K33,K34,K44,N2,N3,N4,N5,N6,N8,B7,B9,B11,B13,Q7,Q9,Q11,Q13,R1,R2,R3,R4=pickle.load(f)
    f.close()
    Outcome={-1:'Unexpected',0:'Draw',1:'Expected'}
    Expected = sign(score*newscore) #if score and newscore are the same sign
    if abs(newscore)>=MATE_VALUE:
        return 'Mate'
    for x in range(119):
        change=0
        if Initial[x].isupper():
            change = ((newscore-score)/numpieces[0])/modifier #if the calculation improved the score, white goes up
            pos=render(x)
        elif Initial[x].islower():
            change = ((score-newscore)/numpieces[1])/modifier #if the calculation degraded the score, black goes up
            pos=render(119-x)
        if change!=0:
            piece=Initial[x].upper()
            row=int(pos[1:])
            col={'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8}.get(pos[0])
            if piece=='P':
                a=int(4.5-abs(4.5-col))
                if a==1:
                    Pa+=change
                elif a==2:
                    Pb+=change
                elif a==3:
                    Pc+=change
                elif a==4:
                    Pd+=change
                d=locals()#{'row':row,'change':change}
                var='P'+str(row)
            elif piece=='K':
                a=max(int(4.5-abs(4.5-col)),int(4.5-abs(4.5-row)))
                b=min(int(4.5-abs(4.5-col)),int(4.5-abs(4.5-row)))
                var='K'+str(b)+str(a)
            elif piece=='B':
                a=min(int(4.5-abs(4.5-col)),int(4.5-abs(4.5-row)))
                c={1:7,2:9,3:11,4:13}.get(a)
                d={'c':c,'change':change}
                var='B'+str(c)
            elif piece=='Q':
                a=min(int(4.5-abs(4.5-col)),int(4.5-abs(4.5-row)))
                b={1:7,2:9,3:11,4:13}.get(a)
                d={'b':b,'change':change}
                var='Q'+str(b)
            elif piece=='R':
                a=min(int(4.5-abs(4.5-col)),int(4.5-abs(4.5-row)))
                d={'a':a,'change':change}
                var='R'+str(a)
            elif piece=='N':
                a=max(int(4.5-abs(4.5-col)),int(4.5-abs(4.5-row)))
                b=min(int(4.5-abs(4.5-col)),int(4.5-abs(4.5-row)))
                c={11:2,12:3,13:4,14:4,22:4,23:5,24:6,33:8,34:8,44:8}.get(10*b+a)
                d={'c':c,'change':change}
                var='N'+str(c)
            [P1,P2,P3,P4,P5,P6,P7,P8,Pa,Pb,Pc,Pd,K11,K12,K13,K14,K22,K23,K24,K33,K34,K44,N2,N3,N4,N5,N6,N8,B7,B9,B11,B13,Q7,Q9,Q11,Q13,R1,R2,R3,R4]=upd(var,change,P1,P2,P3,P4,P5,P6,P7,P8,Pa,Pb,Pc,Pd,K11,K12,K13,K14,K22,K23,K24,K33,K34,K44,N2,N3,N4,N5,N6,N8,B7,B9,B11,B13,Q7,Q9,Q11,Q13,R1,R2,R3,R4)
    #renormalises K
    pst2={key: value for key, value in pst.items() if key is not 'K'}
    highscore=max(max(pst2[x]) for x in pst2)
    Kadd = max(max(60000,15*highscore) - min(K11,K12,K13,K14,K22,K23,K24,K33,K34,K44),0)
    [K11,K12,K13,K14,K22,K23,K24,K33,K34,K44] = [a+Kadd for a in [K11,K12,K13,K14,K22,K23,K24,K33,K34,K44]]
    doc = open('PieceValues.pckl','wb')
    pickle.dump([P1,P2,P3,P4,P5,P6,P7,P8,Pa,Pb,Pc,Pd,K11,K12,K13,K14,K22,K23,K24,K33,K34,K44,N2,N3,N4,N5,N6,N8,B7,B9,B11,B13,Q7,Q9,Q11,Q13,R1,R2,R3,R4],doc)
    doc.close()
    return Outcome.get(Expected)

def main():
    global modifier
    modifier=50
    try: 
        raw_input = input
    except NameError: 
        pass
    #NumberOfGamesToCheck=int(raw_input("How many puzzles would you like to create?"))
    NumberOfGamesToCheck=100000
    #NODES_SEARCHED=int(raw_input("What level of depth? (suggested 10^2-10^4)"))
    NODES_SEARCHED=1000
    x=0
    expected=0
    unexpected=0
    mate=0
    draw=0
    global pst
    while x < NumberOfGamesToCheck:
        
        pst = update()
        
        score = 100000
        while abs(score)>1500:
            Initial,score,numpieces = RandomInitial()
            #print_pos(Position(Initial, 0, 0, Initial))
            #print('Score = '+str(score))
        message = '|exp='+str(expected)+'|unexp='+str(unexpected)+'|'+str(mate)+'|'+str(draw)+'|'
        #Result,nummoves = game(Initial,message)
        pos=Position(Initial,0,0,Initial)
        move, newscore = search(pos,NODES_SEARCHED)
        exp = ValueModify(Initial,score,newscore,numpieces)
        print_pos(pos)
        print_pos(pos.move(move).rotate())
        print(message)
        print('score='+str(score)+', newscore='+str(newscore))
        #[print([int(y) for y in pst[z] if y!=0]) for z in pst]
        with open('PieceValues.pckl','rb') as f:
            print([int(z) for z in pickle.load(f)])
        #print(P1,P2,P3,P4,P5,P6,P7,P8,Pa,Pb,Pc,Pd,K11,K12,K13,K14,K22,K23,K24,K33,K34,K44,N2,N3,N4,N5,N6,N8,B7,B9,B11,B13,Q7,Q9,Q11,Q13,R1,R2,R3,R4)
        if exp=='Expected':
            expected+=1
        elif exp=='Unexpected':
            unexpected+=1
            x+=1
        elif exp=='Mate':
            mate+=1
        else:
            draw+=1
if __name__ == '__main__':
    main()
