from __future__ import division

#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import math as _math
from mola.core import Vertex as _Vertex

def add(v1,v2):
    return _Vertex(v1.x+v2.x,v1.y+v2.y,v1.z+v2.z)

def angle(v1,v2):
    a=unitize(v1)
    b=unitize(v2)
    f=dot(a,b)
    if f<-1:f=-1
    if f>1:f=1
    return _math.acos(f)

def subtract(v1,v2):
    return _Vertex(v1.x-v2.x,v1.y-v2.y,v1.z-v2.z)

def scale(v,factor):
    return _Vertex(v.x*factor,v.y*factor,v.z*factor)

def divide(v,factor):
    return _Vertex(v.x/factor,v.y/factor,v.z/factor)

def length(v):
    return _math.sqrt(v.x*v.x+v.y*v.y+v.z*v.z)

def unitize(v):
    l=length(v)
    if l==0: return v
    return divide(v,l)

def cross(v1,v2):
    return _Vertex(v1.y * v2.z - v2.y * v1.z, v1.z * v2.x - v2.z * v1.x, v1.x * v2.y - v2.x * v1.y)

def dot(v1,v2):
  return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z

def distance(v1,v2):
  dX=v2.x-v1.x
  dY=v2.y-v1.y
  dZ=v2.z-v1.z
  return _math.sqrt(dX*dX+dY*dY+dZ*dZ)

def center(v1,v2):
    return _Vertex((v1.x+v2.x)/2,(v1.y+v2.y)/2,(v1.z+v2.z)/2)

def betweenRel( v1,  v2,  f):
    return _Vertex((v2.x - v1.x) * f + v1.x, (v2.y - v1.y) * f + v1.y, (v2.z - v1.z) * f + v1.z)

def betweenAbs( v1,  v2,  f):
    d = distance(v1,v2)
    return betweenRel(v1, v2, f / d)

def lineLineIntersection(a,b,c,d):
  deltaABX=b.x - a.x
  deltaABY=b.y - a.y
  deltaDCX=d.x - c.x
  deltaDCY=d.y - c.y
  denominator = deltaABX * deltaDCY - deltaABY * deltaDCX
  if denominator == 0:
    return None
  numerator = (a.y - c.y) * deltaDCX - (a.x - c.x) * deltaDCY
  r = numerator / denominator
  x = a.x + r * deltaABX
  y = a.y + r * deltaABY
  return _Vertex(x,y,0)

def offsetLine(v1, v2,  offset):
  v =subtract(v2, v1)
  v=unitize(v)
  v=scale(v,offset)
  t = v.x
  v.x = -v.y
  v.y = t
  v.z=0
  return _Vertex(add(v1,v),add(v2,v))

def offsetPoint(v1,  v2,  v3,  offset1,  offset2):
  line1= offsetLine(v1, v2, offset1);
  line2= offsetLine(v2, v3, offset2);
  return lineLineIntersection(line1.x,line1.y,line2.x,line2.y)

def rot2D90(vertex):
    return _Vertex(-vertex.y,vertex.x,vertex.z)
