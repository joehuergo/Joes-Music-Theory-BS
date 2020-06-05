# test file

import piano
from pset_ops import *
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

cm7 = PSet([0, 3, 7, 10])
cm7_voicings_no_P5 = cm7.get_voicings().filter_intervals(5)

piano.draw_pianos(cm7_voicings_no_P5, 10)

# drawing = svg2rlg('piano.svg')
# renderPM.drawToFile(drawing, "file.png", fmt="PNG")
