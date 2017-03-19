import math
Valid=False
peterstest = ''
xfrom=0
xto=0
yfrom=0
yto=0
CurrentPiece=''
def DisplayBoard(Board):
		print '  1 2 3 4 5 6 7 8'
		for xvar in range(8):
				peterstest = ''
				peterstest += str(xvar+1)
				for var in range(8):
						peterstest += '|'
						peterstest += str(Board[xvar*8+var])
				peterstest+='|'
				print peterstest
		print ' '

def InitialiseGame():
		Board=[]
		for x in range(64):
				Board.append(' ')
		Board[0]='r'
		Board[7]='r'
		Board[1]='n'
		Board[6]='n'
		Board[2]='b'
		Board[5]='b'
		Board[3]='q'
		Board[4]='k'
		Board[56]='R'
		Board[63]='R'
		Board[57]='N'
		Board[62]='N'
		Board[58]='B'
		Board[61]='B'
		Board[59]='Q'
		Board[60]='K'
		for y in range (8):
				Board[y+8]='p'
				Board[y+48]='P'
		return Board

def InputMove(Board):
		xfrom=raw_input('Please enter the row of the piece you would like to move: ')
		yfrom=raw_input('Please enter the column of the piece you would like to move: ')
		xto=raw_input('Please enter the row of the position you would like to move to: ')
		yto=raw_input('Please enter the column of the position you would like to move to: ')
		valid=["1","2","3","4","5","6","7","8"]
		if xfrom in valid and yfrom in valid and xto in valid and yto in valid:
				xfrom=int(xfrom)
				yfrom=int(yfrom)
				xto=int(xto)
				yto=int(yto)
		elif xfrom=='RESTART':
			return 'restart'
		else:
				return 'error'

		CurrentPiece=Board[8*(xfrom-1)+yfrom-1]
		return (((xfrom, yfrom), (xto, yto)),CurrentPiece)

def get_xfrom(position):
		return position[0][0][0]
		ally
def get_xto(position):
		return position[0][1][0]

def get_yfrom(position):
		return position[0][0][1]

def get_yto(position):
		return position[0][1][1]

def get_CP(position):
		return position[1][0][0]

def Occupied(x, y, CurrentPiece, Board):
		white = ["K", "Q", "P", "N", "B", "R"]
		black = ["k", "q", "p", "n", "b", "r"]
		pos=8*x+y-9
		if pos<(0) or pos>(63):
				return 'blank'
		if Board[pos] in white:
				if CurrentPiece in white:
						return 'ally'
				if CurrentPiece in black:
						return 'enemy'
		elif Board[pos] in black:
				if CurrentPiece in white:
						return 'enemy'
				if CurrentPiece in black:
						return 'ally'
		else:
				return 'blank'

