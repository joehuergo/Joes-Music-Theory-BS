from itertools import permutations
import math
import numpy as np
from misc import *


#############################################
# --- OPERATIONS ON LISTS OF PITCH SETS --- #
#############################################


def filter_intervals(psetlist, filt):
    if type(filt) != list:
        filt = [filt]
    pset_list = []
    intervals = [[i % 12 for i in flatten_list(j.iseqset)] for j in psetlist]
    for i in range(len(psetlist)):
        if not common_data(filt, intervals[i]):
            pset_list.append(psetlist[i])
    return pset_list


def filter_interval_span(psetlist, filt):
    pset_list = []
    iseq = [i.iseqset[0] for i in psetlist]
    for i in range(len(psetlist)):
        if not any(x > filt for x in iseq[i]):
            pset_list.append(psetlist[i])
    return pset_list


def filter_pset_span(psetlist, filt):
    pset_list = []
    for i in psetlist:
        if max(i) - min(i) <= filt:
            pset_list.append(i)
    return pset_list


def sort(psetlist):
    return sorted({tuple(x): x for x in psetlist}.values())


def voice_lead_bass(psetlist):
    for i in range(1, len(psetlist)):
        # tranpose until bass is within an octave of the previous bass
        while math.ceil(abs((psetlist[i][0] - psetlist[i-1][0]) / 12)) > 1:
            if psetlist[i][0] < psetlist[i-1][0]:
                psetlist[i] = transpose(psetlist[i], 12)
            elif psetlist[i][0] > psetlist[i-1][0]:
                psetlist[i] = transpose(psetlist[i], -12)
        if abs(psetlist[i][0] - psetlist[i-1][0]) > 6:
            if psetlist[i][0] < 0:
                psetlist[i] = transpose(psetlist[i], 12)
            elif psetlist[i][0] > 0:
                psetlist[i] = transpose(psetlist[i], -12)
    return psetlist


####################################
# --- OPERATIONS ON PITCH SETS --- #
####################################


def apply_moveset(pset, move_set, iterations, wrap_octave):
    if any(len(i) != len(pset) for i in move_set):
        print("Move sets must be same size as pitch set.")
        return
    psets = [pset]
    for x in range(iterations):
        for i in range(len(move_set)):
            index = x * len(move_set) + i
            psets.append([])
            for j in range(len(move_set[i])):
                psets[index + 1].append(psets[index][j] + move_set[i][j])
    psets = [normalize_negatives(i, wrap_octave) for i in psets]
    return psets


def get_voicings(pset):
    psetlist = [list(x) for x in permutations(pset)]
    for i in range(len(psetlist)):
        for b in range(len(psetlist[i]) - 1):
            while psetlist[i][b] >= psetlist[i][b + 1]:
                psetlist[i][b + 1] += 12
    return psetlist


def normalize(pset):
    if min(pset) < 0 or min(pset) > 11:
        sub = math.floor(min(pset) / 12) * 12
        for i in range(len(pset)):
            pset[i] = pset[i] - sub
    return pset


def get_moveset(pset_list):
    moveset = []
    for i in range(len(pset_list) - 1):
        difference = list(np.array(pset_list[i + 1]) - np.array(pset_list[i]))
        moveset.append(difference)
    return moveset


# wraps around negative pitches to wrap_octave, 0 wraps to first octave, 1 wraps to second, etc
def normalize_negatives(pset, wrap_octave):
    if min(pset) < 0:
        sub = math.floor(min(pset) / 12) * (wrap_octave * 12)
        for i in range(len(pset)):
            pset[i] = pset[i] - sub
    return pset


def permute_distinct(pset):
    perm_iseq = []
    for i in permutations(pset):
        if list(i) not in perm_iseq:
            perm_iseq.append(list(i))
    return perm_iseq


def get_intervals(pset):
    iseqset = []
    for i in range(1, len(pset)):
        iseq = []
        for j in range(len(pset) - i):
            iseq.append(pset[i + j] - pset[j])
        iseqset.append(iseq)
    return iseqset


#######################################
# --- OPERATIONS ON INTERVAL SETS --- #
#######################################


def transpose(pset, trans):
    trans_pset = []
    for i in pset:
        trans_pset.append(i + trans)
    return trans_pset


def intervals_to_pitches(iseq):
    perm_pset = []
    p = 0
    perm_pset.append(0)
    for j in iseq:
        p += j
        perm_pset.append(p)
    return perm_pset