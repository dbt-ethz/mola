#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import colorsys
from mola import utils_face
from mola import utils_math

def color_hue_to_rgb(hue, do_grayscale):
    """
    Converts a color defined as Hue (HSV, saturation and value assumed to be 100%) into red, green and blue
    and returns (r,g,b,1)
    """
    if do_grayscale:
        return (hue,hue,hue,1)
    else:
        hue = utils_math.math_map(hue, 0.0, 1.0, 0.0, 0.8) #limit hue red-red to red-magenta
        col = colorsys.hsv_to_rgb(hue, 1, 1)
        return (col[0], col[1], col[2], 1) # alpha = 100 %

def color_faces_by_function(faces,faceFunction, do_grayscale=False):
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

def color_faces_by_curvature(faces):
    """
    Assigns a color to all the faces by curvature (require topological meshinformation),
    from smallest (red) to biggest (purple).
    """
    color_faces_by_function(faces, utils_face.curvature)

def color_faces_by_area(faces):
    """
    Assigns a color to all the faces by area,
    from smallest (red) to biggest (purple).
    """
    color_faces_by_function(faces, utils_face.area)

def color_faces_by_perimeter(faces):
    """
    Assigns a color to all the faces by perimeter,
    from smallest (red) to biggest (purple).
    """
    color_faces_by_function(faces, utils_face.perimeter)

def color_faces_by_compactness(faces):
    """
    Assigns a color to all the faces by compactness (area/perimeter),
    from smallest (red) to biggest (purple).
    """
    color_faces_by_function(faces, utils_face.compactness)

def color_faces_by_horizontal_angle(faces):
    color_faces_by_function(faces, utils_face.horizontal_angle)

def color_faces_by_vertical_angle(faces):
    """
    Assigns a color to all the faces by verticality,
    from smallest (red) to biggest (purple).
    """
    color_faces_by_function(faces, utils_face.vertical_angle)