def ValidateMovement(CurrentPieceX,Xfrom,Yfrom,Xto,Yto, xBoard):
		global WKingMoved
		global BKingMoved
		if Xfrom==Xto and Yfrom==Yto:
				return False
		if CurrentPieceX=='Q' or CurrentPieceX=='q':
				if Xfrom==Xto or Yfrom==Yto:
						return True
			#	 print 'queen values:'
			#	print (Xfrom-Xto)
			 #	print (Yfrom-Yto)
				if math.fabs(Xfrom-Xto)==math.fabs(Yfrom-Yto):
						return True
		if CurrentPieceX=='P':
				if Xfrom==7 and Xto==5 and Yto==Yfrom and Occupied(Xto, Yto, CurrentPieceX, xBoard)=='blank' :
						return True
				if Xto==Xfrom-1 and Yto==Yfrom and Occupied(Xto, Yto, CurrentPieceX, xBoard)=='blank' :
						return True
				if Occupied(Xfrom-1, Yfrom-1, CurrentPieceX, xBoard)=='enemy' and Xto==Xfrom-1 and Yto==Yfrom-1:
						return True
				if Occupied(Xfrom-1, Yfrom+1, CurrentPieceX, xBoard)=='enemy' and Xto==Xfrom-1 and Yto==Yfrom+1:
						return True
		if CurrentPieceX=='p':
				if Occupied(Xfrom+1, Yfrom-1, CurrentPieceX, xBoard)=='enemy' and Xto==Xfrom+1 and Yto==Yfrom-1:
						return True
				if Occupied(Xfrom+1, Yfrom+1, CurrentPieceX, xBoard)=='enemy' and Xto==Xfrom+1 and Yto==Yfrom+1:
						return True
				if Xfrom==2 and Xto==4 and Yto==Yfrom and Occupied(Xto, Yto, CurrentPieceX, xBoard)=='blank':
						return True
				if Xto==Xfrom+1 and Yto==Yfrom and Occupied(Xto, Yto, CurrentPieceX, xBoard)=='blank':
						return True
		if CurrentPieceX=='K':
				print 'a'
				if WKingMoved==False and Xfrom==8 and Yfrom==5 and Xto==8 and WhiteCheck(xBoard)==False:
						print 'b'
						aBoard=xBoard[:]
						if Occupied(8,6,'K', xBoard)=='blank':
								aBoard=MovePiece('K',8,5,8,6,aBoard)
								if Yto==7 and xBoard[63]=='R' and Occupied(8,7,'K', xBoard)=='blank' and WhiteCheck(aBoard)==False:
										WKingMoved=True
										return True
						bBoard=xBoard[:]
						if Occupied(8,4,'K', xBoard)=='blank':
								bBoard=MovePiece('K',8,5,8,4,bBoard)
								cBoard=xBoard[:]
								if Occupied(8,3,'K', xBoard)=='blank':
										cBoard=MovePiece('K',8,5,8,3,cBoard)
										if Yto==2 and xBoard[56]=='R' and Occupied(8,2,'K', xBoard)=='blank' and WhiteCheck(bBoard)==False and WhiteCheck(cBoard)==False:
												WKingMoved=True
												return True

				if math.fabs(Xfrom-Xto)<=1 and math.fabs(Yfrom-Yto)<=1 and math.fabs(Yfrom-Yto)+math.fabs(Xfrom-Xto)>=1:
						print 'c'
						WKingMoved=True
						return True
		if CurrentPieceX=='k':
				if BKingMoved==False and Xfrom==1 and Yfrom==5 and Xto==1 and BlackCheck(xBoard)==False:
						if Yto==7 and xBoard[8]=='R' and Occupied(1,7,'K', xBoard)=='blank' and Occupied(1,6,'K', xBoard)=='blank':
								BKingMoved=True
								return True
						if Yto==2 and xBoard[1]=='R' and Occupied(1,4,'K', xBoard)=='blank' and Occupied(1,3,'K', xBoard)=='blank' and Occupied(1,2,'K')=='blank':
								BKingMoved=True
								return True
				if math.fabs(Xfrom-Xto)<=1 and math.fabs(Yfrom-Yto)<=1 and math.fabs(Yfrom-Yto)+math.fabs(Xfrom-Xto)>=1:
						BKingMoved=True
						return True
		if CurrentPieceX=='N' or CurrentPieceX=='n':
				if math.fabs((Xfrom-Xto)*(Yfrom-Yto))==2:
						return True
		if CurrentPieceX=='B' or CurrentPieceX=='b':
			#	 print 'bishop alert'
		#		 print math.fabs(Xfrom-Xto)
			#	 print math.fabs(Yfrom-Yto)
				if math.fabs(Xfrom-Xto)==math.fabs(Yfrom-Yto):
						return True
		if CurrentPieceX=='R' or CurrentPieceX=='r':
				if Xfrom==Xto or Yfrom==Yto:
						return True
		return False

