This is a chess AI that uses decision-tree solution with min-max algorithm and alpha-beta pruning algorithm.

To run the program you need to have pygame installed as it is what we uses to view the board. 
To install pygame you can run:
    python3 -m pip install -U pygame --user

The program also uses a chess library for representing the board and it also have move validation. 
To install python-chess:
    pip install python-chess

To run the program you have to run the chessboard.py file

At the start of the program you will get a few options in the terminal where you can chose between:
1. player vs AI
2. AI vs AI
3. player vs player

To chose a mode you have to write the corresponding number in the terminal

To move a piece you press it's square and then the square you want to move the piece to.
If it is a legal move it will do the move, and if it is not a legal move it will ignore the request. 