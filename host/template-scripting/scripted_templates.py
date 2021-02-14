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
import math


def rm2dimensions():
    """Returns the dimensions of the rm2 screen."""
    # Template size in px
    h_px = 1872
    w_px = 1404
    # Display size in mm
    h_mm = 210
    w_mm = 157
    return w_px, h_px, w_mm, h_mm


def grid5mm(filename, draw_markers=False):
    """
    Renders a 5x5 mm grid.

    :filename: Output filename of the SVG.

    :draw_markers: Draw '+' markers at the page and quadrant centers.
                   These markers will not be aligned with the grid corners
                   due to the display dimensions!
    """
    w_px, h_px, w_mm, h_mm = rm2dimensions()

    dwg = svgwrite.Drawing(filename=filename, height=f'{h_px}px', width=f'{w_px}px',
                           profile='tiny', debug=False)
    # Height/width weren't set properly (my SVGs had 100% instead of the correct
    # dimensions). Thus, overwrite the attributes manually:
    dwg.attribs['height'] = f'{h_px}px'
    dwg.attribs['width'] = f'{w_px}px'

    # Add style definitions
    dwg.defs.add(dwg.style(".grid { stroke: rgb(128,128,128); stroke-width:0.3px; }"))

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

    # Vertical lines (shift to the right, to have the
    # rightmost line aligned with the display border)
    grid = dwg.add(dwg.g(id='vlines'))
    offset_mm = w_mm % 5
    for x_mm in range(0, w_mm+1, 5):
        x_px = xmm2px(x_mm + offset_mm)
        grid.add(dwg.line(start=(x_px, 0), end=(x_px, h_px),
                          class_='grid'))
    
    # Draw '+' marks
    if draw_markers:
        center_marks = dwg.add(dwg.g(id='marks'))
        def draw_marker(gcx_mm, gcy_mm):
            length_mm = 3
            cx_px = xmm2px(gcx_mm)
            cy_px = ymm2px(gcy_mm)
            lh_px = xmm2px(length_mm / 2)
            center_marks.add(dwg.line(start=(cx_px - lh_px, cy_px),
                                    end=(cx_px + lh_px, cy_px),
                                    class_='mark'))
            lh_px = ymm2px(length_mm / 2)
            center_marks.add(dwg.line(start=(cx_px, cy_px - lh_px),
                                    end=(cx_px, cy_px + lh_px),
                                    class_='mark'))

        grid_w_mm = (w_mm // 5) * 5
        grid_h_mm = h_mm
        draw_marker(grid_w_mm/2 + offset_mm, grid_h_mm/2)
        draw_marker(grid_w_mm/4 + offset_mm, grid_h_mm/4)
        draw_marker(3*grid_w_mm/4 + offset_mm, grid_h_mm/4)
        draw_marker(grid_w_mm/4 + offset_mm, 3*grid_h_mm/4)
        draw_marker(3*grid_w_mm/4 + offset_mm, 3*grid_h_mm/4)
    return dwg


def ruled_grid5mm(filename,
                  major_tick_len_horz_mm=5.0,
                  major_tick_len_vert_mm=3.5,
                  tick_label_margin_mm=1,
                  draw_markers=True,
                  draw_corner_diagonals=False,
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

    :draw_markers: Draw '+' markers at the page and quadrant centers.

    :draw_corner_diagonals: Draw diagonals in the corners (where the
            rulers overlap).

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
    .grid { stroke: rgb(128,128,128); stroke-width: 0.3px; }
    .ruler { stroke: black; stroke-width: 1px; }
    .ruler-major { stroke: black; stroke-width: 3px; }
    .mark { stroke: rgb(128,128,128); stroke-width: 2px;}
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
    if draw_markers:
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

    if draw_corner_diagonals:
        for ln in lines:
            corners.add(dwg.line(start=mm2px(ln[0]),
                                end=mm2px(ln[1]),
                                class_='ruler'))

    # "Neatification" aka overkill at the corners:
    for x_mm in range(-1, -int(major_tick_len_vert_mm + 0.5), -1):
        # Don't forget: we have an offset between pixel 0 and drawing area/grid
        xpos = x_mm + major_tick_len_vert_mm
        # Length of tick via similar triangles
        y_mm = xpos * major_tick_len_horz_mm / major_tick_len_vert_mm -\
            (0.8 if draw_corner_diagonals else 0)
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



def print3d_template(filename,
                     major_tick_len_horz_mm=5.0,
                     major_tick_len_vert_mm=3.5,
                     tick_label_margin_mm=1,
                     draw_markers=True,
                     draw_corner_diagonals=False,
                     invert_vertical_axis=True,
                     font_size_px=21,
                     landscape=False):
    dwg = ruled_grid5mm(filename,
                        major_tick_len_horz_mm=major_tick_len_horz_mm,
                        major_tick_len_vert_mm=major_tick_len_vert_mm,
                        tick_label_margin_mm=tick_label_margin_mm,
                        draw_markers=draw_markers,
                        draw_corner_diagonals=draw_corner_diagonals,
                        invert_vertical_axis=invert_vertical_axis,
                        font_size_px=font_size_px,
                        landscape=landscape)
    # Millimeter to pixel conversion
    w_px, h_px, w_mm, h_mm = rm2dimensions()
    def ymm2px(y_mm):
        return y_mm / h_mm * h_px

    def xmm2px(x_mm):
        return x_mm / w_mm * w_px

    # Add the 3d printer task list to the template (top-right)
    insert_x_mm = 133.5 - 2.5
    insert_y_mm = 10
    insert_w_mm = 15
    insert_h_mm = 15
    text_offset_mm = 5
    stroke_width_box = 2
    cb_width_mm = 2.5

    left_px = xmm2px(insert_x_mm) + stroke_width_box/2
    top_px = ymm2px(insert_y_mm) + stroke_width_box/2
    dwg.add(dwg.rect(insert=(left_px, top_px),
                     size=(xmm2px(insert_w_mm) - stroke_width_box, ymm2px(insert_h_mm) - stroke_width_box),
                     fill='white', stroke_width='{:d}'.format(stroke_width_box), stroke='gray'))
    
    txt_offset_px = ymm2px(text_offset_mm)
    txt_left_px = left_px + xmm2px(text_offset_mm)
    dwg.add(dwg.text('Sketched',
                     insert=(txt_left_px, top_px + txt_offset_px/2),
                     class_='txt',
                     text_anchor='start'))
    dwg.add(dwg.text('Sliced',
                     insert=(txt_left_px, top_px + 1.5*txt_offset_px),
                     class_='txt',
                     text_anchor='start'))
    dwg.add(dwg.text('Printed',
                     insert=(txt_left_px, top_px + 2.5*txt_offset_px),
                     class_='txt',
                     text_anchor='start'))
    
    cb_left_px = xmm2px(insert_x_mm + (5-cb_width_mm)/2)

    for i in range(3):
        cb_top_px = top_px + i*txt_offset_px + ymm2px((5-cb_width_mm)/2)
        dwg.add(dwg.rect(insert=(cb_left_px, cb_top_px),
                         size=(xmm2px(cb_width_mm), ymm2px(cb_width_mm)),
                         fill='white', stroke_width='{:d}'.format(stroke_width_box), stroke='gray'))

    return dwg


def gardening_planner(filename, font_size_px=42):
    """
    Renders a quarterly gardening task list/planner.

    :filename: Output filename of the SVG.

    :font_size_px: Font size of the title in pixels.
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
.grid { stroke: rgb(128,128,128); stroke-width:3px; }
.txt { font-size: """ + str(font_size_px) + """px; font-family: xkcd; fill: #404040; dominant-baseline: central; }
"""))

    # Background should not be transparent
    dwg.add(dwg.rect(insert=(0, 0), size=(w_px, h_px), class_='grid', fill='white'))

    # Millimeter to pixel conversion
    def ymm2px(y_mm):
        return y_mm / h_mm * h_px

    def xmm2px(x_mm):
        return x_mm / w_mm * w_px
    
    # Size definitions
    title_height_mm = 10
    month_title_height_mm = 7
    guide_cell_size_mm = 5

    # Horizontal lines
    grid = dwg.add(dwg.g(id='hlines'))
    evenly_spaced = (h_mm - title_height_mm) / 3
    month_height_mm = (evenly_spaced // guide_cell_size_mm) * guide_cell_size_mm
    hline_positions = [0,
        title_height_mm,
        title_height_mm + month_height_mm,
        title_height_mm + 2 * month_height_mm,
        h_mm]
    for y_mm in hline_positions:
        y_px = ymm2px(y_mm)
        grid.add(dwg.line(start=(0, y_px), end=(w_px, y_px),
                          class_='grid'))
    
    # Vertical lines
    grid = dwg.add(dwg.g(id='vlines'))
    for x_mm in [0, w_mm-month_title_height_mm, w_mm]:
        x_px = xmm2px(x_mm)
        grid.add(dwg.line(start=(x_px, ymm2px(title_height_mm)), end=(x_px, h_px),
                          class_='grid'))
    
    # Dots
    y_mm = title_height_mm + guide_cell_size_mm
    while y_mm <= h_mm - guide_cell_size_mm:
        y_px = ymm2px(y_mm)
        if all([abs(y_mm - y) > 1 for y in hline_positions]):
            x_mm = guide_cell_size_mm
            while x_mm <= w_mm - month_title_height_mm - guide_cell_size_mm:
                x_px = xmm2px(x_mm)
                grid.add(dwg.circle(center=(x_px, y_px), r=0.5, class_='grid'))
                x_mm += guide_cell_size_mm
        y_mm += guide_cell_size_mm
    
    dwg.add(dwg.text('Gartenplaner',
                     insert=(xmm2px(0.35*w_mm), ymm2px(title_height_mm/2)),
                     class_='txt',
                     text_anchor='middle'))
    dwg.add(dwg.text('Periode:',
                     insert=(xmm2px(0.65*w_mm), ymm2px(title_height_mm/2)),
                     class_='txt',
                     text_anchor='middle'))
    return dwg


def todo_list(filename, font_size_px=42,
              title_height_mm=10,
              guide_cells_mm=6.5,
              num_guides_per_item=2,
              guide_radius_px=1,
              margin_left_mm=14,
              checkbox_size_mm=3.5,
              distance_box_dots_mm=3.5,
              distance_box_divider_mm=-1.5):
    """
    Renders a todo list (similar to the built-in, but with
    additional dots for orientation and nicer checkbox indentation)

    :filename: Output filename of the SVG.

    :font_size_px: Font size of the title in pixels.

    :title_height_mm: Height of the title in [mm]

    :guide_cells_mm: Size of the guide cells in [mm]

    :num_guides_per_item: Number of "guide rows" per checklist item

    :guide_radius_px: Radius of the guide dots

    :margin_left_mm: Margin between left border and checkboxes in [mm].

    :checkbox_size_mm: Size of each checkbox in [mm]

    :distance_box_dots_mm: Distance between checkbox and guidance dots.

    :distance_box_divider_mm: Distance between checkbox and item divider (can
                              also be negative).
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
.checkbox { stroke: rgb(80,80,80); stroke-width:2px; fill:#ffffff; }
.divider { stroke: rgb(80,80,80); stroke-width:1px; }
.dots { stroke: rgb(128,128,128); stroke-width:1px; }
.txt { font-size: """ + str(font_size_px) + """px; font-family: xkcd; fill: #404040; dominant-baseline: central; }
"""))

    # Background should not be transparent
    dwg.add(dwg.rect(insert=(0, 0), size=(w_px, h_px), class_='grid', fill='white'))

    # Millimeter to pixel conversion
    def ymm2px(y_mm):
        return y_mm / h_mm * h_px

    def xmm2px(x_mm):
        return x_mm / w_mm * w_px
    
    # Pre-computable dimensions:
    w_px = xmm2px(w_mm)
    
    checkbox_left_px = xmm2px(margin_left_mm)    
    # Title text
    dwg.add(dwg.text('Notes & TODOs',
                     insert=(checkbox_left_px, ymm2px(title_height_mm/2 + 1)), #insert=(xmm2px(0.35*w_mm), ymm2px(title_height_mm/2 + 1)),
                     class_='txt',
                     text_anchor='start')) # text_anchor='middle'))
    dwg.add(dwg.text('Date:',
                     insert=(xmm2px(0.75*w_mm), ymm2px(title_height_mm/2 + 1)),
                     class_='txt',
                     text_anchor='middle'))
    
    # Group all lines and dots
    grid = dwg.add(dwg.g(id='grid'))
    y_px = ymm2px(title_height_mm)
    grid.add(dwg.line(start=(0, y_px), end=(w_px, y_px),
                      class_='divider'))

    num_rows = (h_mm - title_height_mm) / guide_cells_mm
    num_items = math.floor(num_rows / num_guides_per_item)
    guide_row = 0
    item_count = 0
    y_mm = title_height_mm

    checkbox_offsety_px = ymm2px((num_guides_per_item * guide_cells_mm - checkbox_size_mm) / 2)
    checkbox_width_px = xmm2px(checkbox_size_mm)
    checkbox_height_px = ymm2px(checkbox_size_mm)
    guide_left_px = xmm2px(margin_left_mm
                           + checkbox_size_mm
                           + distance_box_dots_mm)
    guide_width_px = xmm2px(guide_cells_mm)
    divider_left_px = xmm2px(margin_left_mm
                             + checkbox_size_mm
                             + distance_box_divider_mm)
    while guide_row < num_rows:
        y_px = ymm2px(y_mm)
        if (guide_row % num_guides_per_item == 0) and (item_count < num_items):
            x_px = 0 if guide_row == 0 else divider_left_px            
            grid.add(dwg.line(start=(x_px, y_px), end=(w_px, y_px),
                              class_='divider'))
            # Draw checkbox
            grid.add(dwg.rect(insert=(checkbox_left_px, y_px + checkbox_offsety_px),
                              size=(checkbox_width_px, checkbox_height_px),
                              class_='checkbox'))
            item_count += 1
        else:
            # Draw dots for guidance
            x_px = guide_left_px
            while x_px < w_px:
                grid.add(dwg.circle(center=(x_px, y_px), r=guide_radius_px, class_='dots'))
                x_px += guide_width_px
        guide_row += 1
        y_mm += guide_cells_mm

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


