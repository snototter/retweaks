#!/usr/bin/env python
# coding=utf-8
"""
Creates custom SVG templates for my rm2 along with
a .json.inc file which can be used to automagically
register these custom templates.
TODO reference the upload/register script once implemented
TODO requires installed inkscape
"""

import os
import sys
import subprocess
import svgwrite
import json

def rm2dimensions():
    """Returns the dimensions of the rm2 screen."""
    # Template size in px
    h_px = 1872
    w_px = 1404
    # Display size in mm
    h_mm = 210
    w_mm = 157
    return w_px, h_px, w_mm, h_mm


def grid5mm(filename):
    w_px, h_px, w_mm, h_mm = rm2dimensions()

    dwg = svgwrite.Drawing(filename=filename, height=f'{h_px}px', width=f'{w_px}px',
                           profile='tiny', debug=False)
    # Height/width weren't set properly (my SVGs had 100% instead of the correct
    # dimensions). Thus, overwrite the attributes manually:
    dwg.attribs['height'] = f'{h_px}px'
    dwg.attribs['width'] = f'{w_px}px'

    # Add style definitions
    dwg.defs.add(dwg.style(".grid { stroke: black; stroke-width:1px; }"))

    # Background should not be transparent
    dwg.add(dwg.rect(insert=(0, 0), size=(w_px, h_px), fill='white'))

    # Horizontal lines
    grid = dwg.add(dwg.g(id='hlines'))
    for y_mm in range(0, h_mm+1, 5):
        y_px = y_mm / h_mm * h_px
        grid.add(dwg.line(start=(0, y_px), end=(w_px, y_px),
                          class_='grid'))

    # Vertical lines (I prefer centering them)
    grid = dwg.add(dwg.g(id='vlines'))
    offset_mm = w_mm % 5
    offset_px = offset_mm / w_mm * w_px
    for x_mm in range(0, w_mm+1, 5):
        x_px = x_mm / w_mm * w_px + offset_px
        grid.add(dwg.line(start=(x_px, 0), end=(x_px, h_px),
                          class_='grid'))
    return dwg

def ruled_grid5mm(filename):
    w_px, h_px, w_mm, h_mm = rm2dimensions()

    dwg = svgwrite.Drawing(filename=filename, height=f'{h_px}px', width=f'{w_px}px',
                           profile='tiny', debug=False)
    # Height/width weren't set properly (my SVGs had 100% instead of the correct
    # dimensions). Thus, overwrite the attributes manually:
    dwg.attribs['height'] = f'{h_px}px'
    dwg.attribs['width'] = f'{w_px}px'

    # Add style definitions
    dwg.defs.add(dwg.style("""
.grid { stroke: black; stroke-width:0.3px; }
.ruler { stroke: black; stroke-width:1px; }
.txt { font-size:23px; font-family:xkcd; fill: black; dominant-baseline: middle;}
"""))

    # Background should not be transparent
    dwg.add(dwg.rect(insert=(0, 0), size=(w_px, h_px), fill='white'))

    # Millimeter to pixel conversion
    def ymm2px(y_mm):
        return y_mm / h_mm * h_px
    def xmm2px(x_mm):
        return x_mm / w_mm * w_px

    # Horizontal lines
    grid = dwg.add(dwg.g(id='hlines'))
    for y_mm in range(0, h_mm+1, 5):
        y_px = ymm2px(y_mm)
        grid.add(dwg.line(start=(0, y_px), end=(w_px, y_px),
                          class_='grid'))
    # Vertical lines (align to the right as the screen is 157mm wide)
    grid = dwg.add(dwg.g(id='vlines'))
    offset_mm = w_mm % 5
    offset_px = xmm2px(offset_mm)
    for x_mm in range(0, w_mm+1, 5):
        x_px = xmm2px(x_mm) + offset_px
        grid.add(dwg.line(start=(x_px, 0), end=(x_px, h_px),
                          class_='grid'))

    # Add the ruler ticks
    ruler = dwg.add(dwg.g(id='ruler'))
    minor_tick_len_mm = 4.5
    minor_tick_len_px = ymm2px(minor_tick_len_mm)
    def hruler(y_px, direction):
        for x_mm in range(-offset_mm, w_mm+1):
            x_px = xmm2px(x_mm) + offset_px
            ruler.add(dwg.line(start=(x_px, y_px), 
                              end=(x_px, y_px + direction * minor_tick_len_px),
                              class_='ruler'))
    hruler(0, +1)
    hruler(h_px, -1)

    minor_tick_len_px = xmm2px(minor_tick_len_mm)
    tick_margin_px = 10
    def vruler(x_px, direction):
        for y_mm in range(0, h_mm+1):
            y_px = ymm2px(y_mm)
            ruler.add(dwg.line(start=(x_px, y_px),
                               end=(x_px + direction * minor_tick_len_px, y_px),
                               class_='ruler'))
            if y_mm % 10 == 0:
                x = x_px + direction * (minor_tick_len_px + tick_margin_px)
                y = y_px  # text bottom should be slightly above the grid line
                dwg.add(dwg.text(f'{y_mm} mm',
                    insert=(x, y),
                    class_='txt',
                    text_anchor='end' if direction < 0 else 'start'))
    vruler(0, +1)
    vruler(w_px, -1)
    return dwg
    

