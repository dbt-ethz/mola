#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

from mola.core import Mesh as _Mesh
from mola.core import Vertex as _Vertex
from mola.core import Face as _Face
import mola.vec as _vec
import mola.faceUtils as _faceUtils
import math as _math

def constructSingleFace(vertices):
    """
    Creates and returns a single face mesh from the vertices.

    Arguments:
    ----------
    vertices : list of mola.core.Vertex
        The vertices describing the face
    """
    mesh = _Mesh()
    mesh.vertices=vertices
    mesh.faces=[_Face(vertices)]
    return mesh

def constructCone(z1,z2,radius1,radius2,nSegments,capBottom=True,capTop=True):
    """
    Creates and returns a conic cylinder.
    """
    delaAngle=_math.radians(360.0/nSegments)
    angle=0
    verticesBottom=[]
    verticesTop=[]
    for i in range(nSegments):
        x1=radius1*_math.cos(angle)
        y1=radius1*_math.sin(angle)
        verticesBottom.append(_Vertex(x1,y1,z1))
        x2=radius2*_math.cos(angle)
        y2=radius2*_math.sin(angle)
        verticesTop.append(_Vertex(x2,y2,z2))
        angle+=delaAngle
    mesh=_Mesh()
    mesh.vertices.extend(verticesBottom)
    mesh.vertices.extend(verticesTop)
    for i in range(nSegments):
        i2=(i+1)%nSegments
        mesh.faces.append(_Face([verticesBottom[i],verticesBottom[i2],verticesTop[i2],verticesTop[i]]))
    if capBottom:
        centerBottom=_Vertex(0,0,z1)
        mesh.vertices.append(centerBottom)
        for i in range(nSegments):
            i2=(i+1)%nSegments
            mesh.faces.append(_Face([verticesBottom[i],verticesBottom[i2],centerBottom]))
    if capTop:
        centerTop=_Vertex(0,0,z2)
        mesh.vertices.append(centerTop)
        for i in range(nSegments):
            i2=(i+1)%nSegments
            mesh.faces.append(_Face([verticesTop[i],verticesTop[i2],centerTop]))
    return mesh

def constructBox(x1,y1,z1,x2,y2,z2):
    """
    Creates and returns a mesh box with six quad faces.

    Arguments:
    ----------
    x1,y1,z1 : float
        The coordinates of the bottom left front corner
    x2,y2,z2 : float
        The coordinates of the top right back corner
    """
    mesh = _Mesh()
    v1 = _Vertex(x1,y1,z1)
    v2 = _Vertex(x1,y2,z1)
    v3 = _Vertex(x2,y2,z1)
    v4 = _Vertex(x2,y1,z1)
    v5 = _Vertex(x1,y1,z2)
    v6 = _Vertex(x1,y2,z2)
    v7 = _Vertex(x2,y2,z2)
    v8 = _Vertex(x2,y1,z2)
    mesh.vertices=[v1,v2,v3,v4,v5,v6,v7,v8]
    f1 = _Face([v1, v2, v3, v4])
    f2 = _Face([v8, v7, v6, v5])
    f3 = _Face([v4, v3, v7, v8])
    f4 = _Face([v3, v2, v6, v7])
    f5 = _Face([v2, v1, v5, v6])
    f6 = _Face([v1, v4, v8, v5])
    mesh.faces=[f1,f2,f3,f4,f5,f6]
    return mesh

def constructIcosahedron(cx,cy,cz,radius):
    """
    Creates and returns a mesh in the form of an icosahedron.

    Arguments:
    ----------
    cx,cy,cz : float
        The coordinates of the center point
    radius : float
        The radius of the containing sphere
    """
    mesh=_Mesh()
    phi = (1 + 5 ** 0.5) / 2
    coordA = 1/(2*_math.sin(2*_math.pi/5))
    coordB = phi/(2*_math.sin(2*_math.pi/5))
    mesh.vertices = [_Vertex(0,-coordA,coordB),
                _Vertex(coordB, 0, coordA),
                _Vertex(coordB, 0, -coordA),
                _Vertex(-coordB, 0, -coordA),
                _Vertex(-coordB, 0, coordA),
                _Vertex(-coordA, coordB, 0),
                _Vertex(coordA, coordB, 0),
                _Vertex(coordA, -coordB, 0),
                _Vertex(-coordA, -coordB, 0),
                _Vertex(0, -coordA, -coordB),
                _Vertex(0, coordA, -coordB),
                _Vertex(0, coordA, coordB)]

    for i in range(len(mesh.vertices)):
        mesh.vertices[i] = _vec.scale(mesh.vertices[i],radius)
        mesh.vertices[i] = _vec.add(mesh.vertices[i],_Vertex(cx,cy,cz))

    indices = [1, 2, 6, 1, 7, 2, 3, 4, 5, 4, 3, 8, 6, 5, 11, 5, 6, 10, 9, 10, 2, 10, 9, 3, 7, 8, 9, 8, 7, 0, 11, 0, 1, 0, 11, 4, 6, 2, 10, 1, 6, 11, 3, 5, 10, 5, 4, 11, 2, 7, 9, 7, 1, 0, 3, 9, 8, 4, 8, 0]
    faces = []

    for i in range(0,len(indices),3):
        f = _Face([mesh.vertices[indices[i]],mesh.vertices[indices[i + 1]],mesh.vertices[indices[i + 2]]])
        faces.append(f)
    mesh.faces=faces
    return mesh