def save_template(svgtpl_export, svgtpl_display, name, rmfilename,
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
    #### Export to PNG first, if we have a separate display template
    if svgtpl_display is not None:
        # Save the corresponding SVG
        print('* Saving the display template as SVG')
        svgtpl_display.save()
        # Convert text to path
        print('* Converting SVG text to path tags (requires inkscape).')
        subprocess.call(f'inkscape "{rmfilename}.svg" --export-text-to-path --export-plain-svg "{rmfilename}.svg"', shell=True)
        # Export to PNG
        print('* Converting SVG to PNG (requires inkscape).')
        subprocess.call(f'inkscape -z -f "{rmfilename}.svg" -w 1404 -h 1872 -j -e "{rmfilename}".png', shell=True)

    # Save SVG
    svgtpl_export.save()
    # Convert text to path (to avoid problems with remarkable's PDF export)
    print('* Converting SVG text to path tags (requires inkscape).')
    subprocess.call(f'inkscape "{rmfilename}.svg" --export-text-to-path --export-plain-svg "{rmfilename}.svg"', shell=True)
    # Export to PNG (if there's no separate display template)
    if svgtpl_display is None:
        print('* Converting SVG to PNG (requires inkscape).')
        subprocess.call(f'inkscape -z -f "{rmfilename}.svg" -w 1404 -h 1872 -j -e "{rmfilename}".png', shell=True)


if __name__ == '__main__':
    # A list of available icons (for a slightly older firmware version) can
    # be found on reddit: https://www.reddit.com/r/RemarkableTablet/comments/j75nis/reference_image_template_icon_codes_for_23016/

    # Render the 5mm grid
    save_template(grid5mm('Grid5mm.svg'), None,
                  name='Grid 5mm', rmfilename='Grid5mm',
                  icon_code_portrait='\ue99e',
                  icon_code_landscape='\ue9fa',
                  categories=['Grids'])

    # Render a 5mm grid with ruler in portrait mode
    save_template(ruled_grid5mm('GridRulerP.svg', draw_markers=False),
                  ruled_grid5mm('GridRulerP.svg', draw_markers=True),
                  name='Grid Ruler', rmfilename='GridRulerP',
                  icon_code_portrait='\ue99e',
                  icon_code_landscape=None,
                  categories=['Grids'])

    # Render a 5mm grid with ruler in landscape mode
    save_template(ruled_grid5mm('GridRulerLS.svg', landscape=True, draw_markers=False),
                  ruled_grid5mm('GridRulerLS.svg', landscape=True, draw_markers=True),
                  name='Grid Ruler', rmfilename='GridRulerLS',
                  icon_code_portrait=None,
                  icon_code_landscape='\ue9fa',
                  categories=['Grids'])
    
    # 3D printer template (5mm grid with ruler in portrait mode)
    save_template(print3d_template('Print3dP.svg', draw_markers=False),
                  print3d_template('Print3dP.svg', draw_markers=True),
                  name='3D Printing', rmfilename='Print3dP',
                  icon_code_portrait='\ue99e',
                  icon_code_landscape=None,
                  categories=['Grids'])
    
    # Render a gardening plan/todo list
    save_template(gardening_planner('GardeningP.svg'),
                  None,
                  name='Gardening', rmfilename='GardeningP',
                  icon_code_portrait='\ue98f',
                  icon_code_landscape=None,
                  categories=['Life/organize'])

    # Render a generic todo list
    save_template(todo_list('TodoListP.svg'),
                  None,
                  name='TODOs', rmfilename='TodoListP',
                  icon_code_portrait='\ue98f',
                  icon_code_landscape=None,
                  categories=['Life/organize'])
