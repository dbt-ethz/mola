#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

from mola.core_mesh import Mesh
from mola.core_vertex import Vertex
from mola.core_face import Face
from mola import utils_vertex
import math

def construct_single_face(vertices):
    """
    Creates and returns a single face mesh from the vertices.

    Arguments:
    ----------
    vertices : list of mola.core.Vertex
        The vertices describing the face
    """
    mesh = Mesh()
    mesh.vertices = vertices
    mesh.faces = [Face(vertices)]
    mesh.update_topology()
    return mesh

def construct_cone(z1, z2, radius1, radius2, nSegments, capBottom=True, capTop=True):
    """
    Creates and returns a conic cylinder.
    """
    delaAngle = math.radians(360.0 / nSegments)
    angle = 0
    verticesBottom = []
    verticesTop = []
    for i in range(nSegments):
        x1 = radius1 * math.cos(angle)
        y1 = radius1 * math.sin(angle)
        verticesBottom.append(Vertex(x1, y1, z1))
        x2 = radius2 * math.cos(angle)
        y2 = radius2 * math.sin(angle)
        verticesTop.append(Vertex(x2, y2, z2))
        angle += delaAngle

    mesh = Mesh()
    mesh.vertices.extend(verticesBottom)
    mesh.vertices.extend(verticesTop)
    for i in range(nSegments):
        i2 = (i + 1) % nSegments
        mesh.faces.append(Face([verticesBottom[i],verticesBottom[i2],verticesTop[i2],verticesTop[i]]))
    if capBottom:
        # centerBottom = Vertex(0, 0, z1)
        # mesh.vertices.append(centerBottom)
        # for i in range(nSegments):
        #     i2=(i+1)%nSegments
        #     mesh.faces.append(Face([verticesBottom[i2],verticesBottom[i],centerBottom]))
        mesh.faces.append(Face(list(reversed(verticesBottom))))
    if capTop:
        # centerTop=Vertex(0,0,z2)
        # mesh.vertices.append(centerTop)
        # for i in range(nSegments):
        #     i2=(i+1)%nSegments
        #     mesh.faces.append(Face([verticesTop[i],verticesTop[i2],centerTop]))
        mesh.faces.append(Face(verticesTop))
    mesh.update_topology()
    return mesh

def construct_box(x1,y1,z1,x2,y2,z2):
    """
    Creates and returns a mesh box with six quad faces.

    Arguments:
    ----------
    x1,y1,z1 : float
        The coordinates of the bottom left front corner
    x2,y2,z2 : float
        The coordinates of the top right back corner
    """
    mesh = Mesh()
    v1 = Vertex(x1, y1, z1)
    v2 = Vertex(x1, y2, z1)
    v3 = Vertex(x2, y2, z1)
    v4 = Vertex(x2, y1, z1)
    v5 = Vertex(x1, y1, z2)
    v6 = Vertex(x1, y2, z2)
    v7 = Vertex(x2, y2, z2)
    v8 = Vertex(x2, y1, z2)
    mesh.vertices = [v1, v2, v3, v4, v5, v6, v7, v8]
    f1 = Face([v1, v2, v3, v4])
    f2 = Face([v8, v7, v6, v5])
    f3 = Face([v4, v3, v7, v8])
    f4 = Face([v3, v2, v6, v7])
    f5 = Face([v2, v1, v5, v6])
    f6 = Face([v1, v4, v8, v5])
    mesh.faces = [f1, f2, f3, f4, f5, f6]
    mesh.update_topology()
    return mesh

def construct_icosahedron(radius=1,cx=0,cy=0,cz=0):
    """
    Creates and returns a mesh in the form of an icosahedron.

    Optional Arguments:
    ----------
    radius : float
        The radius of the containing sphere.
    cx,cy,cz : float
        The coordinates of the center point.
    """
    mesh = Mesh()
    phi = (1 + 5 ** 0.5) / 2
    coordA = 1 / (2 * math.sin(2 * math.pi / 5))
    coordB = phi / (2 * math.sin(2 * math.pi / 5))
    mesh.vertices = [Vertex(0, -coordA, coordB),
                Vertex(coordB, 0, coordA),
                Vertex(coordB, 0, -coordA),
                Vertex(-coordB, 0, -coordA),
                Vertex(-coordB, 0, coordA),
                Vertex(-coordA, coordB, 0),
                Vertex(coordA, coordB, 0),
                Vertex(coordA, -coordB, 0),
                Vertex(-coordA, -coordB, 0),
                Vertex(0, -coordA, -coordB),
                Vertex(0, coordA, -coordB),
                Vertex(0, coordA, coordB)]

    for i in range(len(mesh.vertices)):
        mesh.vertices[i] = utils_vertex.vertex_scale(mesh.vertices[i], radius)
        mesh.vertices[i] = utils_vertex.vertex_add(mesh.vertices[i], Vertex(cx,cy,cz))

    indices = [1, 2, 6, 1, 7, 2, 3, 4, 5, 4, 3, 8, 6, 5, 11, 5, 6, 10, 9, 10, 2, 10, 9, 3, 7, 8, 9, 8, 7, 0, 11, 0, 1, 0, 11, 4, 6, 2, 10, 1, 6, 11, 3, 5, 10, 5, 4, 11, 2, 7, 9, 7, 1, 0, 3, 9, 8, 4, 8, 0]
    faces = []

    for i in range(0,len(indices),3):
        f = Face([mesh.vertices[indices[i]], mesh.vertices[indices[i + 1]], mesh.vertices[indices[i + 2]]])
        faces.append(f)
    mesh.faces = faces
    mesh.update_topology()
    return mesh

