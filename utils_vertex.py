from __future__ import division

#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import math
from mola.core_vertex import Vertex
from mola import utils_math

def vertex_add(v1,v2):
    """
    adds the position vector of v2 to the position vector of v1
    and returns the result as a new Vertex.
    """
    return Vertex(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)

def vertex_subtract(v1,v2):
    """
    subtracts the position vector of v2 from the position vector of v1
    and returns the result as a new Vertex.
    """
    return Vertex(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)

def vertex_scale(v,factor):
    """
    scales the position vector of a Vertex by a factor (multiplication)
    and returns the result as a new Vertex.
    """
    return Vertex(v.x * factor, v.y * factor, v.z * factor)

def vertex_divide(v,factor):
    """
    scales the position vector of a Vertex by a factor (division)
    and returns the result as a new Vertex.
    """
    return Vertex(v.x / factor, v.y / factor, v.z / factor)

def vertex_center(v1,v2):
    """
    Returns the center of a line defined by two vertices.

    Arguments:
    ----------
    v1, v2 : mola.Vertex
        start and end points of the line

    Returns:
    --------
    mola.Vertex
        the center point of the line
    """

    return Vertex((v1.x+v2.x)/2,(v1.y+v2.y)/2,(v1.z+v2.z)/2)

def vertex_unitize(v):
    """
    returns a Vertex of the same direction
    and of unit length 1
    """
    l = vertex_length(v)
    if l == 0:
        return v
    return vertex_scale(v,1/l)

def vertex_angle(v1,v2):
    a = vertex_unitize(v1)
    b = vertex_unitize(v2)
    f = vertex_dot(a, b)
    f = min(1, max(-1, f))
    return math.acos(f)

def vertex_angle_triangle(vPrevious,v,vNext):
    #law of cosines
    vvn = vertex_distance(v, vNext)
    vvp = vertex_distance(vPrevious, v)
    vnvp = vertex_distance(vNext, vPrevious)
    return math.acos((vvn * vvn + vvp * vvp - vnvp * vnvp) / (2 * vvn * vvp))

def vertex_length(v):
    """
    returns the length of the position vector of a Vertex,
    the distance from the origin (0,0,0).
    """
    return math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z)

def vertex_dot(v1,v2):
    """
    returns the dot product of v1 and v2.
    """
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

def vertex_cross(v1,v2):
    """
    returns the cross product of v1 and v2 as a new Vertex.
    """
    return Vertex(v1.y * v2.z - v2.y * v1.z, v1.z * v2.x - v2.z * v1.x, v1.x * v2.y - v2.x * v1.y)

def vertex_distance(v1,v2):
    """
    returns the distance between v1 and v2.
    """
    dX = v2.x - v1.x
    dY = v2.y - v1.y
    dZ = v2.z - v1.z
    return math.sqrt(dX*dX+dY*dY+dZ*dZ)

def vertex_between_rel(v1, v2, factor):
    """
    finds a position vector between v1 and v2 by a factor (0.0 to 1.0 corresponds to v1 to v2)
    and returns the result as a new Vertex.
    """
    return Vertex((v2.x - v1.x) * factor + v1.x, (v2.y - v1.y) * factor + v1.y, (v2.z - v1.z) * factor + v1.z)

def vertex_between_abs(v1, v2, dis):
    """
    finds a position vector between v1 and v2 by an absolute distance value from v1
    and returns the result as a new Vertex.
    """
    d = vertex_distance(v1,v2)
    return vertex_between_rel(v1, v2, dis / d)

def vertex_rotate_2D_90(vertex):
    return Vertex(-vertex.y, vertex.x, vertex.z)


def vertex_offset_line(v1, v2, offset):
    v = vertex_subtract(v2, v1)
    v = vertex_unitize(v)
    v = vertex_scale(v,offset)
    t = v.x
    v.x = -v.y
    v.y = t
    v.z = 0
    return Vertex(vertex_add(v1, v), vertex_add(v2, v))

