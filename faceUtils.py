#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import math
import mola.vec as vec
from mola.core import Vertex


def area(face):
    """
    Returns the area of a face, for quads that of two triangles.

    Arguments:
    ----------
    face : mola.core.Face
            The face to be measured
    """
    if(len(face.vertices) == 3):
        return areaTriangle3D(face.vertices[0],face.vertices[1],face.vertices[2])
    else:
        return areaTriangle3D(face.vertices[0],face.vertices[1],face.vertices[2]) + areaTriangle3D(face.vertices[2],face.vertices[3],face.vertices[0])

def areaFromVertices(vertices):
    """
    Returns the area of a face from a list of 3 or 4 vertices
    """
    if len(vertices) == 3:
        return areaTriangle3D(vertices[0],vertices[1],vertices[2])
    # could be made generic for n-gons, triangle fan?
    elif len(vertices) == 4:
        a1 = areaTriangle3D(vertices[0],vertices[1],vertices[2])
        a2 = areaTriangle3D(vertices[2],vertices[3],vertices[0])
        return a1+a2

def areaTriangle3D(a,b,c):
    """
    Returns the area of the triangle from 3 vertices

    Arguments:
    ----------
    a, b, c : mola.core.Vertex
        vertices of the triangle
    """
    return areaTriangle3DCoords(a.x,a.y,a.z,b.x,b.y,b.z,c.x,c.y,c.z)

def areaTriangle3DCoords(xa, ya, za, xb, yb, zb, xc, yc, zc):
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
    return 0.5 * math.sqrt(math.pow(__determinant(xa, xb, xc, ya, yb, yc, 1, 1, 1), 2) + math.pow(__determinant(ya, yb, yc, za, zb, zc, 1, 1, 1), 2) + math.pow(__determinant(za, zb, zc, xa, xb, xc, 1, 1, 1), 2))

def __determinant(a, b, c, d, e, f, g, h, i):
    """
    returns the determinant of the 9 values of a 3 x 3 matrix
    """
    return (a * e * i - a * f * h - b * d * i + b * f * g + c * d * h - c * e * g)

def compactness(face):
    """
    Returns the compactness of a face as the ratio between area and perimeter.

    Arguments:
    ----------
    face : mola.core.Face
            The face to be measured
    """
    return area(face)/perimeter(face)


def perimeter(face):
    """
    Returns the perimeter of a face as the sum of all the edges' lengths.

    Arguments:
    ----------
    face : mola.core.Face
            The face to be measured
    """
    sum = 0
    for i in range(len(face.vertices)):
        v1 = face.vertices[i]
        v2 = face.vertices[(i+1)%len(face.vertices)]
        sum += vec.distance(v1,v2)
    return sum

def horizontal_angle(face):
    """
    Returns the azimuth, the orientation of the face around the z-axis in the XY-plane

    Arguments:
    ----------
    face : mola.core.Face
            The face to be measured
    """
    n = normal(face)
    return math.atan2(n.y,n.x)

def vertical_angle(f):
    """
    Returns the altitude, 0 if the face is vertical, -Pi/2 if it faces downwards, +Pi/2 if it faces upwards.

    Arguments:
    ----------
    face : mola.core.Face
            The face to be measured
    """
    n = normal(f)
    #nXY = Vertex(n.x, n.y, 0.0)
    #return vec.angle(n, nXY)
    # alternative, probably less computationally intense:
    return math.asin(n.z)

def curvature(face):
    """
    Returns the local curvature of a mesh face, by measuring the angle to the neighbour faces.

    Arguments:
    ----------
    face : mola.core.Face
            The face to be measured
    """
    facenormal=normal(face)
    sumD=0
    vPrev=face.vertices[-1]
    num_faces = 1
    for v in face.vertices:
        edge=v.getEdgeAdjacentToVertex(vPrev)
        if edge != None:
            nbFace=edge.face1
            if edge.face1==face:
                nbFace=edge.face2
            if nbFace != None:
                num_faces += 1
                nbNormal = normal(nbFace)
                sumD+=vec.distance(nbNormal,facenormal)
        vPrev=v
    return sumD / num_faces

def center(face):
    """
    Returns the center point (type Vertex) of a face.
    Note: not the center of gravity, just the average of its vertices.

    Arguments:
    ----------
    face : mola.core.Face
            The face to be measured
    """
    return centerFromVertices(face.vertices)

def centerFromVertices(vertices):
    """
    Returns the center point (type Vertex) of a list of vertices.
    Note: not the center of gravity, just the average of the vertices.

    Arguments:
    ----------
    vertices : list of mola.core.Vertex
            The list of vertices to be measured
    """
    n = len(vertices)
    cx = sum([v.x for v in vertices])/n
    cy = sum([v.y for v in vertices])/n
    cz = sum([v.z for v in vertices])/n
    return Vertex(cx,cy,cz)

def centerFromLine(v1,v2):
    """
    Returns the center of a line defined by two vertices.

    Arguments:
    ----------
    v1, v2 : mola.core.Vertex
        start and end points of the line

    Returns:
    --------
    mola.core.Vertex
        the center point of the line
    """
    return Vertex((v1.x+v2.x)/2,(v1.y+v2.y)/2,(v1.z+v2.z)/2)

def normal(face):
    """
    Returns the normal of a face, a vector of length 1 perpendicular to the plane of the triangle.

    Arguments:
    ----------
    face : mola.core.Face
        the face to get the normal from
    """
    return normalFromTriangle(face.vertices[0],face.vertices[1],face.vertices[2])

def normalFromTriangle(v1,v2,v3):
    """
    Returns the normal of a triangle defined by 3 vertices.
    The normal is a vector of length 1 perpendicular to the plane of the triangle.

    Arguments:
    ----------
    v1, v2, v3 : mola.core.Vertex
        the vertices get the normal from
    """
    v = vec.subtract(v2, v1)
    u = vec.subtract(v3, v1)
    crossProduct=vec.cross(v,u)
    return vec.unitize(crossProduct)

def normalFromVertices(vertices):
    """
    Returns the normal of a triangle defined by 3 vertices.
    The normal is a vector of length 1 perpendicular to the plane of the triangle.

    Arguments:
    ----------
    vertices : list
        the list of vertices get the normal from (first 3 will be used)
    """
    return normalFromTriangle(vertices[0],vertices[1],vertices[2])

def copyProperties(faceParent,faceChild):
    """
    Copies the properties (color,group,...) of faceParent to faceChild.

    Arguments:
    ----------
    faceParent : mola.core.Face
                 The face to copy the properties From.
    faceChild : mola.core.Face
                 The face to copy the properties To.
    """
    faceChild.group = faceParent.group
    faceChild.color = faceParent.color