def construct_dodecahedron(radius=1, cx=0,cy=0,cz=0):
    """
    Constructs a dodecaheron mesh.

    Optional Arguments:
    ----------
    radius : float
        The radius of the containing sphere
    cx,cy,cz : float
        The coordinates of the center point.
    """
    mesh = Mesh()
    phi = (1 + 5 ** 0.5) / 2
    mesh.vertices = [Vertex( 1, 1, 1),
                Vertex( 1, 1,-1),
                Vertex( 1,-1, 1),
                Vertex( 1,-1,-1),
                Vertex(-1, 1, 1),
                Vertex(-1, 1,-1),
                Vertex(-1,-1, 1),
                Vertex(-1,-1,-1),
                Vertex(0,-phi,-1/phi),
                Vertex(0,-phi, 1/phi),
                Vertex(0, phi,-1/phi),
                Vertex(0, phi, 1/phi),
                Vertex(-phi,-1/phi,0),
                Vertex(-phi, 1/phi,0),
                Vertex( phi,-1/phi,0),
                Vertex( phi, 1/phi,0),
                Vertex(-1/phi,0,-phi),
                Vertex( 1/phi,0,-phi),
                Vertex(-1/phi,0, phi),
                Vertex( 1/phi,0, phi)]

    for i in range(len(mesh.vertices)):
        mesh.vertices[i] = utils_vertex.vertex_scale(mesh.vertices[i], radius)
        mesh.vertices[i] = utils_vertex.vertex_add(mesh.vertices[i], Vertex(cx,cy,cz))
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

    for i in range(0, len(indices), 5):
        f = Face([mesh.vertices[indices[i]],
                  mesh.vertices[indices[i + 1]],
                  mesh.vertices[indices[i + 2]],
                  mesh.vertices[indices[i + 3]],
                  mesh.vertices[indices[i + 4]]])
        mesh.faces.append(f)
    mesh.update_topology()
    return mesh

def construct_tetrahedron(size=1,cx=0,cy=0,cz=0):
    """
    Constructs a tetrahedron mesh.

    Optional Arguments:
    ----------
    side : float
        The edge length of the tetrahedron
    cx,cy,cz : float
        The coordinates of the center point.
    """

    mesh = Mesh()
    coord = 1 / math.sqrt(2)
    mesh.vertices = [Vertex(+1, 0, -coord),
                     Vertex(-1, 0, -coord),
                     Vertex(0, +1, +coord),
                     Vertex(0, -1, +coord)]

    for i in range(len(mesh.vertices)):
        mesh.vertices[i] = utils_vertex.vertex_scale(mesh.vertices[i], size / 2)
        mesh.vertices[i] = utils_vertex.vertex_add(mesh.vertices[i], Vertex(cx, cy, cz))

    f1 = Face([mesh.vertices[0], mesh.vertices[1], mesh.vertices[2]])
    f2 = Face([mesh.vertices[1], mesh.vertices[0], mesh.vertices[3]])
    f3 = Face([mesh.vertices[2], mesh.vertices[3], mesh.vertices[0]])
    f4 = Face([mesh.vertices[3], mesh.vertices[2], mesh.vertices[1]])

    mesh.faces = [f1, f2, f3, f4]
    mesh.update_topology()
    return mesh

def construct_torus(ringRadius, tubeRadius, ringN = 16, tubeN = 16):
    """
    Constructs a torus mesh.

    Arguments:
    ----------
    ringRadius : float
        the big radius of the axis
    tubeRadius : float
        radius of the the tube along the axis

    Optional Arguments:
    ----------
    ringN : int
        resolution along the ring
    tubeN : int
        resolution along the tube
    """
    mesh = Mesh()
    theta = 2 * math.pi / ringN
    phi = 2 * math.pi / tubeN

    for i in range (ringN):
        for j in range (tubeN):
            mesh.vertices.append(_torus_vertex(ringRadius, tubeRadius, phi * j, theta * i))

    for i in range(ringN):
        ii = (i + 1) % ringN
        for j in range(tubeN):
            jj = (j + 1) % tubeN
            a = i  * tubeN + j
            b = ii * tubeN + j
            c = ii * tubeN + jj
            d = i  * tubeN + jj
            f = Face([mesh.vertices[k] for k in [a, b, c, d]])
            mesh.faces.append(f)
    mesh.update_topology()
    return mesh