def CollisionCheck(CurrentPieceX,Xfrom,Yfrom,Xto,Yto, xBoard):
		if (CurrentPieceX=='P' or CurrentPieceX=='p') and math.fabs(Xto-Xfrom)==2 and Occupied((Xto+Xfrom)/2,Yto,CurrentPieceX, xBoard)!='blank':
				return True
		for x in range (7):
				x=x+1
				if x<math.fabs(Yto-Yfrom) and (Xto!=Xfrom and Yto!=Yfrom):
					  #  print math.fabs(Yto-Yfrom)
						if Xfrom<Xto and Yfrom<Yto:
								occupied=Occupied(Xfrom+x,Yfrom+x,CurrentPieceX, xBoard)
						if Xfrom<Xto and Yfrom>Yto:
								occupied=Occupied(Xfrom+x,Yfrom-x,CurrentPieceX, xBoard)
						if Xfrom>Xto and Yfrom<Yto:
								occupied=Occupied(Xfrom-x,Yfrom+x,CurrentPieceX, xBoard)
						if Xfrom>Xto and Yfrom>Yto:
								occupied=Occupied(Xfrom-x,Yfrom-x,CurrentPieceX, xBoard)
						 #		print (Xfrom, Yfrom)
						  #	  print occupied
						if (CurrentPieceX=='B' or CurrentPieceX=='b' or CurrentPieceX=='Q' or CurrentPieceX=='q') and x<math.fabs(Xfrom-Xto) and occupied !='blank':
								return True

		for x in range(7):
				x=x+1
				if x<math.fabs((Xfrom-Xto)+(Yfrom-Yto)) and (Xto==Xfrom or Yto==Yfrom):
						if Xto==Xfrom and Yfrom<Yto:
								occupied=Occupied(Xfrom, Yfrom+x, CurrentPieceX, xBoard)
						if Xto==Xfrom and Yfrom>Yto:
								occupied=Occupied(Xfrom, Yfrom-x, CurrentPieceX, xBoard)
						if Yto==Yfrom and Xfrom<Xto:
								occupied=Occupied(Xfrom+x, Yfrom, CurrentPieceX, xBoard)
						if Yto==Yfrom and Xfrom>Xto:
								occupied=Occupied(Xfrom-x, Yfrom, CurrentPieceX, xBoard)
						if (CurrentPieceX=='R' or CurrentPieceX=='r' or CurrentPieceX=='Q' or CurrentPieceX=='q') and occupied!='blank':
								return True
		return False

def MovePiece(CurrentPieceX,Xfrom,Yfrom,Xto,Yto,xBoard):
		#print (xBoard[39],'MPT',Yto)
		NewPiece=' '
		if (CurrentPieceX=='P' and Xto==1) or (CurrentPieceX=='p' and Xto==8):
				val=False
				while val==False:
						NewPiece=raw_input('Your pawn has reached the end! \nPlease enter the type of piece you would like it to be upgraded into. Q for queen, K for knight, B for bishop and R for rook. ')
						if NewPiece=='Q' or NewPiece=='K' or NewPiece=='R' or NewPiece=='B':
								val=True
								break
				print 'Your entry was invalid. Please try again.'
				if CurrentPieceX=='P':
						CurrentPieceX=NewPiece
				if CurrentPieceX=='p':
						CurrentPieceX=NewPiece.lower()
		if CurrentPieceX=='K' and xfrom==8 and xto==8 and yfrom==5:
				if yto==7:
						MovePiece('R',8,8,8,6,xBoard)
				if yto==2:
						MovePiece('R',8,1,8,3,xBoard)
		if CurrentPieceX=='k' and xfrom==1 and xto==1 and yfrom==5:
				if yto==7:
						MovePiece('r',1,8,1,6,xBoard)
				if yto==2:
						MovePiece('r',1,1,1,3,xBoard)
		xBoard[8*Xto+Yto-9]=CurrentPieceX
		xBoard[8*Xfrom+Yfrom-9]=' '
		#print (xBoard[39],'MPB')
		return xBoard

