# Cellular automaton simulation with different rules
import copy
import os
import random
import shutil
import sys
import time

from PIL import Image, ImageDraw, ImageFont


class Board():
    _SLEEP_TIME_MAX = 1
    _FLICKER_MODES = 3 + 1

    def __init__(self, w, h, rule_string, tiles, subtitle_format=None, flicker_mode=0, tick=0, random_state=True,
                 state=False, seed='-1', max_ticks=None, spans_render_image=None, image_dir=None,
                 image_format=None, image_zoom=None, font_size=None, font_path=None, fill_percentage=0.5,
                 render_ticks=1, paused=False, no_expand=False, post_rule_string=None, post_ticks=0):
        self.rules, self.rule_string = Board.parse_rules(rule_string)
        self.tiles = {
            0: tiles[0],
            1: tiles[1],
        }
        self.fill_percentage = fill_percentage
        if not state:
            if seed == '-1':
                seed = ''.join(random.sample([chr(i + 65) for i in list(range(26))], 5))
            self.seed = seed
            random.seed(self.seed)
        self.w = w
        self.h = h
        if not state:
            self.board = [[0] * self.w for i in range(self.h)]
            if random_state:
                self.init_random_state()
        else:
            state_w = len(state[0])
            state_h = len(state)
            if state_w < w and state_h < h and not no_expand:
                self.board = Board.expand_state(state, w, h)
            else:
                self.w = state_w
                self.h = state_h
                self.board = state
            self.seed = f'{seed}?'
        self.flicker_mode = flicker_mode
        self.flicker_mode %= self._FLICKER_MODES
        self.tick = tick
        self.max_ticks = max_ticks
        self.cells_alive_old = self.cells_alive
        self.cells_dead_old = self.cells_total - self.cells_alive_old
        if spans_render_image:
            self.ticks_render_image = self.parse_ranges(spans_render_image)
        else:
            self.ticks_render_image = None
        if image_dir:
            self.image_dir = image_dir
            try:
                os.mkdir(self.image_dir)
            except FileExistsError:
                pass
        self.subtitle_format = subtitle_format
        self.image_format = image_format
        if image_zoom:
            self.image_zoom = int(image_zoom)
        if font_size and font_path and font_size:
            self.font_size = font_size
            self.font_path = font_path
            try:
                self.font = ImageFont.truetype(self.font_path, self.font_size)
            except OSError:
                if spans_render_image:
                    print(f"You're missing the selected font '{self.font_path}'. Rendering may look awkward...")
                self.font = ImageFont.load_default()
        self.render_ticks = render_ticks
        self.paused = paused
        self.post_ticks = post_ticks
        if post_rule_string and post_ticks > 0:
            self.post_rules, self.post_rule_string = Board.parse_rules(post_rule_string)
            self.board_post = self.post_process(post_rule_string, self.post_ticks)

    def init_random_state(self):
        for y in range(self.h):
            for x in range(self.w):
                self.board[y][x] = 1 if random.random() > self.fill_percentage else 0

    def draw(self, invert=False):
        if self.paused:
            time.sleep(self._SLEEP_TIME_MAX)
            return
        if self.tick % self.render_ticks != 0 or self.tick < 0:
            return
        inverted = self.inverted
        if self.post_ticks > 0:
            board = self.board_post
        else:
            board = self.board
        for y in range(self.h):
            for x in range(self.w):
                if not inverted:
                    print(self.tiles[board[y][x]], end='')
                else:
                    print(self.tiles[1 - board[y][x]], end='')
            print()
        print()
        if self.subtitle_format:
            print(self.subtitle)

    def step(self):
        if self.paused:
            time.sleep(self._SLEEP_TIME_MAX)
            return
        board_next = copy.deepcopy(self.board)
        for y in range(self.h):
            for x in range(self.w):
                n = self.neighbours(x, y)
                alive = self.board[y][x]
                flip_alive, flip_dead = self.rules[self.tick % len(self.rules)][n]
                if not alive and flip_dead:
                    board_next[y][x] = 1
                if alive and flip_alive:
                    board_next[y][x] = 0
        self.board = board_next
        self.tick += 1
        if self.post_ticks > 0:
            self.board_post = self.post_process(self.post_rule_string, self.post_ticks)
        self.render_image()

    def neighbours(self, x_cen, y_cen):
        s = 0
        for y in range(y_cen - 1, y_cen + 2):
            while y < 0:
                y += self.h
            if y > self.h - 1:
                y %= self.h
            for x in range(x_cen - 1, x_cen + 2):
                if x == x_cen and y == y_cen:
                    continue
                while x < 0:
                    x += self.w
                if x > self.w - 1:
                    x %= self.w
                if self.board[y][x]:
                    s += 1
        return s

    def board_serialize(self, prefix_param=False):
        if prefix_param:
            board_serial = '-b '
        else:
            board_serial = ''
        for y in range(self.h):
            for x in range(self.w):
                board_serial += str(self.board[y][x])
            board_serial += '.'
        return board_serial[:-1]

    def __str__(self):
        return self.subtitle

    def render_image(self):
        if self.paused:
            time.sleep(self._SLEEP_TIME_MAX)
            return
        if not self.ticks_render_image or self.tick not in self.ticks_render_image:
            return
        image_file = self.parse_format(self.image_format)
        image_path = f'{self.image_dir}/{image_file}'
        image_dir = '/'.join(image_path.split('/')[:-1])
        try:
            os.mkdir(image_dir)
        except FileExistsError:
            pass
        z = self.image_zoom
        offset = 0 if self.subtitle_format is None else self.font_size
        im = Image.new('1', (self.w * z, self.h * z + offset), 0)
        draw = ImageDraw.Draw(im)
        inverted = self.inverted
        if self.post_ticks > 0:
            board = self.board_post
        else:
            board = self.board
        for y in range(self.h):
            for x in range(self.w):
                if inverted and not board[y][x] or (not inverted and board[y][x]):
                    draw.rectangle([(x * z, y * z), ((x + 1) * z - 1, (y + 1) * z - 1)], 1)
        if self.subtitle_format is not None:
            draw.text([0, (self.h) * z - self.font_size / 4], self.subtitle, 1, font=self.font)
        del draw
        im.save(image_path)

    def parse_ranges(self, ranges_str):
        ranges = [e.split(':') for e in ranges_str.split(',')]
        ranges_rollout = []
        for r in ranges:
            r = [int(e) for e in r]  # typecast
            if self.max_ticks > 0:
                r = [e % (self.max_ticks + 1) if e < 0 else e for e in r]  # wrap negative
            else:
                if True in [e < 0 for e in r]:
                    print('Negative ranges are only allowed if max ticks is given.')
                    sys.exit(1)
            if len(r) > 2:  # range w/ stepsize
                ranges_rollout += list(range(r[0], r[1] + 1, r[2]))
            elif len(r) > 1:  # range
                ranges_rollout += list(range(r[0], r[1] + 1))
            else:  # single tick
                ranges_rollout += [int(r[0])]
        return ranges_rollout

    def parse_format(self, fmt):
        if not fmt:
            return None
        seed = self.seed
        for s in ['[', ']']:
            seed = seed.replace(s, '')
        s = {  # sequences
            'r': self.rule_string,
            'R': self.rule_string.replace('/', '-'),
            'd': f'{self.w}x{self.h}',
            'D': f'{self.w}-{self.h}',
            'f': self.flicker_mode,
            'a': 'X' if self.flicker_mode == 0 else chr(self.flicker_mode + 64),
            's': self.seed,
            'S': seed,
            't': self.tick,
            'T': f'{self.tick:08}',
            'i': 'i' if self.inverted else ' ',
            'o': 's' if self.ticks_render_image and self.tick in self.ticks_render_image else ' ',
            'pr': self.post_rule_string if self.post_ticks > 0 else '',
            'PR': self.post_rule_string.replace('/', '-') if self.post_ticks > 0 else '',
            'pt': f'{self.post_ticks}x' if self.post_ticks > 0 else '',
        }
        for k in s.keys():
            fmt = fmt.replace(f'%{k}', f'{{{k}}}')
        return fmt.format(**s)

    def post_process(self, rule_string, ticks=1):
        board = Board(self.w, self.h, rule_string, state=self.board, tiles=self.tiles, subtitle_format=None)
        for i in range(ticks):
            board.step()
        return board.board

    def pause_toggle(self):
        self.paused ^= 1

    def recover(self, parser=None, args=None):
        print('\nTo recover from this configuration, use the following representation as additional parameter:\n')
        name = sys.argv[0].split('/')[-1]
        indent = len(name) + 1
        first = True
        print(name, end=' ')
        for k, v in vars(args).items():
            if v == parser.get_default(k):
                continue
            if not first:
                print(' ' * indent, end='')
            if k == 'rules':
                print(f'--rules {self.rule_string} \\')
            else:
                print(f'--{k.replace("_", "-")} {v} \\')
            first = False
        if args.seed == '-1':
            print(' ' * indent, end='')
            print(f'-e {self.seed}')
        print(' ' * indent, end='')
        print(self.board_serialize(prefix_param=True))

    def cycle_flicker_mode(self):
        self.flicker_mode = (self.flicker_mode + 1) % self._FLICKER_MODES

    @ property
    def inverted(self):
        if self.flicker_mode == 0:
            return 0
        elif self.flicker_mode == 3:
            if self.tick % 2 == 0:
                return True
            else:
                return False
        invert = False
        cells_alive = self.cells_alive
        cells_dead = self.cells_total - cells_alive
        if self.flicker_mode == 1:
            corr_false = self.cells_alive_old - cells_dead
        elif self.flicker_mode == 2:
            corr_false = self.cells_dead_old - cells_dead
        # TODO: Use (board_old XOR board_now)'s count of 1s?
        else:
            corr_false = 0
        corr_true = self.cells_alive_old - cells_alive
        if corr_false > corr_true:
            invert = True
        self.cells_alive_old = cells_alive
        self.cells_dead_old = cells_dead
        return invert

    @property
    def cells_alive(self):
        alive = 0
        for y in range(self.h):
            for x in range(self.w):
                if self.board[y][x]:
                    alive += 1
        return alive

    @property
    def cells_total(self):
        return self.w * self.h

    @property
    def subtitle(self):
        return self.parse_format(self.subtitle_format)

    @staticmethod
    def parse_state(state_string):
        state = []
        for line in state_string.split('.'):
            state.append([int(c) for c in line])
        return state

    @staticmethod
    def random_rules(l_min=1, l_max=8, r_min=1, r_max=8):
        choices = list(range(8))
        l_num = random.randrange(l_min, l_max)
        r_num = random.randrange(r_min, r_max)
        l_rules = sorted(random.sample(choices, l_num))
        r_rules = sorted(random.sample(choices, r_num))
        l_str = "".join([str(e) for e in l_rules])
        r_str = "".join([str(e) for e in r_rules])
        rule_string = f'{l_str}/{r_str}'
        return rule_string

    @staticmethod
    def parse_rules(rule_string):
        if ',' in rule_string:
            rule_strings = rule_string.split(',')
        else:
            rule_strings = [rule_string]
        rules = []
        for j, r in enumerate(rule_strings):
            if 'x' in r:
                rs = r.split('x')
                f = int(rs[0])
                r = rs[1]
            else:
                f = 1
            if '+' in r:
                rule_tmp = r.split('+')
                rn = Board.random_rules(
                        int(rule_tmp[0][0]),
                        int(rule_tmp[0][1]),
                        int(rule_tmp[1][0]),
                        int(rule_tmp[1][1]),
                )
                rule_string = rule_string.replace(r, rn, 1)
                r = rn
            flip_alive, flip_dead = r.split('/')
            rule_set = {i: [True, False] for i in range(9)}
            for i in flip_alive:
                rule_set[int(i)][0] = False
            for i in flip_dead:
                rule_set[int(i)][1] = True
            for i in range(f):
                rules.append(rule_set)
        return rules, rule_string

    @staticmethod
    def parse_dimensions(dimensions, no_subtitle=False):
        h_mod = 2 if no_subtitle else 3
        w, h = dimensions.split('x')
        col, lin = shutil.get_terminal_size()
        w = col if w == 'M' else int(w)
        h = lin - h_mod if h == 'M' else int(h)
        return w, h

    @staticmethod
    def expand_state(state, w, h):
        state_w = len(state[0])
        state_h = len(state)
        w_odd = 1 if w % 2 == 0 else 0
        h_odd = 1 if h % 2 == 0 else 0
        x_off = (w // 2) - (state_w // 2 + w_odd)
        y_off = (h // 2) - (state_h // 2 + h_odd)
        board = [[0] * w for i in range(h)]
        for y in range(state_h):
            for x in range(state_w):
                if state[y][x]:
                    board[y + y_off][x + x_off] = 1
        return board