#https://stackoverflow.com/questions/18057911/how-to-convert-text-to-paths
# export to pdf
# convert text to path!
    
def template_dict(name, filename, icon_code,
                  landscape, categories):
    """Returns a dict for rM's template.json"""
    return {
        'name': name,
        'filename': filename,
        'iconCode': icon_code,
        'landscape': landscape,
        'categories': categories
    }


def save_template(svgtpl, name, rmfilename,
                  icon_code_portrait, icon_code_landscape,
                  categories):
    print(f"""
##############################################################
Saving template  "{name}"
* SVG file:      "{rmfilename}.svg"
* PNG file:      "{rmfilename}.png"
* JSON snipplet: "{rmfilename}.json.inc"
# """)
    tpl_desc = list()
    if icon_code_portrait is not None:
        tpl_desc.append(template_dict(
                        name, rmfilename, icon_code_portrait,
                        False, categories))
    if icon_code_landscape is not None:
        tpl_desc.append(template_dict(
                        name, rmfilename, icon_code_portrait,
                        True, categories))
    print(json.dumps(tpl_desc, indent=4))

    print(f'TODO!!!!!! save {rmfilename}')
    # TODO store json.inc
    svgtpl.save()
    # Convert text to path (to avoid problems with remarkable's PDF export)
    subprocess.call(f'inkscape "{rmfilename}.svg" --export-text-to-path --export-plain-svg "{rmfilename}.svg"', shell=True)
    # Export to PNG
    subprocess.call(f'inkscape -z -f "{rmfilename}.svg" -w 1404 -h 1872 -j -e "{rmfilename}".png', shell=True)


if __name__ == '__main__':
    # A list of available icons (for a slightly older firmware version) can
    # be found on reddit: https://www.reddit.com/r/RemarkableTablet/comments/j75nis/reference_image_template_icon_codes_for_23016/

    # 5mm grid
    save_template(grid5mm('Grid5mm.svg'),
                  name='Grid 5mm', rmfilename='Grid5mm',
                  icon_code_portrait='\\ue99e',
                  icon_code_landscape='\\ue9fa',
                  categories=['Grids'])

    # Ruler with 5mm grid
    save_template(ruled_grid5mm('GridRuler.svg'),
                  name='Grid Ruler', rmfilename='GridRuler',
                  icon_code_portrait='\\ue99e',
                  icon_code_landscape='\\ue9fa',
                  categories=['Grids'])
    