def LegalMove(a, xBoard):
		CP=get_CP(a)
		xfrom=get_xfrom(a)
		yfrom=get_yfrom(a)
		xto=get_xto(a)
		yto=get_yto(a)
		if CollisionCheck(CP,xfrom,yfrom,xto,yto,xBoard)==True :
				#print 'collided'
				return False
		if Occupied(xto,yto,CP,xBoard)=='ally':
				#print 'occupied'
				return False
		if ValidateMovement(CP,xfrom,yfrom,xto,yto,xBoard)==False:
				#print 'invalid'
				return False
		return True

def WhiteCheck(Board):
		#print (Board[39],'WC')
		black=["k", "q", "p", "n", "b", "r"]
		for x in range(8):
				x+=1
				for y in range(8):
						y+=1
						if Board[8*x+y-9]=='K':
								wking=(x,y)
								# print 'wking is'+str(wking)
		for x in range(8):
				x+=1
				for y in range(8):
						y+=1
						if Board[8*x+y-9] in black:
								#print Board[8*x+y-9]
								#print(x,y)
								if LegalMove((((x,y), wking),Board[8*x+y-9]), Board):
										return True
		return False

def BlackCheck(xBoard):
		white = ["K", "Q", "P", "N", "B", "R"]
		for x in range(8):
				x+=1
				for y in range(8):
						y+=1
						if xBoard[8*x+y-9]=='k':
								bking=(x,y)
							  #  print 'bking is'+str(bking)
		for x in range(8):
				x+=1
				for y in range(8):
						y+=1
						if xBoard[8*x+y-9] in white:
						 #		print Board[8*x+y]
								if LegalMove((((x,y), bking),xBoard[8*x+y-9]), xBoard):
										return True
		return False

def BlackCheckmate(xBoard):
		if BlackCheck(xBoard)==False:
				return False
		black=["k", "q", "p", "n", "b", "r"]
		for xf in range (8):
				xf+=1
				for yf in range (8):
						yf+=1
						CP=xBoard[8*xf+yf-9]
						if (CP in black):
								for xt in range (8):
										xt+=1
										for yt in range (8):
												yt+=1
												if LegalMove((((xf,yf),(xt,yt)),CP), xBoard)==True:
														CheckBoard=xBoard[:]
														CheckBoard=MovePiece(CP,xf,yf,xt,yt,CheckBoard)
														if BlackCheck(CheckBoard)==False:
																return False
		return True

def WhiteCheckmate(xBoard):
		if WhiteCheck(xBoard)==False:
				return False
		white = ["K", "Q", "P", "N", "B", "R"]
		for xf in range (8):
				xf+=1
				for yf in range (8):
						yf+=1
						CP=xBoard[8*xf+yf-9]
						if (CP in white):
								for xt in range (8):
										xt+=1
										for yt in range (8):
												yt+=1
												if LegalMove((((xf,yf),(xt,yt)),CP), xBoard)==True:
														CheckBoard=xBoard[:]
														CheckBoard=MovePiece(CP,xf,yf,xt,yt,CheckBoard)
														x=WhiteCheck(CheckBoard)
														if x==False:
																CheckBoard=xBoard[:]
																#print (xf, yf, xt, yt)
																return False
														else:
																CheckBoard=xBoard[:]
		return True

def WhiteTurn(Board):
		DisplayBoard(Board)
		print "It is White's Turn."
		if WhiteCheck(Board)==True:
				print 'You are in check.'
		Valid=True
		a = InputMove(Board)
		black = ["k", "q", "p", "n", "b", "r"]
		if a == 'restart':
			return 'gg'
		if a != 'error':
				if LegalMove(a, Board)==True and (get_CP(a) not in black):
						MovedBoard=Board[:]
						MovedBoard=MovePiece(get_CP(a),get_xfrom(a),get_yfrom(a),get_xto(a),get_yto(a),MovedBoard)
						if WhiteCheck(MovedBoard)==True:
								if WhiteCheck(Board)==False:
										print 'You are moving into check. Please try again.'
								if WhiteCheck(Board)==True:
										print 'You are still in check. Please try again.'
								MovedBoard=''
								return WhiteTurn(Board)
						else:
								Board=MovedBoard[:]
								return Board
				else:
						print 'Your move is invalid. Please try again.'
						return WhiteTurn(Board)
		else:
				print 'Please enter numbers from 1 to 8.'
				return WhiteTurn(Board)

