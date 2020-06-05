import piano
from pset_ops import *
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

pset = [0, 4, 7, 11, 14]
voicings = get_voicings(pset)
print("Original # of chords: " + str(len(voicings)))
voicings = filter_intervals(voicings, [1])
print("# of chords after filter: " + str(len(voicings)))


piano.draw_pianos(voicings, 10)
piano.dwg.save()
#
# drawing = svg2rlg('piano.svg')
# renderPM.drawToFile(drawing, "file.png", fmt="PNG")
