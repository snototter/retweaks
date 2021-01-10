#!/usr/bin/env python
# coding=utf-8
"""
Creates custom SVG templates for my rm2 along with
a .json.inc file which can be used to automagically
register/install these custom templates (see also
./install_templates.py).

Note: this script depends on inkscape (to export PNGs from
the rendered SVGs and to convert SVG text to paths, needed
for compatibility reasons).
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
    """
    Renders a 5x5 mm grid.
    :filename: Output filename of the SVG.
    """
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


def ruled_grid5mm(filename,
                  major_tick_len_horz_mm=5.0,
                  major_tick_len_vert_mm=3.5,
                  tick_label_margin_mm=1,
                  invert_vertical_axis=True,
                  font_size_px=21,
                  landscape=False):
    """
    Renders a 5x5 mm grid with rulers.

    :filename: Output filename of the SVG.

    :major_tick_len_horz_mm: Tick length in [mm] of the horizontal
            rulers' (top and bottom) major ticks. Tick length of
            minor ticks will be 1 mm less.

    :major_tick_len_vert_mm: Tick length in [mm] of the vertical
            rulers' (left and right) major ticks. Tick length of
            minor ticks will be 1 mm less.

    :tick_label_margin_mm: Margin between tip of the major ticks
            and the corresponding label in [mm]. Note: this is not
            an exact value - it will only be exact at the vertical
            rulers in portrait mode (i.e. landscape=False). In any
            other configuration, it will be slightly off (search for
            'text rotation' in SVGs to understand why making this
            exact would be overkill).

    :invert_vertical_axis: If True, ruler marks/labels will increase from
            bottom to top (and left to right). Otherwise, ruler marks/labels
            increase top to bottom (and left to right, too).

    :font_size_px: Size of the ruler font.

    :landscape: Set to True for landscape, False for portrait version
            of this template.
    """
    w_px, h_px, w_mm, h_mm = rm2dimensions()

    dwg = svgwrite.Drawing(filename=filename, height=f'{h_px}px', width=f'{w_px}px',
                           profile='tiny', debug=False)
    # Height/width weren't set properly (my SVGs had 100% instead of the correct
    # dimensions). Thus, overwrite the attributes manually:
    dwg.attribs['height'] = f'{h_px}px'
    dwg.attribs['width'] = f'{w_px}px'

    # Add style definitions
    dwg.defs.add(dwg.style("""
    .grid { stroke: black; stroke-width: 0.5px; }
    .ruler { stroke: black; stroke-width: 1px; }
    .ruler-major { stroke: black; stroke-width: 3px; }
    .mark { stroke: black; stroke-width: 2px;}
    .txt { font-size: """ + str(font_size_px) + """px; font-family: xkcd; fill: #808080; dominant-baseline: central; }
    """))
    # Background should not be transparent to avoid "funny" eraser or export 
    # behavior (according to some reddit posts I can't find anymore...)
    dwg.add(dwg.rect(insert=(0, 0), size=(w_px, h_px), fill='white'))

    # Millimeter to pixel conversion
    def ymm2px(y_mm):
        return y_mm / h_mm * h_px

    def xmm2px(x_mm):
        return x_mm / w_mm * w_px

    # Draw grid: Horizontal lines
    grid = dwg.add(dwg.g(id='hlines'))
    y_mm = 0
    while y_mm + 2*major_tick_len_horz_mm <= h_mm:
        y_px = ymm2px(y_mm + major_tick_len_horz_mm)
        grid.add(dwg.line(start=(0, y_px), end=(w_px, y_px),
                          class_='grid'))
        y_mm += 5

    # Draw grid: Vertical lines
    grid = dwg.add(dwg.g(id='vlines'))
    x_mm = 0
    while x_mm + 2*major_tick_len_vert_mm <= w_mm:
        x_px = xmm2px(x_mm + major_tick_len_vert_mm)
        grid.add(dwg.line(start=(x_px, 0), end=(x_px, h_px),
                          class_='grid'))
        x_mm += 5

    # Compute length of minor ticks (every 5 mm)
    minor_tick_len_horz_mm = major_tick_len_horz_mm - 1.0
    minor_tick_len_vert_mm = major_tick_len_vert_mm - 1.0

    # Add the ruler ticks
    ruler = dwg.add(dwg.g(id='ruler'))
    def hruler(y_px, direction):
        minor_px = ymm2px(minor_tick_len_horz_mm)
        major_px = ymm2px(major_tick_len_horz_mm)
        # Offset (left) is the length (width) of the
        # vertical ruler's major ticks!
        max_x_tick = ((w_mm - 2*major_tick_len_vert_mm) // 10) * 10
        x_mm = 0
        while x_mm + 2*major_tick_len_vert_mm <= w_mm:
            x_px = xmm2px(x_mm + major_tick_len_vert_mm)
            is_major = (x_mm % 5) == 0
            y_end = y_px + direction * (major_px if is_major else minor_px)
            ruler.add(dwg.line(start=(x_px, y_px), end=(x_px, y_end),
                              class_='ruler-major' if is_major else 'ruler'))
            if x_mm % 10 == 0 and x_mm > 0 and x_mm < w_mm - 2*major_tick_len_vert_mm:
                y = y_px + direction * (major_px + ymm2px(tick_label_margin_mm) + font_size_px / 2)
                if landscape:
                    # qad: additional spacing required due to the rotation
                    y += direction * (font_size_px / 4)
                txt = f'{int(max_x_tick - x_mm)}' if (landscape and invert_vertical_axis) else f'{int(x_mm)}'
                txttag = dwg.text(txt,
                                  insert=(x_px, y),
                                  class_='txt',
                                  text_anchor='middle')
                if landscape:
                    txttag.rotate(angle=-90, center=(x_px, y))
                ruler.add(txttag)
                # ruler.add(dwg.circle(center=(x_px, y), r=2, fill="red"))  # To debug text alignment
            x_mm += 1
    hruler(0, +1)
    hruler(h_px, -1)

    def vruler(x_px, direction):
        minor_px = xmm2px(minor_tick_len_vert_mm)
        major_px = xmm2px(major_tick_len_vert_mm)
        # Offset (top/bottom) is the length of the
        # horizontal ruler's major ticks!
        max_y_tick = ((h_mm - 2*major_tick_len_horz_mm) // 10) * 10
        y_mm = 0
        while y_mm + 2*major_tick_len_horz_mm <= h_mm:
            y_px = ymm2px(y_mm + major_tick_len_horz_mm)
            is_major = (y_mm % 5) == 0
            x_end = x_px + direction * (major_px if is_major else minor_px)
            ruler.add(dwg.line(start=(x_px, y_px), end=(x_end, y_px),
                              class_='ruler-major' if is_major else 'ruler'))
            if y_mm % 10 == 0 and y_mm > 0 and y_mm < h_mm - 2*major_tick_len_horz_mm:
                x = x_px + direction * (major_px + xmm2px(tick_label_margin_mm))
                if landscape:
                    # qad: additional spacing required due to the rotation
                    x += direction * (font_size_px / 3)
                    txt = f'{int(max_y_tick - y_mm)}'
                else:
                    txt = f'{int(max_y_tick - y_mm)}' if invert_vertical_axis else f'{int(y_mm)}'
                anchor = 'middle' if landscape else ('end' if direction < 0 else 'start')
                txttag = dwg.text(txt,
                                  insert=(x, y_px),
                                  class_='txt',
                                  text_anchor=anchor)
                if landscape:
                    txttag.rotate(angle=-90, center=(x, y_px))
                ruler.add(txttag)
                # ruler.add(dwg.circle(center=(x, y_px), r=2, fill="red"))  # To debug text alignment
            y_mm += 1
    vruler(0, +1)
    vruler(w_px, -1)

    # Draw '+' marks
    center_marks = dwg.add(dwg.g(id='marks'))
    def draw_marker(gcx_mm, gcy_mm):
        length_mm = 3
        cx_px = xmm2px(gcx_mm + major_tick_len_vert_mm)
        cy_px = ymm2px(gcy_mm + major_tick_len_horz_mm)
        lh_px = xmm2px(length_mm / 2)
        center_marks.add(dwg.line(start=(cx_px - lh_px, cy_px),
                                  end=(cx_px + lh_px, cy_px),
                                  class_='mark'))
        lh_px = ymm2px(length_mm / 2)
        center_marks.add(dwg.line(start=(cx_px, cy_px - lh_px),
                                  end=(cx_px, cy_px + lh_px),
                                  class_='mark'))

    grid_w_mm = w_mm - 2 * major_tick_len_vert_mm
    grid_h_mm = h_mm - 2 * major_tick_len_horz_mm
    draw_marker(grid_w_mm/2, grid_h_mm/2)
    draw_marker(grid_w_mm/4, grid_h_mm/4)
    draw_marker(3*grid_w_mm/4, grid_h_mm/4)
    draw_marker(grid_w_mm/4, 3*grid_h_mm/4)
    draw_marker(3*grid_w_mm/4, 3*grid_h_mm/4)

    # Draw diagonals at the 4 courners (non-drawing/grid area)
    corners = dwg.add(dwg.g(id='corner'))
    lines = [
        ((0, 0),  # top-left (in portrait mode)
         (major_tick_len_vert_mm, major_tick_len_horz_mm)),
        ((w_mm, 0),  # top-right
         (w_mm-major_tick_len_vert_mm, major_tick_len_horz_mm)),
        ((w_mm, h_mm),  # bottom-right
         (w_mm-major_tick_len_vert_mm, h_mm - major_tick_len_horz_mm)),
        ((0, h_mm),  # bottom-left
         (major_tick_len_vert_mm, h_mm - major_tick_len_horz_mm))
    ]
    # Unit conversion helper for points (2d coordinates in [mm])
    def mm2px(pt_mm):
        return (xmm2px(pt_mm[0]), ymm2px(pt_mm[1]))

    for ln in lines:
        corners.add(dwg.line(start=mm2px(ln[0]),
                             end=mm2px(ln[1]),
                             class_='ruler'))

    # "Neatification" aka overkill at the corners:
    for x_mm in range(-1, -int(major_tick_len_vert_mm + 0.5), -1):
        # Don't forget: we have an offset between pixel 0 and drawing area/grid
        xpos = x_mm + major_tick_len_vert_mm
        # Length of tick via similar triangles
        y_mm = xpos * major_tick_len_horz_mm / major_tick_len_vert_mm - 0.8
        if y_mm < 0.3:
            continue
        # Top-left
        x_px = xmm2px(xpos)
        y_px = ymm2px(y_mm)
        corners.add(dwg.line(start=(x_px, 0),
                             end=(x_px, y_px),
                             class_='ruler'))
        # Bottom-left
        corners.add(dwg.line(start=(x_px, h_px),
                             end=(x_px, h_px - y_px),
                             class_='ruler'))
        # Top-right
        xpos = w_mm - major_tick_len_vert_mm - x_mm
        x_px = xmm2px(xpos)
        y_px = ymm2px(y_mm)
        corners.add(dwg.line(start=(x_px, 0),
                             end=(x_px, y_px),
                             class_='ruler'))
        # Bottom-right
        corners.add(dwg.line(start=(x_px, h_px),
                             end=(x_px, h_px - y_px),
                             class_='ruler'))

    for y_mm in range(-1, -int(major_tick_len_horz_mm + 0.5), -1):
        # Don't forget: we have an offset between pixel 0 and drawing area/grid
        ypos = y_mm + major_tick_len_horz_mm
        # Length of tick via similar triangles
        x_mm = ypos * major_tick_len_vert_mm / major_tick_len_horz_mm - 0.8
        if x_mm < 0.3:
            continue
        # Top-left
        y_px = ymm2px(ypos)
        x_px = xmm2px(x_mm)
        corners.add(dwg.line(start=(0, y_px),
                             end=(x_px, y_px),
                             class_='ruler'))
        # Top-right
        corners.add(dwg.line(start=(w_px, y_px),
                             end=(w_px - x_px, y_px),
                             class_='ruler'))
        # Bottom-left
        ypos = h_mm - major_tick_len_horz_mm - y_mm
        y_px = ymm2px(ypos)
        corners.add(dwg.line(start=(0, y_px),
                             end=(x_px, y_px),
                             class_='ruler'))
        # Bottom-right
        corners.add(dwg.line(start=(w_px, y_px),
                             end=(w_px - x_px, y_px),
                             class_='ruler'))
    return dwg


def template_dict(name, filename, icon_code,
                  landscape, categories):
    """Returns an entry for remarkable's template.json config file."""
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
Rendering template "{name}"
* SVG file:     "{rmfilename}.svg"
* PNG file:     "{rmfilename}.png"
* JSON snippet: "{rmfilename}.inc.json"
""")
    tpl_desc = list()
    if icon_code_portrait is not None:
        tpl_desc.append(template_dict(
                        name, rmfilename, icon_code_portrait,
                        False, categories))
    if icon_code_landscape is not None:
        tpl_desc.append(template_dict(
                        name, rmfilename, icon_code_landscape,
                        True, categories))
    # Save JSON snippet
    with open(f'{rmfilename}.inc.json', 'w') as jif:
        json.dump(tpl_desc, jif, indent=2)
        jif.write('\n')
    # Save SVG
    svgtpl.save()
    # Convert text to path (to avoid problems with remarkable's PDF export)
    print('* Converting SVG text to path tags (requires inkscape).')
    subprocess.call(f'inkscape "{rmfilename}.svg" --export-text-to-path --export-plain-svg "{rmfilename}.svg"', shell=True)
    # Export to PNG
    print('* Converting SVG to PNG (requires inkscape).')
    subprocess.call(f'inkscape -z -f "{rmfilename}.svg" -w 1404 -h 1872 -j -e "{rmfilename}".png', shell=True)


if __name__ == '__main__':
    # A list of available icons (for a slightly older firmware version) can
    # be found on reddit: https://www.reddit.com/r/RemarkableTablet/comments/j75nis/reference_image_template_icon_codes_for_23016/

    # Render the 5mm grid
    save_template(grid5mm('Grid5mm.svg'),
                  name='Grid 5mm', rmfilename='Grid5mm',
                  icon_code_portrait='\ue99e',
                  icon_code_landscape='\ue9fa',
                  categories=['Grids'])

    # Render a 5mm grid with ruler in portrait mode
    save_template(ruled_grid5mm('GridRulerP.svg'),
                  name='Grid Ruler', rmfilename='GridRulerP',
                  icon_code_portrait='\ue99e',
                  icon_code_landscape=None,
                  categories=['Grids'])

    # Render a 5mm grid with ruler in landscape mode
    save_template(ruled_grid5mm('GridRulerLS.svg', landscape=True),
                  name='Grid Ruler', rmfilename='GridRulerLS',
                  icon_code_portrait=None,
                  icon_code_landscape='\ue9fa',
                  categories=['Grids'])