def BlackTurn(Board):
		DisplayBoard(Board)
		print "It is Black's Turn."
		if BlackCheck(Board)==True:
				print 'You are in check.'
		Valid=True
		a = InputMove(Board)
		if a == 'restart':
			return 'gg'
		white = ["K", "Q", "P", "N", "B", "R"]
		if a != 'error':
				if LegalMove(a, Board)==True and (get_CP(a) not in white):
						MovedBoard=Board[:]
						MovedBoard=MovePiece(get_CP(a),get_xfrom(a),get_yfrom(a),get_xto(a),get_yto(a),MovedBoard)
						if BlackCheck(MovedBoard)==True:
								if BlackCheck(Board)==False:
										print 'You are moving into check. Please try again.'
								if BlackCheck(Board)==True:
										print 'You are still in check. Please try again.'
								MovedBoard=''
								return BlackTurn(Board)
						else:
								Board=MovedBoard[:]
								return Board
				else:
						print 'Your move is invalid. Please try again.'
						return BlackTurn(Board)
		else:
				print 'Please enter numbers from 1 to 8.'
				return BlackTurn(Board)

def WCannotMove(xBoard):
		if WhiteCheck(xBoard)==True:
				return False
		white = ["K", "Q", "P", "N", "B", "R"]
		for xf in range (8):
				xf+=1
				for yf in range (8):
						yf+=1
						CP=xBoard[8*xf+yf-9]
						if (CP in white):
								for xt in range (8):
										xt+=1
										for yt in range (8):
												yt+=1
												if LegalMove((((xf,yf),(xt,yt)),CP), xBoard)==True:
														#print (xf,yf,xt,yt,CP)
														return False
		return True

def BCannotMove(xBoard):
		if BlackCheck(xBoard)==True:
				return False
		black=["k", "q", "p", "n", "b", "r"]
		for xf in range (8):
				xf+=1
				for yf in range (8):
						yf+=1
						CP=xBoard[8*xf+yf-9]
						if (CP in black):
								for xt in range (8):
										xt+=1
										for yt in range (8):
												yt+=1
												if LegalMove((((xf,yf),(xt,yt)),CP), xBoard)==True:
														return False
		return True



PlayAgain=True
while PlayAgain==True:
	Stalemate=False
	WKingMoved=False
	BKingMoved=False
	Continue=True
	Board3=InitialiseGame()
	while Continue==True:
		if WhiteCheckmate(Board3)==False and WCannotMove(Board3)==False:
			Board2=WhiteTurn(Board3)
			if Board2=='gg':
				Continue=False
		else:
			Continue=False
		if Continue==False:
			break
		if BlackCheckmate(Board2)==False and BCannotMove(Board2)==False:
				Board3=BlackTurn(Board2)
				if Board3=='gg':
					Continue=False
		else:
			Continue=False
		if WCannotMove(Board3) or BCannotMove(Board2):
			Stalemate=True
		if BlackCheckmate(Board2)==True:
			DisplayBoard(Board2)
			print 'Checkmate! White player wins!'
		if WhiteCheckmate(Board3)==True:
			DisplayBoard(Board3)
			print 'Checkmate! Black player wins!'
		if Stalemate==True:
			print "It's a draw!"
	answer=raw_input('Would you like to play again? ')
	if answer=='yes' or answer=='Yes':
		PlayAgain=True
	else:
		PlayAgain=False