def vertex_offset_point(v1, v2, v3, offset1, offset2):
    line1 = vertex_offset_line(v1, v2, offset1)
    line2 = vertex_offset_line(v2, v3, offset2)
    return vertex_line_line_intersection(line1.x,line1.y,line2.x,line2.y)

def vertex_line_line_intersection(a,b,c,d):
    """
    Returns the intersection of two lines in 2D as a new Vertex.

    Arguments:
    ----------
    a,b,c,d: mola.Vertex
             a,b are the endpoints of line1
             c,d are the endpoints of line2
    """
    deltaABX = b.x - a.x
    deltaABY = b.y - a.y
    deltaDCX = d.x - c.x
    deltaDCY = d.y - c.y
    denominator = deltaABX * deltaDCY - deltaABY * deltaDCX
    if denominator == 0:
        return None
    numerator = (a.y - c.y) * deltaDCX - (a.x - c.x) * deltaDCY
    r = numerator / denominator
    x = a.x + r * deltaABX
    y = a.y + r * deltaABY
    return Vertex(x,y,0)


"""// VERTICES LIST //"""

def vertices_list_normal(vertices):
    """
    Returns the normal of a triangle defined by 3 vertices.
    The normal is a vector of length 1 perpendicular to the plane of the triangle.

    Arguments:
    ----------
    vertices : list
        the list of vertices get the normal from (first 3 will be used)
    """
    return normalFromTriangle(vertices[0], vertices[1], vertices[2])

def vertices_list_area(vertices):
    """
    Returns the area of a face from a list of 3 or 4 vertices
    """
    if len(vertices) == 3:
        return triangle_area(vertices[0],vertices[1],vertices[2])
    # could be made generic for n-gons, triangle fan?
    elif len(vertices) == 4:
        a1 = triangle_area(vertices[0], vertices[1], vertices[2])
        a2 = triangle_area(vertices[2], vertices[3], vertices[0])
        return a1 + a2

def vertices_list_center(vertices):
    """
    Returns the center point (type Vertex) of a list of vertices.
    Note: not the center of gravity, just the average of the vertices.

    Arguments:
    ----------
    vertices : list of mola.Vertex
            The list of vertices to be measured
    """
    n = len(vertices)
    cx = sum([v.x for v in vertices]) / n
    cy = sum([v.y for v in vertices]) / n
    cz = sum([v.z for v in vertices]) / n
    return Vertex(cx,cy,cz)


"""// TRIANGLE //"""

def triangle_area(v1,v2,v3):
    """
    Returns the area of the triangle from 3 vertices

    Arguments:
    ----------
    v1, v2, v3 : mola.Vertex
        vertices of the triangle
    """
    return triangle_coords_area(v1.x, v1.y, v1.z, v2.x, v2.y, v2.z, v3.x, v3.y, v3.z)

def triangle_normal(v1,v2,v3):
    """
    Returns the normal of a triangle defined by 3 vertices.
    The normal is a vector of length 1 perpendicular to the plane of the triangle.

    Arguments:
    ----------
    v1, v2, v3 : mola.Vertex
        the vertices get the normal from
    """
    v = v2-v1
    u = v3-v1
    crossProduct=vertex_cross(v, u)
    return vertex_unitize(crossProduct)

def triangle_coords_area(xa, ya, za, xb, yb, zb, xc, yc, zc):
    """
    Returns the area of the triangle from 9 coordinates

    Arguments:
    ----------
    xa, ya, za : float
        coordinates of vertex a
    xb, yb, zb : float
        coordinates of vertex b
    xc, yc, zc : float
        coordinates of vertex c
    """
    return 0.5 * math.sqrt(math.pow(utils_math.math_determinant(xa, xb, xc, ya, yb, yc, 1, 1, 1), 2) + math.pow(utils_math.math_determinant(ya, yb, yc, za, zb, zc, 1, 1, 1), 2) + math.pow(utils_math.math_determinant(za, zb, zc, xa, xb, xc, 1, 1, 1), 2))
