import piano
from voicings import *
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

pset = [0, 4, 7, 14]

full_list = get_voicings(pset)
print(full_list)

piano.draw_pianos(full_list, 10)
piano.dwg.save()

drawing = svg2rlg('piano.svg')
renderPM.drawToFile(drawing, "file.png", fmt="PNG")
