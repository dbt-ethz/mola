from __future__ import division

#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import math
from mola.core import Vertex
'''
def vec_add(v1,v2):
    return Vertex(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)
'''
'''
def vec_angle(v1,v2):
    a = vec_unitize(v1)
    b = vec_unitize(v2)
    f = vec_dot(a, b)
    f = min(1, max(-1, f))
    return math.acos(f)
'''
'''
def vec_angle_triangle(vPrevious,v,vNext):
  #law of cosines
  vvn = vec_distance(v, vNext)
  vvp = vec_distance(vPrevious, v)
  vnvp = vec_distance(vNext, vPrevious)
  return math.acos((vvn * vvn + vvp * vvp - vnvp * vnvp) / (2 * vvn * vvp))
'''
'''
def vec_subtract(v1,v2):
    """
    subtracts the position vector of v2 from the position vector of v1
    and returns the result as a new Vertex.
    """
    return Vertex(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)

def vec_scale(v,factor):
    """
    scales the position vector of a Vertex by a factor (multiplication)
    and returns the result as a new Vertex.
    """
    return Vertex(v.x * factor, v.y * factor, v.z * factor)
'''
'''
def vec_divide(v,factor):
    """
    scales the position vector of a Vertex by a factor (division)
    and returns the result as a new Vertex.
    """
    return Vertex(v.x / factor, v.y / factor, v.z / factor)
'''
'''
def vec_length(v):
    """
    returns the length of the position vector of a Vertex,
    the distance from the origin (0,0,0).
    """
    return math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z)

def vec_unitize(v):
    """
    returns a Vertex of the same direction
    and of unit length 1
    """
    l = vec_length(v)
    if l == 0:
        return v
    return vec_scale(v,1/l)
'''
'''
def vec_cross(v1,v2):
    return Vertex(v1.y * v2.z - v2.y * v1.z, v1.z * v2.x - v2.z * v1.x, v1.x * v2.y - v2.x * v1.y)
'''
'''
def vec_dot(v1,v2):
    """
    returns the dot product of v1 and v2.
    """
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z
'''
'''
def vec_distance(v1,v2):
    """
    returns the distance between v1 and v2.
    """
    dX = v2.x - v1.x
    dY = v2.y - v1.y
    dZ = v2.z - v1.z
    return math.sqrt(dX*dX+dY*dY+dZ*dZ)
'''
'''
def vec_center(v1,v2):
    return Vertex((v1.x+v2.x)/2,(v1.y+v2.y)/2,(v1.z+v2.z)/2)
'''
'''
def vec_between_rel(v1, v2, factor):
    """
    finds a position vector between v1 and v2 by a factor (0.0 to 1.0 corresponds to v1 to v2)
    and returns the result as a new Vertex.
    """
    return Vertex((v2.x - v1.x) * factor + v1.x, (v2.y - v1.y) * factor + v1.y, (v2.z - v1.z) * factor + v1.z)

def vec_between_abs(v1, v2, dis):
    """
    finds a position vector between v1 and v2 by an absolute distance value from v1
    and returns the result as a new Vertex.
    """
    d = vec_distance(v1,v2)
    return vec_between_rel(v1, v2, dis / d)
'''
'''
def lineLineIntersection(a,b,c,d):
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
'''
'''
def offsetLine(v1, v2, offset):
    v = vec_subtract(v2, v1)
    v = vec_unitize(v)
    v = vec_scale(v,offset)
    t = v.x
    v.x = -v.y
    v.y = t
    v.z = 0
    return Vertex(vec_add(v1, v), vec_add(v2, v))

def offsetPoint(v1, v2, v3, offset1, offset2):
    line1 = offsetLine(v1, v2, offset1)
    line2 = offsetLine(v2, v3, offset2)
    return lineLineIntersection(line1.x,line1.y,line2.x,line2.y)
'''
'''
def rot2D90(vertex):
    return Vertex(-vertex.y, vertex.x, vertex.z)
'''
