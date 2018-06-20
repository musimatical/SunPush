# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 17:37:31 2017

@author: s4352483
"""
import re
import sys
import pickle
def update():    
    with open('PieceValues.pckl','rb') as f:
        P1,P2,P3,P4,P5,P6,P7,P8,Pa,Pb,Pc,Pd,K11,K12,K13,K14,K22,K23,K24,K33,K34,K44,N2,N3,N4,N5,N6,N8,B7,B9,B11,B13,Q7,Q9,Q11,Q13,R1,R2,R3,R4=pickle.load(f)
        f.close()
    pst={
    'P': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
     0, P8+Pa, P8+Pb, P8+Pc, P8+Pd, P8+Pd, P8+Pc, P8+Pb, P8+Pa, 0,
     0, P7+Pa, P7+Pb, P7+Pc, P7+Pd, P7+Pd, P7+Pc, P7+Pb, P7+Pa, 0,
     0, P6+Pa, P6+Pb, P6+Pc, P6+Pd, P6+Pd, P6+Pc, P6+Pb, P6+Pa, 0,
     0, P5+Pa, P5+Pb, P5+Pc, P5+Pd, P5+Pd, P5+Pc, P5+Pb, P5+Pa, 0,
     0, P4+Pa, P4+Pb, P4+Pc, P4+Pd, P4+Pd, P4+Pc, P4+Pb, P4+Pa, 0,
     0, P3+Pa, P3+Pb, P3+Pc, P3+Pd, P3+Pd, P3+Pc, P3+Pb, P3+Pa, 0,
     0, P2+Pa, P2+Pb, P2+Pc, P2+Pd, P2+Pd, P2+Pc, P2+Pb, P2+Pa, 0,
     0, P1+Pa, P1+Pb, P1+Pc, P1+Pd, P1+Pd, P1+Pc, P1+Pb, P1+Pa, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
     0, 0, 0, 0, 0, 0, 0, 0],
    'B': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, B7, B7, B7, B7, B7, B7, B7, B7, 0, 
     0,  B7, B9, B9, B9, B9, B9, B9, B7, 0, 
     0,  B7, B9, B11, B11, B11, B11, B9, B7, 0,  
     0,  B7, B9, B11, B13, B13, B11, B9, B7, 0,   
     0,  B7, B9, B11, B13, B13, B11, B9, B7, 0,   
     0,  B7, B9, B11, B11, B11, B11, B9, B7, 0,  
     0,  B7, B9, B9, B9, B9, B9, B9, B7, 0, 
     0,  B7, B7, B7, B7, B7, B7, B7, B7, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'N': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
     0, N2, N3, N4, N4, N4, N4, N3, N2, 0,
     0, N3, N4, N5, N6, N6, N5, N4, N3, 0,
     0, N4, N6, N8, N8, N8, N8, N6, N4, 0,
     0, N4, N6, N8, N8, N8, N8, N6, N4, 0,
     0, N4, N6, N8, N8, N8, N8, N6, N4, 0,
     0, N4, N6, N8, N8, N8, N8, N6, N4, 0,
     0, N3, N4, N5, N6, N6, N5, N4, N3, 0,
     0, N2, N3, N4, N4, N4, N4, N3, N2, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'R': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
     0, R1, R1, R1, R1, R1, R1, R1, R1, 0, 
     0,  R1, R2, R2, R2, R2, R2, R2, R1, 0, 
     0,  R1, R2, R3, R3, R3, R3, R2, R1, 0,  
     0,  R1, R2, R3, R4, R4, R3, R2, R1, 0,   
     0,  R1, R2, R3, R4, R4, R3, R2, R1, 0,   
     0,  R1, R2, R3, R3, R3, R3, R2, R1, 0,  
     0,  R1, R2, R2, R2, R2, R2, R2, R1, 0, 
     0,  R1, R1, R1, R1, R1, R1, R1, R1, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'Q': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
     0, Q7, Q7, Q7, Q7, Q7, Q7, Q7, Q7, 0, 
     0,  Q7, Q9, Q9, Q9, Q9, Q9, Q9, Q7, 0, 
     0,  Q7, Q9, Q11, Q11, Q11, Q11, Q9, Q7, 0,  
     0,  Q7, Q9, Q11, Q13, Q13, Q11, Q9, Q7, 0,   
     0,  Q7, Q9, Q11, Q13, Q13, Q11, Q9, Q7, 0,   
     0,  Q7, Q9, Q11, Q11, Q11, Q11, Q9, Q7, 0,  
     0,  Q7, Q9, Q9, Q9, Q9, Q9, Q9, Q7, 0, 
     0,  Q7, Q7, Q7, Q7, Q7, Q7, Q7, Q7, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'K': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
     0, K11, K12, K13, K14, K14, K13, K12, K11, 0,
     0, K12, K22, K23, K24, K24, K23, K22, K12, 0,
     0, K13, K23, K33, K34, K34, K33, K23, K13, 0,
     0, K14, K24, K34, K44, K14, K34, K24, K14, 0,
     0, K14, K24, K34, K44, K14, K34, K24, K14, 0,
     0, K13, K23, K33, K34, K34, K33, K23, K13, 0,
     0, K12, K22, K23, K24, K24, K23, K22, K12, 0,
     0, K11, K12, K13, K14, K14, K13, K12, K11, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
    return pst
    
def upd(var,change,P1,P2,P3,P4,P5,P6,P7,P8,Pa,Pb,Pc,Pd,K11,K12,K13,K14,K22,K23,K24,K33,K34,K44,N2,N3,N4,N5,N6,N8,B7,B9,B11,B13,Q7,Q9,Q11,Q13,R1,R2,R3,R4):
    if var=='P1':
        P1+=change
    if var=='P2':
        P2+=change
    if var=='P3':
        P3+=change
    if var=='P4':
        P4+=change
    if var=='P5':
        P5+=change
    if var=='P6':
        P6+=change
    if var=='P7':
        P7+=change
    if var=='P8':
        P8+=change
    if var=='K11':
        K11+=change
    if var=='K12':
        K12+=change
    if var=='K13':
        K13+=change
    if var=='K14':
        K14+=change
    if var=='K22':
        K22+=change
    if var=='K23':
        K23+=change
    if var=='K24':
        K24+=change
    if var=='K33':
        K33+=change
    if var=='K34':
        K34+=change
    if var=='K44':
        K44+=change
    if var=='N2':
        N2+=change
    if var=='N3':
        N3+=change
    if var=='N4':
        N4+=change
    if var=='N5':
        N5+=change
    if var=='N6':
        N6+=change
    if var=='N8':
        N8+=change
    if var=='B7':
        B7+=change
    if var=='B9':
        B9+=change
    if var=='B11':
        B11+=change
    if var=='B13':
        B13+=change
    if var=='Q7':
        Q7+=change
    if var=='Q9':
        Q9+=change
    if var=='Q11':
        Q11+=change
    if var=='Q13':
        Q13+=change
    if var=='R1':
        R1+=change
    if var=='R2':
        R2+=change
    if var=='R3':
        R3+=change
    if var=='R4':
        R4+=change
    return [P1,P2,P3,P4,P5,P6,P7,P8,Pa,Pb,Pc,Pd,K11,K12,K13,K14,K22,K23,K24,K33,K34,K44,N2,N3,N4,N5,N6,N8,B7,B9,B11,B13,Q7,Q9,Q11,Q13,R1,R2,R3,R4]
