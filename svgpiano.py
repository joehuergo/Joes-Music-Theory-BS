import piano
from voicings import *
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

pset = [0, 156, 225, 1248]
print([note_name(i) for i in [x+12 for x in pset]])

full_list = get_voicings(pset)
[print(i) for i in full_list]

piano.draw_pianos(full_list, 10)
piano.dwg.save()

drawing = svg2rlg('piano.svg')
renderPM.drawToFile(drawing, "file.png", fmt="PNG")
