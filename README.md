installation isntruction:

this game runs on python while using pygame.

in cmd

pip install pygame

both game files need to be in the same directory.




The left side is the human player board (upper grid is the search grid)
the right side is the AI player.

how to play.

the human player has the first move. in order to make a move, you just need to click the cell you want to investigate.
after that the AI player will play.
Orange - hit (+ extra turn), Blue - miss (pass the turn), Red - hit and sunk (+ extra turn)

useful keys:

h - hide/unhide the AI ships

m - hide/unhide the AI probability decision mask. 

enter - restart a new game



known bugs:

if the human player presses on a cell that already been filled, it changes the turn without actually making a move.
when a new game has been started (via pressing enter) the probability mask will not reset.