def constructDodecahedron(cx,cy,cz,radius):
    mesh=_Mesh()
    phi = (1 + 5**0.5)/2
    mesh.vertices = [_Vertex( 1, 1, 1),
                _Vertex( 1, 1,-1),
                _Vertex( 1,-1, 1),
                _Vertex( 1,-1,-1),
                _Vertex(-1, 1, 1),
                _Vertex(-1, 1,-1),
                _Vertex(-1,-1, 1),
                _Vertex(-1,-1,-1),
                _Vertex(0,-phi,-1/phi),
                _Vertex(0,-phi, 1/phi),
                _Vertex(0, phi,-1/phi),
                _Vertex(0, phi, 1/phi),
                _Vertex(-phi,-1/phi,0),
                _Vertex(-phi, 1/phi,0),
                _Vertex( phi,-1/phi,0),
                _Vertex( phi, 1/phi,0),
                _Vertex(-1/phi,0,-phi),
                _Vertex( 1/phi,0,-phi),
                _Vertex(-1/phi,0, phi),
                _Vertex( 1/phi,0, phi)]

    for i in range(len(mesh.vertices)):
        mesh.vertices[i] = _vec.scale(mesh.vertices[i],radius)
        mesh.vertices[i] = _vec.add(mesh.vertices[i],_Vertex(cx,cy,cz))
    indices = [2,9,6,18,19,
               4,11,0,19,18,
               18,6,12,13,4,
               19,0,15,14,2,
               4,13,5,10,11,
               14,15,1,17,3,
               1,15,0,11,10,
               3,17,16,7,8,
               2,14,3,8,9,
               6,9,8,7,12,
               1,10,5,16,17,
               12,7,16,5,13]

    faces = []
    for i in range(0,len(indices),5):
        f = _Face([mesh.vertices[indices[i]],
                  mesh.vertices[indices[i + 1]],
                  mesh.vertices[indices[i + 2]],
                  mesh.vertices[indices[i + 3]],
                  mesh.vertices[indices[i + 4]]])
        faces.append(f)

    # make triangles
    newfaces = []
    for f in faces:
        v = _faceUtils.center(f)
        mesh.vertices.append(v)
        for i,cv in enumerate(f.vertices):
            nv = f.vertices[(i+1)%len(f.vertices)]
            newfaces.append(_Face([cv,v,nv]))

    mesh.faces = newfaces
    return mesh

def constructTetrahedron(cx,cy,cz,side):
    mesh=_Mesh()
    coord = 1/_math.sqrt(2)
    mesh.vertices = [_Vertex(+1,0,-coord),
                     _Vertex(-1,0,-coord),
                     _Vertex(0,+1,+coord),
                     _Vertex(0,-1,+coord)]

    for i in range(len(mesh.vertices)):
        mesh.vertices[i] = _vec.scale(mesh.vertices[i],side/2)
        mesh.vertices[i] = _vec.add(mesh.vertices[i],_Vertex(cx,cy,cz))

    f1 = _Face([mesh.vertices[0],mesh.vertices[1],mesh.vertices[2]])
    f2 = _Face([mesh.vertices[1],mesh.vertices[0],mesh.vertices[3]])
    f3 = _Face([mesh.vertices[2],mesh.vertices[3],mesh.vertices[0]])
    f4 = _Face([mesh.vertices[3],mesh.vertices[2],mesh.vertices[1]])

    mesh.faces = [f1,f2,f3,f4]
    return mesh
