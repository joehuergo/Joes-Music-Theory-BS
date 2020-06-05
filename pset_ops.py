from itertools import permutations
import math
from music21 import *

# operations on pitch sets and whatnot

# test list of pitch sets
a = [[0, 2, 4, 9],
     [0, 2, 4, 9],
     [-3, 0, 4, 7],
     [21, 4, 8, 4],
     [4, 4, 8, 21]]


def common_data(list1, list2):
    result = False
    # traverse in the 1st list
    for x in list1:
        # traverse in the 2nd list
        for y in list2:
            # if one common
            if x == y:
                result = True
                return result
    return result


def flatten_list(inp):
    output = []
    for i in inp:
        if type(i) == list:
            output.extend(flatten_list(i))
        else:
            output.append(i)
    return output


def prune_copies(inp):
    list_len = len(inp)
    i = 0
    while i < list_len:
        j = i + 1
        while j < list_len:
            if inp[i] == inp[j]:
                inp.reverse()
                inp.remove(inp[j])
                inp.reverse()
                list_len -= 1
                j -= 1
            j += 1
        i += 1
    return inp


def depth_count(x):
    return int(isinstance(x, list)) and len(x) and 1 + max(map(depth_count, x))


def sort_psets(psets):
    return sorted({tuple(x): x for x in psets}.values())


# filters for lists of pitch sets
def filter_intervals(psets, filt):
    out_pset = []
    intervals = [[i % 12 for i in flatten_list(get_intervals(i))] for i in psets]
    for i in range(len(psets)):
        if not common_data(filt, intervals[i]):
            out_pset.append(psets[i])
    return out_pset


def filter_interval_span(psets, filt):
    out_pset = []
    intervals = [get_intervals(i)[0] for i in psets]
    for i in range(len(psets)):
        if not any(x > filt for x in intervals[i]):
            out_pset.append(psets[i])
    return out_pset


def filter_span(psets, filt):
    out_pset = []
    for i in psets:
        if max(i) - min(i) <= filt:
            out_pset.append(i)
    return out_pset


# operates on a 1-dimensional list
def normalize_set(pset):
    if min(pset) < 0 or min(pset) > 11:
        sub = math.floor(min(pset) / 12) * 12
        for i in range(len(pset)):
            pset[i] = pset[i] - sub
    return pset


def get_voicings(pset):
    voicings = [list(x) for x in permutations(pset)]
    for i in range(len(voicings)):
        for b in range(len(voicings[i]) - 1):
            while voicings[i][b] >= voicings[i][b + 1]:
                voicings[i][b + 1] += 12
    return voicings


def get_intervals(pset):
    big_iset = []
    for i in range(1, len(pset)):
        lil_iset = []
        for j in range(len(pset) - i):
            lil_iset.append(pset[i + j] - pset[j])
        big_iset.append(lil_iset)
    return big_iset


def permute(iset):
    perm_iset = []
    for i in permutations(iset):
        if list(i) not in perm_iset:
            perm_iset.append(list(i))
    return perm_iset


def intervals_to_pitches(iset):
    perm_pset = []
    p = 0
    perm_pset.append(0)
    for j in iset:
        p += j
        perm_pset.append(p)
    return perm_pset


def transpose_pitches(pset, trans):
    trans_pset = []
    for i in pset:
        trans_pset.append(i + trans)
    return trans_pset


def permute_intervals(pset):
    return [intervals_to_pitches(i) for i in permute(get_intervals(pset)[0])]


# some chord naming stuff
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


def chord_stuff(pitch_sets, base_pitch):
    pitch_sets = [transpose_pitches(i, base_pitch) for i in pitch_sets]
    chords = [chord.Chord(i) for i in pitch_sets]
    for i in chords:
        print(i, end=" : ")
        print(i.commonName)
