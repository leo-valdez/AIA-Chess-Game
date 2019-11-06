# Chess
![Chess](https://image.shutterstock.com/image-vector/vector-chess-pieces-team-isolated-260nw-1068349304.jpg)

Chess is one of the most oldest games to be played on Earth and considered to be a  game played by the intelligent and the game of Brilliant people.This Game requires us to apply permutations and think two or three steps ahead  of the Game. This is also the thing that defeats us in Chess. Our Human brain is limited to calculations and slow as compared to Computers.

This was our first step towards AI as initially in 20th Century Chess was considered to be the first thing that Humans ought to be defeated by Computers. The History dates back to Garry Kasparov and IBM machines but it could not pull through but still brought a bright side that AI could defeat Humans in this Game.

<h3>Deep Blue</h3> was the first AI that introduced the world how computers had Started beating Humans.
So we did our first project on AI to realize the extent of AI and also make you realize that CHESS is so great.

Then came Competitors like Stockfish, AlphaGO etc that made it impossible for humans to defeat them even GrandMasters like Magnus Carlson, Vishwanathan Anand...

To show you the extent of how AI is developing i'll like to show you the 
![Chess](https://lh3.googleusercontent.com/fH046CiV5rLPsWZvOrg8bQFq3RA-iT7Qgr01IgZzuoAb2XbDXDxH7WrQ4-48g7pmd0i4KWMQdH-U3yxIVzR6ZK_-p7YkJCt6cGKq=w1440-rw-v1)

There are 10^120 Moves in Chess and for reference my Chess Code calculates Somewhere around 25K moves in 6 s avg. Then the time taken to See all possible moves and move the best piece would estimate to around 7.6103500761035007610350076103501e+108 Years !!!!!! 

<h1>Approach</h1>
We used Min-Max Algorithm to solve this problem also added weights to all the pieces on the game on the basis of their degree of Freedom in that position. PyGame was used as the frontend and simple mouse  drags can be used to play the game. The Game is a bit slow as it has a depth first search for the MIN-MAX algorithm in it .

These are the weights 
```bash
pip install python-chess
```
Hatsofff to this man ! 
https://github.com/niklasf/python-chess
This is needed as Python chess is too helpful to get the Chess notations and also getting positions and all possible moves. This reduces the task to an extent that we believe would save your months.
Other Important Packages are pygame
```bash
pip install pygame
```
Adding the Given Weights.
```python
pawn_table = [0, 0, 0, 0, 0, 0, 0, 0,
              50, 50, 50, 50, 50, 50, 50, 50,
              10, 10, 20, 30, 30, 20, 10, 10,
              5, 5, 10, 25, 25, 10, 5, 5,
              0, 0, 0, 20, 20, 0, 0, 0,
              5, -5, -10, 0, 0, -10, -5, 5,
              5, 10, 10, -20, -20, 10, 10, 5,
              0, 0, 0, 0, 0, 0, 0, 0]
knight_table = [-50, -40, -30, -30, -30, -30, -40, -50,
                -40, -20, 0, 0, 0, 0, -20, -40,
                -30, 0, 10, 15, 15, 10, 0, -30,
                -30, 5, 15, 20, 20, 15, 5, -30,
                -30, 0, 15, 20, 20, 15, 0, -30,
                -30, 5, 10, 15, 15, 10, 5, -30,
                -40, -20, 0, 5, 5, 0, -20, -40,
                -50, -90, -30, -30, -30, -30, -90, -50]
bishop_table = [-20, -10, -10, -10, -10, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 10, 10, 5, 0, -10,
                -10, 5, 5, 10, 10, 5, 5, -10,
                -10, 0, 10, 10, 10, 10, 0, -10,
                -10, 10, 10, 10, 10, 10, 10, -10,
                -10, 5, 0, 0, 0, 0, 5, -10,
                -20, -10, -90, -10, -10, -90, -10, -20]
rook_table = [0, 0, 0, 0, 0, 0, 0, 0,
              5, 10, 10, 10, 10, 10, 10, 5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              0, 0, 0, 5, 5, 0, 0, 0]
queen_table = [-20, -10, -10, -5, -5, -10, -10, -20,
               -10, 0, 0, 0, 0, 0, 0, -10,
               -10, 0, 5, 5, 5, 5, 0, -10,
               -5, 0, 5, 5, 5, 5, 0, -5,
               0, 0, 5, 5, 5, 5, 0, -5,
               -10, 5, 5, 5, 5, 5, 0, -10,
               -10, 0, 5, 0, 0, 0, 0, -10,
               -20, -10, -10, 70, -5, -10, -10, -20]
king_table = [-30, -40, -40, -50, -50, -40, -40, -30,
              -30, -40, -40, -50, -50, -40, -40, -30,
              -30, -40, -40, -50, -50, -40, -40, -30,
              -30, -40, -40, -50, -50, -40, -40, -30,
              -20, -30, -30, -40, -40, -30, -30, -20,
              -10, -20, -20, -20, -20, -20, -20, -10,
              20, 20, 0, 0, 0, 0, 20, 20,
              20, 30, 10, 0, 0, 10, 30, 20]
king_endgame_table = [-50, -40, -30, -20, -20, -30, -40, -50,
                      -30, -20, -10, 0, 0, -10, -20, -30,
                      -30, -10, 20, 30, 30, 20, -10, -30,
                      -30, -10, 30, 40, 40, 30, -10, -30,
                      -30, -10, 30, 40, 40, 30, -10, -30,
                      -30, -10, 20, 30, 30, 20, -10, -30,
                      -30, -30, 0, 0, 0, 0, -30, -30,
                      -50, -30, -30, -30, -30, -30, -30, -50]
                 
```
<h1>Failed Approach</h2>
We did try using Alpha-Beta pruning and CNN but due to lack of proper knowledge it wasnt working properly. 
<h1>Future Improvments</h1>
Imporoving the game with the approch of RNN, after successful implementation of Aplha-Beta pruning. 

