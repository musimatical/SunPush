PUSH CHESS RULES

Push chess is a chess variant in which the rules are modified as follows:

**Push**: Wherever a capture would be legal in regular chess, the piece that would be captured is instead pushed back in the direction of the original piece's movement (by one square, or one L-shape for the knight). If this collides with another piece, it too is pushed back. If a piece is pushed off the board, it is captured.

**No Immediate Pushbacks**: If a piece has just been pushed in a given direction, it cannot immediately move/push back in the opposite direction.

**Check**: Just as in normal chess, a move puts the opponent in Check if their king is in danger of being captured (pushed off the board) on the following turn. Checkmate occurs if the opponent cannot prevent immediate capture of the king.

**Stalemate**: The same rules for stalemate apply as in regular chess.

**Queen nerf**: The Queen cannot move more than one square at a time.

**King nerf**: The King cannot push or capture.

**No King Contact**: It is illegal for the two kings to be immediately adjacent to one another.

**Promotion**: Promotion acts as normal, with the following exception -- if you push an opponent's pawn to the back rank, then you decide how it promotes.

**Initial board setup**: Using many similar principles to that of regular chess, a new starting setup has been developed to delay conflict and provide a range of development options.


------------------------------------------------------------------------------------------------
sunpush.py runs the original text-based interface, featuring an AI engine called Sunpush which has been modified from an existing 'Sunfish' engine designed for regular chess.

PythonChessMain.py will run the game with a GUI, and the options for different AI and player configurations.

The ChessAI.py file contains a random AI and a Sunpush AI. The latter imports information from the sunpush.py file.

Currently the biggest obstacle to readability (and probably efficiency) is that I've somewhat hybridised the conventions for notation between Sunfish and PythonChess. There's a lot of unnecessary conversion between the the PythonChess style (in which 'wK' means white king, 'e' for empty, 'bT' for black knight, etc) and the Sunfish style (with 'K' for white king, '.' for empty, 'n' for black knight, etc.)

There's also a bit of doubling up between the sunpush file and the ChessRules file, because both of them implement the push chess rules but I may have made changes to one and not the other.

improvesunpush.py worked at one point, and it let the Sunpush AI play games against itself to try to improve its weighting for how valuable different pieces are in different positions (stored in PieceValues.txt).

Similarly, improvesunpushv2.py did the same thing, but it focused just on the value of pieces regardless of their position (which might actually be better because the other method seemed to "overfit" beyond the level of actual information it had).

Currently, the Sunpush AI uses position-dependent values for the King but position-independent values for all other pieces (because the King is so position dependent).

"openings.txt" contains information about the Sunpush AI's evaluation of different openings (although it should be noted this was evaluated before the **Queen nerf** rule was introduced).

TODO:
<<<<<<< HEAD
- Implement promotion menu instead of assuming the choices.
- Implement stalemate rules.
=======
>>>>>>> c7ff205a0a5b327cfb67a9728d45b79aa7d8c2ba
- Implement machine learning AI
