import svgwrite
import math


def round_up(num, mult):
    if mult == 0:
        return num
    rem = num % mult
    if rem == 0:
        return num
    return num + mult - rem


# piano dimensions
p_width = 520
p_height = 72
key_width = 22
bkey_width = key_width / 2
bkey_height = (16 / 25) * p_height
bkey_offset = key_width / 4
num_pianos = 0
hilite_color = 'red'


def draw_pianos(psets, p_space):
    if len(psets) == 0:
        print("No chords to draw. Will not create svg.")
        return
    height = len(psets) * (p_space + p_height) + p_space
    width = math.ceil(max([max(p) for p in psets]) / 12) * (key_width * 7) + key_width + (2 * p_space)
    dwg = svgwrite.Drawing('piano.svg', (width, height))
    pianos = []
    for j in range(len(psets)):
        pianos.append(Piano((p_space, p_space + j * (p_space + p_height)), psets[j]))
        for i in range(pianos[j].key_count):
            white_i = pianos[j].white_key_indexes[pianos[j].w_index]
            key_color = 'white'
            if pianos[j].hilite[white_i] == 1:
                key_color = hilite_color
            dwg.add(dwg.rect(((i * key_width) + pianos[j].pos[0], pianos[j].pos[1]), (key_width, p_height),
                             fill=key_color, stroke='black'))
            pianos[j].w_index += 1
            if i % 7 in (1, 2, 4, 5, 6):
                black_i = pianos[j].black_key_indexes[pianos[j].b_index]
                key_color = 'black'
                if pianos[j].hilite[black_i] == 1:
                    key_color = hilite_color
                dwg.add(dwg.rect((((i * key_width) - bkey_offset) + pianos[j].pos[0], pianos[j].pos[1]), (
                    bkey_width, bkey_height), fill=key_color, stroke='black'))
                pianos[j].b_index += 1
    dwg.save()


class Piano:
    gen_key = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]

    # pos is a tuple, pset is a list, kwidth is a number
    def __init__(self, pos, pset):
        self.pset = pset
        self.max_pitch = max(pset)
        self.pos = pos
        self.keypos_map = []
        self.white_key_indexes = []
        self.black_key_indexes = []

        # construct the indexes and map we use for drawing
        it = 0
        for i in range(round_up(self.max_pitch, 12) + 1):
            self.keypos_map.append(it)
            it += self.gen_key[i % 12]
            if self.gen_key[i % 12] == 0:
                self.black_key_indexes.append(i)
            elif self.gen_key[i % 12] == 1:
                self.white_key_indexes.append(i)

        key_val = self.keypos_map[self.max_pitch - 1]
        self.key_count = round_up(key_val + 1, 7) + 1
        self.hilite = [None] * (round_up(self.max_pitch, 12) + 1)
        self.w_index = 0
        self.b_index = 0

        # set notes to be highlighted
        for i in range(self.max_pitch + 1):
            if i in self.pset:
                self.hilite[i] = 1
