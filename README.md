# pacman
an implementation of the Pac-Man arcade game using PyGame and Twisted 


## notes:

Running the game requres Python 2.7 (NOT Python 3.0) and installation of the PyGame and Twisted libraries. For multiplayer mode, which includes network connection, run "python2 twistedP2.py" followed by "python2 twistedP1.py" in two different terminals, then select 2 Player in the right bar in each window and wait for the connection to be made, then play. For single player mode, run either file and select 1 Player, then play. These files can be found in the /src directory.

The game works like normal Pacman. Once you've selected a mode, use the keypad arrows to move up, down, left, or right. The objective is to collect all of the yellow dots while avoiding the ghosts. If you collide with a ghost, Pacman goes back to the starting position and you lose one of your three lives. If you collect one of the big yellow dots, the ghosts become transparent for a limited time and you can run through them without penalty. Collecting all the dots before losing all three lives wins the game. In two player mode, you compete with an opponent to see who can score more points (points are based on yellow dot collection). The gameplay is independent, but the score of each player is tallied and shared with each player in the score bar on the right. Whoever scores more points in their game of Pacman wins.

Credit for the sprites goes to Superjustinbros on https://www.spriters-resource.com 

Credit for the sounds go to crysknife007 from https://www.youtube.com/watch?v=KL_FkWrFThA , http://soundbible.com/tags-winning.html and http://www.classicgaming.cc/