import cProfile
from ChessAI import ChessAI_sunpush
from ChessBoard import ChessBoard

ai = ChessAI_sunpush('','')
chessboard = ChessBoard(0)
cProfile.run("for a in range(100000): ai.value(chessboard,(65,56))")
