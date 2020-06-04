from itertools import permutations
import math


def note_name(mpv):
    return mdict[mpv % 12] + str(math.floor(mpv / 12) - 1)


mdict = {
    0: "C",
    1: "C#",
    2: "D",
    3: "D#",
    4: "E",
    5: "F",
    6: "F#",
    7: "G",
    8: "G#",
    9: "A",
    10: "A#",
    11: "B"
}


def prune_copies(inp):
    list_len = len(inp)
    i = 0
    while i < list_len:
        val1 = inp[i]
        j = i + 1
        while j < list_len:
            val2 = inp[j]
            if val1 == val2:
                inp.reverse()
                inp.remove(val2)
                inp.reverse()
                list_len -= 1
                j -= 1
            j += 1
        i += 1
    return inp


def depth_count(x):
    return int(isinstance(x, list)) and len(x) and 1 + max(map(depth_count, x))


def normalize_sets(pset):
    for i in range(len(pset)):
        if min(pset[i]) < 0 or min(pset[i]) > 11:
            sub = math.floor(min(pset[i]) / 12) * 12
            for x in range(len(pset[i])):
                pset[i][x] = pset[i][x] - sub
    return pset


def sort_psets(psets):
    return sorted({tuple(x): x for x in psets}.values())


def get_voicings(pset):
    voicings = [list(x) for x in permutations(pset)]
    for i in range(len(voicings)):
        for b in range(len(voicings[i]) - 1):
            while voicings[i][b] >= voicings[i][b + 1]:
                voicings[i][b + 1] += 12
    return sort_psets(normalize_sets(voicings))


def get_intervals(pset):
    big_iset = []
    for i in range(1, len(pset)):
        lil_iset = []
        for j in range(len(pset) - i):
            lil_iset.append(pset[i + j] - pset[j])
        big_iset.append(lil_iset)
    return big_iset


def get_permuted_intervals(iset):
    perm_iset = []
    for i in permutations(iset):
        if i not in perm_iset:
            perm_iset.append(list(i))
    return prune_copies(perm_iset)


def get_pitches_from_intervals(iset):
    perm_pset = []
    for i in range(len(iset)):
        p = 0
        perm_pset.append([0])
        for j in iset[i]:
            p += j
            perm_pset[i].append(p)
    return perm_pset


def transpose_pitches(pset, trans):
    trans_pset = []
    for i in pset:
        trans_pset.append(i + trans)
    if min(trans_pset) < 0:
        x = (min(trans_pset) % 12) + abs(min(trans_pset))
        for i in range(len(trans_pset)):
            trans_pset[i] += x
    return trans_pset


def get_permuted_interval_pitches(pset):
    intervals = get_intervals(pset)
    return get_pitches_from_intervals(get_permuted_intervals(intervals[0]))


# this fucked up loop will be performed n times on a single list pset
def fucked_permutation_loop(pset, n):
    outset = [pset]
    for i in range(n):
        for p in range(len(outset)):
            for j in get_permuted_interval_pitches(outset[p]):
                outset.extend(get_voicings(j))
        outset = prune_copies(outset)
    return outset
