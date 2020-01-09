# pycli-game-of-life

Simple Python implementation of [game of life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).
Simulation can be stopped using `^C`/`SIGINT`.

## Rules
The program allows to use Conway's original rules and others.
They can be given via the `-r` or `--rules` argument using [S/B notation](https://www.conwaylife.com/wiki/Rulestring).
Random rules are allowed using the format `-r lL+rR`.
`l` is the minimum, `L` number of elements for the left rule set.
`r` and `R` work analogously.
To allow maximum freedom on randomness of the rule sets, use `-r 18+18`.

### Classical
Rule name | S/B notation
-|-
Conway's | 23/3
[Day and night](https://en.wikipedia.org/wiki/Day_and_Night_(cellular_automaton)) | 3678/34678

### Stumbled upon
The following rules have been randomly found or at least partly crafted by either a friend or myself.
Flicker of rules marked with + can be filtered, flicker of rules with - cannot.
= works sometimes.
Numbers indicate a preferred filter mode given `-m` or `--flicker-mode`.
Convergence describes time to reach a state without much change.
\+ means it takes long, 0 normal and - short to converge.
Stability describes that a system has sufficient change, but not too much to be reduced to noise.
Convergence and stability are not yet operationalized.

S/B notation      | Flicker   | Convergence   | Stability
-----------------:|:---------:|:-------------:|:---------:
01/015678         | 3+        | -             | -
0123/01234        | 3+        | -             | -
01234567/12345678 | 3         | -             | -
012346/0123678    | 2=        | ++            | =
012358/0238       | 1=        | +             | =
0135/012357       | 3+        | +             | =
01357/45678       | 1+        | =             | -
145/0128          | 2+        | +             | -
0/2               | 1+        | +             | -
0234/73           | 0+        | ++            | +
02456/0123467     | 3+        | ++            | +
03/02             | 3+        | -             | -
03456/012346      | 3+        | +             | =
035/012347        | 3+        | =             | =
1/0234            | 3+        | -             | -
12/024            | 3+        | =             | -
1234/4            | 1+        | +             | -
12345/01245678    | 3+        | +             | +
1237/137          | 0=        | +             | =
1238/0127         | 1=        | ++            | =
1245/1234567      | 3+        | ++            | =
12456/4567        | 1=        | ++            | =
12457/04          | 1+        | ++            | =
1256/3            | 0+        | +++           | =
13/34             | 1+        | ++            | +
145/35            | 0+        | -             | -
23/0123           | 3+        | -             | -
23457/05678       | 1=        | +             | -
23457/012346      | 3+        | ++            | =
2356/45           | 0+        | =             | -
25/012346         | 2+        | +             | -
2568/35678        | 1+        | +             | -
3456/012356       | 3+        | ++            | +
34567/68          | 1+        | -             | -
34568/46          | 0+        | -             | -
34568/5678        | 0=        | =             | -
347/356           | 0=        | ++            | =
35/0678           | 0-        | ++            | +
3578/06           | 0=        | +++           | =
4/012346          | 3+        | -             | -
4567/567          | 1+        | -             | -
5/078             | 1-        | ++            | +
567/45678         | 1+        | -             | -
567/245678        | 1=        | ++            | -
5678/1367         | 0=        | ++            | -

To execute all of these one after another using the less strenuous flicker filter the following bash snippet may help:

```bash
for rules in $(grep -Eo '[0-9]+/[0-9]+ +\|' README.md | cut -d\  -f1); do
    mode=$(grep -E "^$rules\s+\|" README.md | awk '{ print $3 }' | cut -c1); [[ $mode =~ [0-3] ]] || mode=0
    ./pycli-game-of-life -cr $rules -s 200 -m $mode
done
```

To cycle through ones with slow convergence (++) using `^C` the following commands can be used:

```
for rules in $(grep -E '\+{2}' README.md | grep -Eo '[0-9]+/[0-9]+ +\|' | cut -d\  -f1); do
    mode=$(grep -E "^$rules\s+\|" README.md | awk '{ print $3 }' | cut -c1); [[ $mode =~ [0-3] ]] || mode=0
    ./pycli-game-of-life -cm $mode -r $rules
done
```

### Exploration
To explore and find new rules the following snippet can be used:

```bash
while true; do
   ./pycli-game-of-life -r 18+18
   sleep .4
done
```

If interesting patterns emerge `^C` can be held.
`sleep` should be modified to match the keyboard's refresh rate to not start a new simulation too soon.

### One dimensional simulations
To simulate all the rules from the list within a single dimension and create graphical "footprints" use the following snippet:

```bash
for rules in $(grep -Eo '[0-9]+/[0-9]+ +\|' README.md | cut -d\  -f1); do
    mode=$(grep -E "^$rules\s+\|" README.md | awk '{ print $3 }' | cut -c1); [[ $mode =~ [0-3] ]] || mode=0
    echo -e "\n$rules"; ./pycli-game-of-life -cr $rules -s 16 -m $mode -ud 80x1 | grep -vE '^$'
done
```

Note that `grep` is used to filter out empty lines that would otherwise disturb the output.
While some of the rules give interesting patterns there are also duplicates (like `35/0678` and `3578/06`).
This is because the rules are still computed in two dimensional neighbourhood with a ring of size 1 in the second dimension.
[Wolfram code](https://en.wikipedia.org/wiki/Wolfram_code) are usually used for one dimensional cellular automata and given S/B notation could be converted accordingly.

## Arguments
Start the program using the `--help` or `-?` flag to see a current overview of allowed arguments.

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

## Suptitle bar
The subtitle bar can display different kinds of information.
The following tables lists possible values for its format:

Format  | Expansion
-------:|:----------------------------------------
`%r`    | Rules
`%R`    | Rules (`/` replaced with `-`)
`%d`    | Dimensions (`WxH`)
`%D`    | Dimensions (`W-H`)
`%f`    | Flicker mode
`%a`    | Flicker mode (alphabetic)
`%s`    | Random seed
`%S`    | Random seed (`[`, `]` removed)
`%t`    | Tick number
`%T`    | Tick number (8 digits, preceding zeroes)
`%i`    | Inversion indicator
`%o`    | Render indicator

The default is `%r %a %t %i` and can be overwritten via `-f`.
Image render file format is using `%R-%D-%S-%a-%T.png` per default.

## Flicker
Some rule sets are strenuous to the eye, because of heavy flicker.
To alleviate this problem use the `-p` flag.
You can choose between different modes `1`, `2` and `3` via `-m` where `1` is default.

## Disclaimer
May create seizures. Use this software at your own risk.

## Render images
You can render images with limited options.

### Stills
The following snippet renders a still in
`img/0123-01234-48-32-DEMO-A-4.png`:

```bash
./pycli-game-of-life -r 0123/01234 -s4 -m1 -d 48x32 -qe DEMO -i -1
xdg-open img/*
```

### Image sequences
The following snippet renders all of the 3000 frames in the `img` directory. This will take some time:

```bash
./pycli-game-of-life -r 3456/012356 -s3100 -m2 -z2 -d 512x256 -e DEMO -i 100:-1:2 -q
xdg-open img/*
```

### Videos
If you have executed the last snippet to create image sequences, you can then use `ffmpeg` to combine these into a video.
A simple command to encode the stills into a video using [WebM and VP9](https://trac.ffmpeg.org/wiki/Encode/VP9):

```
ffmpeg -framerate 60
       -pattern_type glob
       -i 'img/*.png'
       -c:v libvpx-vp9
       -pix_fmt yuva420p
       output.webm 
```

After rendering has completed you can have a look at `output.webm`.
See *Tick spans* below for further details.

## Tick spans
To describe tick spans for `-i` the following notation is used:

* `n` describes a single page
* `n,m` describes both pages or ranges `n` and `m`
* `n:m` describes a range from `n` to `m` including `m`
* `n:m:k` describes a range from `n` to `m` including `m` with step size `k`

E.g. `0:2,5:9:3,-1` unfolds to the list `[0, 1, 2, 5, 9]` if the last tick is `9`.

Note that there is a `--render-ticks` that does something similar for rendering to stdout.
