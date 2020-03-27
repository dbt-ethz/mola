#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import math
from mola.core_vertex import Vertex
from mola import utils_math
from mola import utils_vertex

def face_area(face):
    """
    Returns the area of a face, for quads that of two triangles.

    Arguments:
    ----------
    face : mola.Face
            The face to be measured
    """
    if(len(face.vertices) == 3):
        return utils_vertex.triangle_area(face.vertices[0], face.vertices[1], face.vertices[2])
    else:
        return utils_vertex.triangle_area(face.vertices[0], face.vertices[1], face.vertices[2]) + utils_vertex.triangle_area(face.vertices[2], face.vertices[3], face.vertices[0])

def face_perimeter(face):
    """
    Returns the perimeter of a face as the sum of all the edges' lengths.

    Arguments:
    ----------
    face : mola.Face
            The face to be measured
    """
    sum = 0
    for i in range(len(face.vertices)):
        v1 = face.vertices[i]
        v2 = face.vertices[(i + 1) % len(face.vertices)]
        sum += utils_vertex.vertex_distance(v1,v2)
    return sum

def face_compactness(face):
    """
    Returns the compactness of a face as the ratio between area and perimeter.

    Arguments:
    ----------
    face : mola.Face
            The face to be measured
    """
    return face_area(face) / face_perimeter(face)

def face_angle_horizontal(face):
    """
    Returns the azimuth, the orientation of the face around the z-axis in the XY-plane

    Arguments:
    ----------
    face : mola.Face
            The face to be measured
    """
    n = face_normal(face)
    return math.atan2(n.y, n.x)

def face_angle_vertical(f):
    """
    Returns the altitude, 0 if the face is vertical, -Pi/2 if it faces downwards, +Pi/2 if it faces upwards.

    Arguments:
    ----------
    face : mola.Face
            The face to be measured
    """
    n = face_normal(f)
    #nXY = Vertex(n.x, n.y, 0.0)
    #return vecUtils.angle(n, nXY)
    # alternative, probably less computationally intense:
    return math.asin(n.z)

def face_curvature(face):
    """
    Returns the local curvature of a mesh face, by measuring the angle to the neighbour faces.

    Arguments:
    ----------
    face : mola.Face
        The face to be measured
    """
    facenormal = face_normal(face)
    sumD = 0
    vPrev = face.vertices[-1]
    num_faces = 1
    for v in face.vertices:
        edge = v.edge_adjacent_to_vertex(vPrev)
        if edge != None:
            nbFace = edge.face1
            if edge.face1 == face:
                nbFace = edge.face2
            if nbFace != None:
                num_faces += 1
                nbNormal = face_normal(nbFace)
                sumD += utils_vertex.vertex_distance(nbNormal,facenormal)
        vPrev = v
    return sumD / num_faces

def face_center(face):
    """
    Returns the center point (type Vertex) of a face.
    Note: not the center of gravity, just the average of its vertices.

    Arguments:
    ----------
    face : mola.Face
            The face to be measured
    """
    return utils_vertex.vertices_list_center(face.vertices)

def face_normal(face):
    """
    Returns the normal of a face, a vector of length 1 perpendicular to the plane of the triangle.

    Arguments:
    ----------
    face : mola.Face
        the face to get the normal from
    """
    return utils_vertex.triangle_normal(face.vertices[0], face.vertices[1], face.vertices[2])

def face_copy_properties(faceParent,faceChild):
    """
    Copies the properties (color,group,...) of faceParent to faceChild.

    Arguments:
    ----------
    faceParent : mola.Face
                 The face to copy the properties From.
    faceChild : mola.Face
                 The face to copy the properties To.
    """
    faceChild.group = faceParent.group
    faceChild.color = faceParent.color

def face_scale(face, factor=1.0, origin=None):
    if origin is None:
        for v in face.vertices:
            v.scale(factor)
    else:
        for v in face.vertices:
            delta = v - origin
            delta.scale(factor)
            v.x = origin.x + delta.x
            v.y = origin.y + delta.y
            v.z = origin.z + delta.z
    return face