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

**Initial board setup**: The standard chess setup doesn't work with these rules, because there's a quick forced mate. Using many similar principles to that of regular chess, a new starting setup has been developed to delay conflict and provide a range of development options.

------------------------------------------------------------------------------------------------
sunpush.py runs the original text-based interface, featuring an AI engine called Sunpush which has been modified from an existing 'Sunfish' engine designed for regular chess.

PythonChessMain.py will run the game with a GUI, and the options for different AI and player configurations.

The ChessAI.py file contains a random AI and a Sunpush AI. The latter is mostly the same as the one in sunpush.py.

Currently the biggest obstacle to readability (and probably efficiency) is that I've somewhat hybridised the conventions for notation between Sunfish and PythonChess. There's a lot of unnecessary conversion between the the PythonChess style (in which 'wK' means white king, 'e' for empty, 'bT' for black knight, etc) and the Sunfish style (with 'K' for white king, '.' for empty, 'n' for black knight, etc.)
**UPDATE**: I'm gradually getting rid of the PythonChess style, currently it only survives in the context of (1) the GUI and (2) the initialisation of the ChessBoard. Its main benefit is readability, which is useful in these contexts, so I might leave them as is.

There's also a bit of doubling up between the sunpush file and the ChessRules file, because both of them implement the push chess rules but I may have made changes to one and not the other. **Fixed**

improvesunpush.py worked at one point, and it let the Sunpush AI play games against itself to try to improve its weighting for how valuable different pieces are in different positions (stored in PieceValues.txt). Similarly, improvesunpushv2.py did the same thing, but it focused just on the value of pieces regardless of their position (which might actually be better because the other method seemed to "overfit" beyond the level of actual information it had). Both of these were flawed because they didn't actually update the values as they went, and I'm not convinced that the idea is worth salvaging. A proper machine-learning AI that doesn't refer to "points" like these ones do would be much better.

Currently, the Sunpush AI uses position-dependent values for the King and pawns but position-independent values for all other pieces.

"openings.txt" contains information about the Sunpush AI's evaluation of different openings (although it should be noted this was evaluated before the **Queen nerf** rule was introduced).

TODO:
- Implement promotion menu instead of assuming the choices. **DONE**
- Implement stalemate rules. **DONE**
- Redo text in the right panel to be more useful+readable.
- Make promotion choice occur in a pop-out window.
- Implement machine learning AI.
- SunPush seems to not avoid mate in X even when evaluation depth exceeds X.
- Finish consolidating the two notations.
- Difficulty setting options on startup.
- Implement updates to Sunfish engine (introduced since SunPush                                              started).

Credits:
Sunfish, used for engine: https://github.com/thomasahle/sunfish/
PythonChess, used for GUI: https://www.pygame.org/project-Python+Chess-1099-.html
