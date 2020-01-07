# pycli-game-of-life

Simple Python implementation of [game of life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).
Simulation can be stopped using `^C`/`SIGINT`.

## Rules
The program allows to use Conway's original rules and others.
They can be given via the `--rules` argument using [S/B notation](https://www.conwaylife.com/wiki/Rulestring).
Random rules are allowed using the format `--rules lL+rR`.
`l` is the minimum, `L` number of elements for the left rule set.
`r` and `R` work analogously.
To allow maximum freedom on randomness of the rule sets, use `--rules 18+18`.

### Classical
Rule name | S/B notation
-|-
Conway's | 23/3
[Day and night](https://en.wikipedia.org/wiki/Day_and_Night_(cellular_automaton)) | 3678/34678

### Stumbled upon
The following rules have been randomly found or at least partly crafted by either a friend or myself.
Flicker of rules marked with + can be filtered, flicker of rules with - cannot.
= works sometimes.
Numbers indicate a preferred filter mode given `--flicker-mode`.
Convergence describes time to reach a state without much change.
\+ means it takes long, 0 normal and - short to converge.
Stability describes that a system has sufficient change, but not too much to be reduced to noise.
Convergence and stability are not yet operationalized.

S/B notation   | Flicker | Convergence | Stability
--------------:|:-------:|:-----------:|:--------:
01/015678      | 2=      | -           | -
0123/01234     | +       | -           | -
012346/0123678 | 2=      | ++          | =
012358/0238    | 1=      | +           | =
0135/012357    | 2=      | +           | =
01357/45678    | 1+      | =           | -
0/2            | 1+      | +           | -
0234/73        | 1=      | ++          | +
02456/0123467  | 2=      | ++          | +
03/02          | +       | -           | -
03456/012346   | =       | +           | =
035/012347     | +       | =           | =
1/0234         | 2=      | -           | -
12/024         | +       | =           | -
1234/4         | 1+      | +           | -
12345/01245678 | 2=      | +           | +
1237/137       | 1=      | +           | =
1238/0127      | 1=      | ++          | =
1245/1234567   | 2=      | ++          | =
12456/4567     | 1=      | ++          | =
12457/04       | 1+      | ++          | =
13/34          | 1+      | ++          | +
145//35        | +       | -           | -
23/0123        | +       | -           | -
23457/05678    | 1=      | +           | -
23457/012346   | 2=      | ++          | =
2356/45        | 1=      | =           | -
25/012346      | 2+      | +           | -
2568/35678     | 1+      | +           | -
3456/012356    | 2=      | ++          | +
34567/68       | 1+      | -           | -
34568/46       | +       | -           | -
34568/5678     | 1=      | =           | -
347/356        | 1=      | ++          | =
35/0678        | 1-      | ++          | +
3578/06        | 1=      | +++         | =
4/012346       | =       | -           | -
4/0123567      | 2=      | =           | -
4567/567       | 1+      | -           | -
5/078          | 1-      | ++          | +
567/45678      | 1+      | -           | -
567/245678     | 1=      | ++          | -
5678/1367      | 1=      | ++          | -

To execute all of these one after another using the less strenuous flicker filter the following bash snippet may help:

```bash
for rules in $(grep -Eo '[0-9]+/[0-9]+ +\|' README.md | cut -d\  -f1); do
    [[ ! $(grep -E "^$rules\s+\|" README.md | awk '{ print $3 }' | cut -c1) =~ 2 ]] && mode=1 || mode=2
    ./pycli-game-of-life -cps0 --rules $rules --steps 200 --flicker-mode $mode
done
```

To cycle through ones with slow convergence (++) using `^C` the following commands can be used:

```
for rules in $(grep -E '\+{2}' README.md | grep -Eo '[0-9]+/[0-9]+ +\|' | cut -d\  -f1); do
    [[ ! $(grep -E "^$rules\s+\|" README.md | awk '{ print $3 }' | cut -c1) =~ 2 ]] && mode=1 || mode=2
    ./pycli-game-of-life -cps0 -m$mode --rules $rules
done
```

### Exploration
To explore and find new rules the following snippet can be used:

```bash
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
Setting the board manually is supported through the `-b` argument.
This implies board size and therefore `-d` is not given.
A sample `5x5` board with a glider can be given using the following notation:

```
-b 00000.00100.00010.01110.00000
```

* `0` dead
* `1` alive
* `.` new line

## Flicker
Some rule sets are strenuous to the eye, because of heavy flicker.
To alleviate this problem use the `-p` flag.
You can choose between different modes `1` and `2` via `-m` where `1` is default.
I'd be happy about another contribution.

## Disclaimer
May create seizures. Use this software at your own risk.
