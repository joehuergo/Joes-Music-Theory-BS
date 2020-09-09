import svgwrite
import math
from psets import *


def round_up(num, mult):
    if mult == 0:
        return num
    rem = num % mult
    if rem == 0:
        return num
    return num + mult - rem


def longest(lis):
    if not isinstance(lis, list): return 0
    return (max([len(lis), ] + [len(subl) for subl in lis if isinstance(subl, list)] +
                [longest(subl) for subl in lis]))


def note_name(mpv):
    mdict = {
        0: "C",
        1: "Db",
        2: "D",
        3: "Eb",
        4: "E",
        5: "F",
        6: "F#",
        7: "G",
        8: "Ab",
        9: "A",
        10: "Bb",
        11: "B"
    }
    return mdict[mpv % 12] + str(math.floor(mpv / 12) - 1)


def interval_name(ival):
    idict = {
        1: "m2",
        2: "M2",
        3: "m3",
        4: "M3",
        5: "P4",
        6: "TT",
        7: "P5",
        8: "m6",
        9: "M6",
        10: "m7",
        11: "M7"
    }
    return idict[ival % 12]


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


class Chart:
    margin = 12
    width = 5
    height = margin + 5
    base_note = 48
    unit_height = 0
    unit_space = 8
    flags = 0
    fontsize = 12
    offset_key = []
    unit_offsets = [0]
    unit_offsets.extend(offset_key)
    draw_label = False
    draw_piano = False

    def __init__(self, filename, pset_list):
        self.filename = filename
        self.plist = pset_list
        self.dwg = 0

    def __get_pset_text(self, pset):
        notename_list = [note_name(i + self.base_note) for i in pset]
        string = "Pitches: " + str(pset) + " / " + str(notename_list)
        return string

    def __get_iset_text(self, iset):
        interval_name_list = [interval_name(i) for i in iset]
        string = "Intervals: " + str(iset) + " / " + str(interval_name_list)
        return string

    def __draw_label(self, label, x, y):
        self.dwg.add(self.dwg.text(label,
                                   insert=(x, y),
                                   font_size=self.fontsize,
                                   fill='black',
                                   style='font-family:Consolas'))

    def __draw_piano(self, piano):
        for i in range(piano.key_count):
            white_i = piano.white_key_indexes[piano.w_index]
            self.key_color = 'white'
            if piano.hilite[white_i] == 1:
                self.key_color = self.hilite_color
            self.dwg.add(self.dwg.rect(((i * self.key_width) + piano.pos[0],
                                        piano.pos[1]), (self.key_width, self.p_height),
                                       fill=self.key_color, stroke='black'))
            piano.w_index += 1
            if i % 7 in (1, 2, 4, 5, 6):
                black_i = piano.black_key_indexes[piano.b_index]
                key_color = 'black'
                if piano.hilite[black_i] == 1:
                    key_color = self.hilite_color
                self.dwg.add(self.dwg.rect((((i * self.key_width) - self.bkey_offset) + piano.pos[0],
                                            piano.pos[1]), (self.bkey_width, self.bkey_height), fill=key_color,
                                           stroke='black'))
                piano.b_index += 1

    def __process_content_flags(self):
        if self.draw_label:
            self.offset_key.append(2 * self.fontsize + self.unit_space)
            # add to unit height
            self.unit_height += 2 * (self.fontsize + self.unit_space)
            self.p_labels = [self.__get_pset_text(self.plist.pset_list[i].pset)
                             for i in range(len(self.plist.pset_list))]
            self.i_labels = [self.__get_iset_text(self.plist.pset_list[i].iseqset[0])
                             for i in range(len(self.plist.pset_list))]
            label_maxwidth = len(max([max(self.p_labels, key=len), max(self.i_labels, key=len)])) * \
                                (0.65 * self.fontsize)
            if label_maxwidth > self.width:
                self.width = 5 + self.margin + label_maxwidth

        if self.draw_piano:
            psets = [i.pset for i in self.plist.pset_list]
            self.p_width = 520
            self.p_height = 72
            self.key_width = 22
            self.bkey_width = self.key_width / 2
            self.bkey_height = (16 / 25) * self.p_height
            self.bkey_offset = self.key_width / 4
            self.hilite_color = 'red'
            self.pianos = []
            self.offset_key.append(self.p_height + self.margin)
            # add to unit height
            self.unit_height += self.margin + self.p_height
            width = math.ceil(max([max(p) for p in psets]) / 12) * \
                    (self.key_width * 7) + self.key_width + (2 * self.margin)
            if width > self.width:
                self.width = width

        self.unit_offsets.extend(self.offset_key)
        self.height = self.unit_height * len(self.plist.pset_list) + self.margin * 2
        return self

    def draw(self):
        self.__process_content_flags()
        self.dwg = svgwrite.Drawing(self.filename, size=(self.width, self.height))
        for i in range(len(self.plist.pset_list)):
            self.flags = 0
            if self.draw_label:
                self.__draw_label(self.i_labels[i], self.margin, i * self.unit_height + self.fontsize + self.margin)
                self.__draw_label(self.p_labels[i], self.margin, i * self.unit_height
                                  + 2 * self.fontsize + self.margin)
                self.flags += 1
            if self.draw_piano:
                self.pianos.append(Piano((self.margin + 2,
                                          i * self.unit_height + self.unit_offsets[self.flags] + self.margin),
                                         self.plist.pset_list[i].pset))
                self.__draw_piano(self.pianos[i])
                self.flags += 1
        self.dwg.save()
        return self


test = PSet([0, 7, 14, 15, 22]).get_voicings()
canvas = Chart('canvas.svg', test)
canvas.draw_label = True
canvas.fontsize = 14
canvas.draw_piano = True
canvas.draw()