def _torus_vertex(ringRadius, tubeRadius, ph,th):
    x = math.cos(th) * (ringRadius + tubeRadius * math.cos(ph))
    y = math.sin(th) * (ringRadius + tubeRadius * math.cos(ph))
    z = tubeRadius * math.sin(ph)
    return Vertex(x, y, z)

def construct_rhombic_dodecahedron(edge_length=1, cx=0, cy=0, cz=0):
    mesh = Mesh()
    #make vertices
    mesh.vertices = [Vertex(0,  0, 2 * edge_length),
                     Vertex(-edge_length, edge_length, edge_length),
                     Vertex(-edge_length, -edge_length, edge_length),
                     Vertex(edge_length, -edge_length, edge_length),
                     Vertex(edge_length, edge_length, edge_length),
                     Vertex(-2 * edge_length, 0, 0),
                     Vertex(0, -2*edge_length, 0),
                     Vertex(2 * edge_length, 0, 0),
                     Vertex(0, 2 * edge_length, 0),
                     Vertex(-edge_length, edge_length, -edge_length),
                     Vertex(-edge_length, -edge_length, -edge_length),
                     Vertex(edge_length, -edge_length, -edge_length),
                     Vertex(edge_length, edge_length, -edge_length),
                     Vertex(0, 0, -2 * edge_length)]

    #move center to desired coordinates
    center = Vertex(cx, cy, cz)
    for v in mesh.vertices:
        v.add(center)

    #construct quad faces
    f1 = Face([mesh.vertices[0],mesh.vertices[2],mesh.vertices[5],mesh.vertices[1]])
    f2 = Face([mesh.vertices[0],mesh.vertices[3],mesh.vertices[6],mesh.vertices[2]])
    f3 = Face([mesh.vertices[0],mesh.vertices[4],mesh.vertices[7],mesh.vertices[3]])
    f4 = Face([mesh.vertices[0],mesh.vertices[1],mesh.vertices[8],mesh.vertices[4]])
    f5 = Face([mesh.vertices[2],mesh.vertices[6],mesh.vertices[10],mesh.vertices[5]])
    f6 = Face([mesh.vertices[3],mesh.vertices[7],mesh.vertices[11],mesh.vertices[6]])
    f7 = Face([mesh.vertices[4],mesh.vertices[8],mesh.vertices[12],mesh.vertices[7]])
    f8 = Face([mesh.vertices[1],mesh.vertices[5],mesh.vertices[9],mesh.vertices[8]])
    f9 = Face([mesh.vertices[10],mesh.vertices[13],mesh.vertices[9],mesh.vertices[5]])
    f10 = Face([mesh.vertices[11],mesh.vertices[13],mesh.vertices[10],mesh.vertices[6]])
    f11 = Face([mesh.vertices[12],mesh.vertices[13],mesh.vertices[11],mesh.vertices[7]])
    f12 = Face([mesh.vertices[9],mesh.vertices[13],mesh.vertices[12],mesh.vertices[8]])

    mesh.faces = [f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12]
    mesh.update_topology()
    return mesh

def construct_octahedron(edgeLen=1, cx=0, cy=0, cz=0):
    mesh = Mesh()
    #make vertices
    mesh.vertices = [Vertex(0, 0, edgeLen/2),
                     Vertex(-edgeLen/2, 0, 0),
                     Vertex(0, -edgeLen/2, 0),
                     Vertex(edgeLen/2, 0, 0),
                     Vertex(0, edgeLen/2, 0),
                     Vertex(0, 0, -edgeLen/2)]

    #move center to desired coordinates
    center = Vertex(cx, cy, cz)
    for v in mesh.vertices:
        v.add(center)

    #construct triangular faces
    f1 = Face([mesh.vertices[0], mesh.vertices[1], mesh.vertices[2]])
    f2 = Face([mesh.vertices[0], mesh.vertices[2], mesh.vertices[3]])
    f3 = Face([mesh.vertices[0], mesh.vertices[3], mesh.vertices[4]])
    f4 = Face([mesh.vertices[0], mesh.vertices[4], mesh.vertices[1]])
    f5 = Face([mesh.vertices[5], mesh.vertices[2], mesh.vertices[1]])
    f6 = Face([mesh.vertices[5], mesh.vertices[3], mesh.vertices[2]])
    f7 = Face([mesh.vertices[5], mesh.vertices[4], mesh.vertices[3]])
    f8 = Face([mesh.vertices[5], mesh.vertices[1], mesh.vertices[4]])

    mesh.faces = [f1,f2,f3,f4,f5,f6,f7,f8]
    mesh.update_topology()
    return mesh