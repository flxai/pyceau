# pycli-game-of-life

Simple Python implementation of [game of life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life). Simulation can be stopped using `^C`/`SIGINT`.

## Rules
The program allows to use Conway's original rules and others. They can be given via the `--rules` argument using [S/B notation](https://www.conwaylife.com/wiki/Rulestring).
Random rules are allowed using the format `--rules lL+rR`. `l` is the minimum, `L` number of elements for the left rule set. `r` and `R` work analogously. To allow maximum freedom on randomness of the rule sets, use `--rules 18+18`.

### Classical
Rule name | S/B notation
-|-
Conway's | 23/3
[Day and night](https://en.wikipedia.org/wiki/Day_and_Night_(cellular_automaton)) | 3678/34678

### Stumbled upon
The following rules have been randomly found by either a friend or myself. If they are marked to contain flicker they expose a risk of epilepsy which may be reduced using `-p`. Flicker of rules marked with + can be filtered, flicker of rules with - cannot. +/- works sometimes.

S/B notation | Flicker
-|-
01347/0123467 | +
01357/45678 |
03/02 | +
1/0234 | -
12/024 | +
1234/4 |
145//35 | +
23/0123 | +
2356/45 |
25/012346 | +/-
34567/68 |

To execute all of these one after another the following bash snippet may help:

```
for rules in $(grep -Eo '[0-9]+/[0-9]+ \|' README.md | cut -d\  -f1); do
    ./pycli-game-of-life -ps0 --rules $rules --steps 200
done
```

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

## Flicker
Some rule sets are strenuous to the eye, because of heavy flicker. To alleviate this problem use the `-p` flag.
