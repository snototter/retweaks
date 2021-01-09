#!/usr/bin/env python
# coding=utf-8
"""
Creates custom SVG templates for my rm2 along with
a .json.inc file which can be used to automagically
register these custom templates.
TODO reference the upload/register script once implemented
"""

import os
import sys

import svgwrite

def rm2dimensions():
    """Returns the dimensions of the rm2 screen."""
    # Template size in px
    hpx = 1872
    wpx = 1404
    # Display size in mm
    hmm = 210
    wmm = 157
    return wpx, hpx, wmm, hmm


def grid5mm(filename):
    wpx, hpx, wmm, hmm = rm2dimensions()

    dwg = svgwrite.Drawing(filename=filename, height=f'{hpx}px', width=f'{wpx}px', profile='tiny', debug=False)
    # Height/width weren't set properly (my SVGs had 100% instead of the correct
    # dimensions). Thus, overwrite the attributes manually:
    dwg.attribs['height'] = f'{hpx}px'
    dwg.attribs['width'] = f'{wpx}px'

    # Add style definitions
    dwg.defs.add(dwg.style(".grid { stroke: black; stroke-width:1px; }"))

    # Background should not be transparent
    dwg.add(dwg.rect(insert=(0, 0), size=(wpx, hpx), fill='white'))

    # Horizontal lines
    grid = dwg.add(dwg.g(id='hlines'))
    for ymm in range(0, hmm+1, 5):
        y = ymm / hmm * hpx
        grid.add(dwg.line(start=(0, y), end=(wpx, y), class_='grid'))

    # Vertical lines (align to the right as the screen is 157mm wide)
    grid = dwg.add(dwg.g(id='vlines'))
    #offsetmm = (wmm % 5) / 2
    offsetmm = wmm % 5
    offsetpx = offsetmm / wmm * wpx
    for xmm in range(0, wmm+1, 5):
        x = xmm / wmm * wpx + offsetpx
        grid.add(dwg.line(start=(x, 0), end=(x, hpx), class_='grid'))
    return dwg


def ruled_grid5mm(filename):
    wpx, hpx, wmm, hmm = rm2dimensions()

    dwg = svgwrite.Drawing(filename=filename, height=f'{hpx}px', width=f'{wpx}px', profile='tiny', debug=False)
    # Height/width weren't set properly (my SVGs had 100% instead of the correct
    # dimensions). Thus, overwrite the attributes manually:
    dwg.attribs['height'] = f'{hpx}px'
    dwg.attribs['width'] = f'{wpx}px'

    # Add style definitions
    dwg.defs.add(dwg.style("""
.grid { stroke: black; stroke-width:0.5px; }
.ruler { stroke: black; stroke-width:1px; }
.txt { font-size:23px; font-family:xkcd; fill: black; text-align: right;}
"""))

    # Background should not be transparent
    dwg.add(dwg.rect(insert=(0, 0), size=(wpx, hpx), fill='white'))

    # Millimeter to pixel conversion
    def ymm2px(ymm):
        return ymm / hmm * hpx
    def xmm2px(xmm):
        return xmm / wmm * wpx

    # Horizontal lines
    grid = dwg.add(dwg.g(id='hlines'))
    for ymm in range(0, hmm+1, 5):
        y = ymm2px(ymm)
        grid.add(dwg.line(start=(0, y), end=(wpx, y), class_='grid'))
    # Vertical lines (align to the right as the screen is 157mm wide)
    grid = dwg.add(dwg.g(id='vlines'))
    #offsetmm = (wmm % 5) / 2
    offsetmm = wmm % 5
    offsetpx = xmm2px(offsetmm)
    for xmm in range(0, wmm+1, 5):
        x = xmm2px(xmm) + offsetpx
        grid.add(dwg.line(start=(x, 0), end=(x, hpx), class_='grid'))

    # Add the ruler ticks
    ruler = dwg.add(dwg.g(id='ruler'))
    minor_tick_lenmm = 6.5
    minor_tick_lenpx = ymm2px(minor_tick_lenmm)
    def hruler(y, direction):
        for xmm in range(-offsetmm, wmm+1):
            x = xmm2px(xmm) + offsetpx
            # if xmm % 5 != 0:
            ruler.add(dwg.line(start=(x, y), 
                end=(x, y + direction * minor_tick_lenpx),
                class_='ruler'))
    hruler(0, +1)
    hruler(hpx, -1)

    minor_tick_lenpx = xmm2px(minor_tick_lenmm)
    def vruler(x, direction):
        for ymm in range(0, hmm+1):
            y = ymm2px(ymm)
            ruler.add(dwg.line(start=(x, y), 
                end=(x + direction * minor_tick_lenpx, y),
                class_='ruler'))
            if ymm % 10 == 0:
                dwg.add(dwg.text(f'{ymm} mm', insert=(x + direction * (minor_tick_lenpx + 10), y), class_='txt'))
                #TODO text
                # left align if direction < 0 else right align
                # margin!
                # (x + direction * (minor_tick_lenpx + margin), y)
    vruler(0, +1)
    vruler(wpx, -1)
    return dwg
    

#https://stackoverflow.com/questions/18057911/how-to-convert-text-to-paths
# export to pdf
# convert text to path!
    

def save_template(svgtpl, name, rmfilename, include_in_landscape=False):
    print(f"""
##############################################################
Saving template  "{name}"
* SVG file:      "{rmfilename}.svg"
* JSON snipplet: "{rmfilename}.json.inc"
# """)
    print(f'TODO!!!!!! save {rmfilename}')
    # TODO store json.inc
    svgtpl.save()


if __name__ == '__main__':
    # 5mm grid
    save_template(grid5mm('Grid5mm.svg'), 'Grid 5mm', 'Grid5mm', True)
    save_template(ruled_grid5mm('GridRuler.svg'), 'Grid Ruler', 'GridRuler', True)
    
