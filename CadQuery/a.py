from doctest import debug

from cadquery import exporters
from cadquery import *
from cadquery.vis import show

thickness = 0.5
width = 2.0
result = Workplane("front").box(width, width, thickness).faces(">Z").hole(thickness)
highlight = result.faces('>Z')

show(result)
debug(highlight)
