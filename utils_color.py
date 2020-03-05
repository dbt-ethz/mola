#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import colorsys
from mola import utils_face
from mola import utils_math
from math import floor

def color_hue_to_rgb(hue, do_grayscale):
    """
    Converts a color defined as Hue (HSV, saturation and value assumed to be 100%) into red, green and blue
    and returns (r,g,b,1)
    """
    if do_grayscale:
        return (hue, hue, hue, 1)
    else:
        hue = utils_math.math_map(hue, 0.0, 1.0, 0.0, 0.8) #limit hue red-red to red-magenta
        col = colorsys.hsv_to_rgb(hue, 1, 1)
        return (col[0], col[1], col[2], 1) # alpha = 100 %

def color_faces_by_function(faces, faceFunction, do_grayscale=False):
    """
    Assigns a color to all the faces by face-function which has to return a float value for a face as argument,
    from smallest (red) to biggest (purple).

    Arguments:
    ----------
    faces: list of faces to color
    faceFunction : one of the functions `ByCurvature`, `ByArea`, etc.
    ----------
    Optional Arguments:
    ----------
    do_grayscale: Boolean
    """
    values = []
    for face in faces:
        values.append(faceFunction(face))
    valueMin = min(values)
    valueMax = max(values)
    for i, face in enumerate(faces):
        h = utils_math.math_map(values[i],valueMin, valueMax, 0.0, 1.0)
        face.color = color_hue_to_rgb(h, do_grayscale)

def color_map(values=[], colors=[(1,0,0.5),(0,0.5,1)]):
    """
    Maps a value to a color on a custom spectrum.
    The values will be remapped from 0 to 1, the first color will be at 0, the
    last at 1 and all other colors evenly spread between.

    Arguments:
    ----------
    values : list of floats
        the list of values to be mapped
    colors : list of (r,g,b) tuples
        the colors along the spectrum
    """
    value_min = min(values)
    value_max = max(values)
    values_mapped = [utils_math.math_map(v, value_min, value_max, 0.0, 0.999) for v in values]
    interval = 1.0 / (len(colors) - 1)
    output_colors = []
    for v in values_mapped:
        lower_ix = int(floor(v * (len(colors)-1)))
        upper_ix = lower_ix + 1
        rv = (v - (lower_ix * interval)) / interval
        r = (1 - rv) * colors[lower_ix][0] + rv * colors[upper_ix][0]
        g = (1 - rv) * colors[lower_ix][1] + rv * colors[upper_ix][1]
        b = (1 - rv) * colors[lower_ix][2] + rv * colors[upper_ix][2]
        output_colors.append((r,g,b,1))
    return output_colors

def color_faces_by_map(faces, colors):
    if len(faces) > len(colors):
        print('not enough colors for all the faces')
        return
    for f,c in zip(faces, colors):
        f.color = c

def _color_faces_by_list_and_scheme(faces, values=[], scheme=[(1,0,0.5),(0,0.5,1)]):
    """
    Assigns a color to all the faces by a list of values and a list of colors.
    The values will be remapped from 0 to 1, the first color will be at 0, the
    last at 1 and all other colors evenly spread between.

    Arguments:
    ----------
    faces : mola.core.Face
        list of faces to color
    values : list of floats
        one property value for each face
    scheme : list of (r,g,b) tuples
        the colors along the spectrum
    """
    if len(faces) > len(values):
        print('not enough values provided')
        return
    if len(scheme)<2:
        print('at least two colors need to be provided')

    #values = [face_function(f) for f in faces]
    value_min = min(values)
    value_max = max(values)
    values_mapped = [utils_math.math_map(v, value_min, value_max, 0.0, 0.999) for v in values]
    interval = 1.0 / (len(scheme) - 1)
    for i,f in enumerate(faces):
        v = values_mapped[i]
        lower_ix = int(floor(v * (len(scheme)-1)))
        upper_ix = lower_ix + 1
        rv = (v - (lower_ix * interval)) / interval
        r = (1 - rv) * scheme[lower_ix][0] + rv * scheme[upper_ix][0]
        g = (1 - rv) * scheme[lower_ix][1] + rv * scheme[upper_ix][1]
        b = (1 - rv) * scheme[lower_ix][2] + rv * scheme[upper_ix][2]
        f.color = (r,g,b,1)

def color_faces_by_curvature(faces):
    """
    Assigns a color to all the faces by curvature (require topological meshinformation),
    from smallest (red) to biggest (purple).
    """
    color_faces_by_function(faces, utils_face.face_curvature)

def color_faces_by_area(faces):
    """
    Assigns a color to all the faces by area,
    from smallest (red) to biggest (purple).
    """
    color_faces_by_function(faces, utils_face.face_area)

def color_faces_by_perimeter(faces):
    """
    Assigns a color to all the faces by perimeter,
    from smallest (red) to biggest (purple).
    """
    color_faces_by_function(faces, utils_face.face_perimeter)

def color_faces_by_compactness(faces):
    """
    Assigns a color to all the faces by compactness (area/perimeter),
    from smallest (red) to biggest (purple).
    """
    color_faces_by_function(faces, utils_face.face_compactness)

def color_faces_by_horizontal_angle(faces):
    color_faces_by_function(faces, utils_face.face_angle_horizontal)

def color_faces_by_vertical_angle(faces):
    """
    Assigns a color to all the faces by verticality,
    from smallest (red) to biggest (purple).
    """
    color_faces_by_function(faces, utils_face.face_angle_vertical)
