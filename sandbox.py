# test file

from junkyard import piano
from psets import *
from svglib.svglib import svg2rlg

chord = PSet([0, 3, 5, 10])
voicings = chord.get_voicings()

piano.draw_pianos(voicings, 10)

drawing = svg2rlg('piano.svg')
# renderPM.drawToFile(drawing, "piano.png", fmt="PNG")
