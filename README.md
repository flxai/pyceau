# pycli-game-of-life

Simple Python implementation of [game of life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life). Simulation can be stopped using `^C`/`SIGINT`.

## Rules
The program allows to use Conway's original rules and others. They can be given via the `--rules` argument using [S/B notation](https://www.conwaylife.com/wiki/Rulestring)

 Rule name | S/B notation
-|-
 Conway's | 23/3
 Day and night | 3678/34678

## Arguments
Start the program using the `--help` flag to see a current overview of allowed arguments.

## Board
Setting the board manually is supported through the `-b` argument. This implies board size and threefore `-w` and `-h` are not given. A sample `5x5` board with a glider can be given using the followin notation:

```
-b 00000.00100.00010.01110.00000
```

* `0` dead
* `1` alive
* `.` new line
