# test file

import piano
from pset_ops import *
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

moveset = [[0, 0, -2, -2], [-1, -1, 1, 1]]

chord = PSet([12, 15, 19, 22])
chord_progression = chord.apply_moveset(moveset, 14, 2)
chord_selection = chord_progression.pset_list[0]
voicings = chord_selection.get_voicings().normalize().filter_interval_span(7).filter_intervals(1)

piano.draw_pianos(voicings, 10)

drawing = svg2rlg('piano.svg')
renderPM.drawToFile(drawing, "piano.png", fmt="PNG")
