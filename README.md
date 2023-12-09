# Tic-tac-toe

<p align="center">
	<img src="./tic-tac-toe.png" alt="Tic-tac-toe"/>
</p>

A state of the art Tic-tac-toe implementation in pure HTML (no JavaScript used).

# About the project

This is a meme project that I created one afternoon after being fed up with DevOps at work.

You can play the game online by visiting https://robertbarachini.github.io/projects/tic-tac-toe/

If you want to play it offline you can do so by downloading the `./src/site` folder and opening `index.html` in your browser.

# Background

Years ago when I was still in primary school (2010?) I wanted to create a website where you could play Tic-tac-toe. Since I didn't know much (anything) about JavaScript, the only logical conclusion was to hard code the game in HTML. After writing about 20 pages, it occurred to me that working like that was Sisyphean and so I abandoned the project to focus on creating cheesy graphics. Now that I know a little bit about programming and am, more importantly, even dumber, the time has come to bring the deranged project of the past to reality. Instead of writing each game state page by hand in Notepad, I let Python do the work for me. Thank you, Python.

The generator plays the entire game and builds a tree of all possible games which is then read (and cached with numpy.save) by another script that builds HTML pages. Each unique game state is a new HTML page and future states are encoded in links. When you play the game by clicking the squares on the board you are traversing the game states as encoded by the program simply by using the HTTP protocol.

Additionally, you could run a Minimax algorithm which reads the tree and returns optimal moves for each state which could then be similarly encoded in HTML links. This would make it possible to play against a perfect Tic-tac-toe AI. Each link would encode a future game state after the AI agent has “made a move”. There would be no real-time computation and yet the AI agent would be unbeatable.

# Some stats

Generated with `tictactoe.py`:

```text
Tree function visits: 294778
Unique states/boards: 5477 (5478 with empty board)

Stats:
> X wins: 131184
> O wins: 77904
> Ties: 46080
> Unique X wins: 626
> Unique O wins: 316
> Unique Ties: 16

Tied boards:

Tie 1:
X | O | X
--+---+--
O | X | X
--+---+--
O | X | O

Tie 2:
X | O | X
--+---+--
O | O | X
--+---+--
X | X | O

Tie 3:
X | O | X
--+---+--
X | O | O
--+---+--
O | X | X

Tie 4:
X | O | X
--+---+--
X | O | X
--+---+--
O | X | O

Tie 5:
X | O | X
--+---+--
X | X | O
--+---+--
O | X | O

Tie 6:
X | O | O
--+---+--
O | X | X
--+---+--
X | X | O

Tie 7:
X | X | O
--+---+--
O | X | X
--+---+--
X | O | O

Tie 8:
X | X | O
--+---+--
O | O | X
--+---+--
X | O | X

Tie 9:
X | X | O
--+---+--
O | O | X
--+---+--
X | X | O

Tie 10:
O | X | X
--+---+--
X | O | O
--+---+--
X | O | X

Tie 11:
O | X | X
--+---+--
X | O | O
--+---+--
O | X | X

Tie 12:
O | X | X
--+---+--
X | X | O
--+---+--
O | O | X

Tie 13:
O | X | O
--+---+--
X | X | O
--+---+--
X | O | X

Tie 14:
O | X | O
--+---+--
X | O | X
--+---+--
X | O | X

Tie 15:
O | X | O
--+---+--
O | X | X
--+---+--
X | O | X

Tie 16:
O | O | X
--+---+--
X | X | O
--+---+--
O | X | X
```
