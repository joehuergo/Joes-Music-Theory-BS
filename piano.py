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
dwg = None


def draw_pianos(psets, p_space):
    global dwg
    height = len(psets) * (p_space + p_height) + p_space
    width = math.ceil(max([max(p) for p in psets])/12)*(key_width*7)+key_width+(2*p_space)
    dwg = svgwrite.Drawing('piano.svg', (width, height))

    pianos = []
    for i in range(len(psets)):
        pianos.append(Piano((p_space, p_space + i * (p_space + p_height)), psets[i]))


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
        for i in range(round_up(self.max_pitch, 12)+1):
            self.keypos_map.append(it)
            it += self.gen_key[i % 12]
            if self.gen_key[i % 12] == 0:
                self.black_key_indexes.append(i)
            elif self.gen_key[i % 12] == 1:
                self.white_key_indexes.append(i)

        mpminus1 = self.max_pitch-1
        keyval = self.keypos_map[mpminus1]
        self.key_count = round_up(keyval, 7) + 1
        self.hilite = [None] * (round_up(self.max_pitch, 12) + 1)
        self.w_index = 0
        self.b_index = 0

        # set notes to be highlighted
        for i in range(self.max_pitch+1):
            if i in self.pset:
                self.hilite[i] = 1

        # draw piano
        for i in range(self.key_count):
            white_i = self.white_key_indexes[self.w_index]
            key_color = 'white'
            if self.hilite[white_i] == 1:
                key_color = hilite_color
            dwg.add(dwg.rect(((i * key_width) + pos[0], pos[1]), (key_width, p_height),
                             fill=key_color, stroke='black'))
            self.w_index += 1
            if i % 7 in (1, 2, 4, 5, 6):
                black_i = self.black_key_indexes[self.b_index]
                key_color = 'black'
                if self.hilite[black_i] == 1:
                    key_color = hilite_color
                dwg.add(dwg.rect((((i * key_width) - bkey_offset) + self.pos[0], self.pos[1]), (
                    bkey_width, bkey_height), fill=key_color, stroke='black'))
                self.b_index += 1

