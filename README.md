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
The following rules have been randomly found by either a friend or myself.
If they are marked to contain flicker they expose a risk of epilepsy which may be reduced using `-p`.
Flicker of rules marked with + can be filtered, flicker of rules with - cannot.
= works sometimes.
Convergence describes time to reach a state without much change.
+ means it takes long, 0 normal and - short to converge.
Stability describes that a system has sufficient change, but not too much to be reduced to noise.
Convergence and stability are not yet operationalized.

S/B notation   | Flicker | Convergence | Stability
--------------:|:-------:|:-----------:|:--------:
01/015678      | -       | -           | -
0123/01234     | +       | -           | -
012358/0238    | =       | +           | =
0135/012357    | +       | +           | =
01357/45678    |         | =           | -
0/2            |         | +           | -
02456/0123467  | -       | ++          | +
03/02          | +       | -           | -
03456/012346   | =       | +           | =
035/012347     | +       | =           | =
1/0234         | -       | -           | -
12/024         | +       | =           | -
1234/4         |         | +           | -
12345/01245678 | -       | +           | +
1237/137       |         | +           | =
1238/0127      |         | ++          | =
1245/1234567   | -       | ++          | =
12456/4567     |         | ++          | =
12457/04       |         | ++          | =
145//35        | +       | -           | -
23/0123        | +       | -           | -
23457/05678    |         | +           | -
2356/45        |         | =           | -
25/012346      | =       | +           | -
2568/35678     |         | +           | -
34567/68       |         | -           | -
347/356        |         | ++          | =
4/012346       | =       | -           | -
4/0123567      | =       | =           | -
4567/567       |         | -           | -

To execute all of these one after another the following bash snippet may help:

```
for rules in $(grep -Eo '[0-9]+/[0-9]+ +\|' README.md | cut -d\  -f1); do
    ./pycli-game-of-life -ps0 --rules $rules --steps 200
done
```

### Exploration
To explore and find new rules the following snippet can be used:

```
while true; do
   ./pycli-game-of-life -ps0 --rules 18+18
   sleep .4
done
```

If interesting patterns emerge `^C` can be held.
`sleep` should be modified to match the keyboard's refresh rate to not start a new simulation too soon.

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
