#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

from mola.core import *
import mola.vec as _vec
from mola.core import Mesh as _Mesh
from mola.core import Vertex as _Vertex
from mola.core import Face as _Face
import mola.faceUtils as faceUtils
import copy

def _collectNewFaces(_mesh):
    newMesh=Mesh()
    for face in _mesh.faces:
        v1=face.vertices[-2]
        v2=face.vertices[-1]
        for v3 in face.vertices:
            edge1=_mesh.getEdgeAdjacentToVertices(v1,v2)
            edge2=_mesh.getEdgeAdjacentToVertices(v2,v3)
            if (edge1 != None) and (edge2!= None):
                newFace=Face([edge1.vertex,v2.vertex,edge2.vertex,face.vertex])
                newFace.color=face.color
                newFace.group=face.group
                newMesh.faces.append(newFace)
            v1=v2
            v2=v3
    newMesh.updateAdjacencies()
    return newMesh

def subdivide(_mesh):
    for face in _mesh.faces:
        face.vertex=faceUtils.center(face)
    for edge in _mesh.edges:
        edge.vertex = edge.getCenter()
    for vertex in _mesh.vertices:
        vertex.vertex = Vertex(vertex.x,vertex.y,vertex.z)
    return _collectNewFaces(_mesh)

def subdivideCatmull(_mesh):
    for face in _mesh.faces:
        face.vertex=faceUtils.center(face)

    for edge in _mesh.edges:
        if edge.face1==None or edge.face2==None:
            edge.v1.fix=True
            edge.v2.fix=True
            edge.vertex = edge.getCenter()
        else:
            vsum=Vertex()
            nElements=2
            vsum=_vec.add(vsum,edge.v1)
            vsum=_vec.add(vsum,edge.v2)
            if edge.face1!=None:
                vsum=_vec.add(vsum,edge.face1.vertex)
                nElements+=1
            if edge.face2!=None:
                vsum=_vec.add(vsum,edge.face2.vertex)
                nElements+=1
            vsum=_vec.divide(vsum,nElements)
            edge.vertex=vsum
        if edge.v1.fix and edge.v2.fix:
            edge.vertex.fix=True

    for vertex in _mesh.vertices:
        if vertex.fix:
            vertex.vertex=copy.copy(vertex)
        else:
            averageFaces=Vertex()
            averageEdges=Vertex()
            nEdges=len(vertex.edges)

            for edge in vertex.edges:
                face=edge.face1
                if edge.v2==vertex:
                    face=edge.face2
                if face!=None:
                    averageFaces=_vec.add(averageFaces,face.vertex)
                averageEdges=_vec.add(averageEdges,edge.getCenter())
            averageEdges=_vec.scale(averageEdges,2.0/nEdges)
            averageFaces=_vec.scale(averageFaces,1.0/nEdges)

            v=Vertex(vertex.x,vertex.y,vertex.z)
            v=_vec.scale(v,nEdges-3)
            v=_vec.add(v,averageFaces)
            v=_vec.add(v,averageEdges)
            v=_vec.scale(v,1.0/nEdges)
            vertex.vertex=v

    return _collectNewFaces(_mesh)

def splitGrid(face,nU,nV):
    """
    splits a triangle, quad or a rectangle into a regular grid
    """
    if len(face.vertices)>4:
        print('too many vertices')
        return face
    if len(face.vertices)==4:
        vsU1=_getVerticesBetween(face.vertices[0],face.vertices[1],nU)
        vsU2=_getVerticesBetween(face.vertices[3],face.vertices[2],nU)
        gridVertices=[]
        for u in range(len(vsU1)):
            gridVertices.append(_getVerticesBetween(vsU1[u],vsU2[u],nV))
        faces=[]
        for u in range(len(vsU1)-1):
            vs1=gridVertices[u]
            vs2=gridVertices[u+1]
            for v in range(len(vs1)-1):
                faces.append(_Face([vs1[v],vs1[v+1],vs2[v+1],vs2[v]]))
        return faces
    if len(face.vertices)==3:
        vsU1=_getVerticesBetween(face.vertices[0],face.vertices[1],nU)
        vsU2=_getVerticesBetween(face.vertices[0],face.vertices[2],nU)
        gridVertices=[]
        for u in range(1,len(vsU1)):
            gridVertices.append(_getVerticesBetween(vsU1[u],vsU2[u],nV))
        faces=[]
        # triangles
        v0=face.vertices[0]
        vs1=gridVertices[0]
        for v in range(len(vs1)-1):
            faces.append(_Face([v0,vs1[v],vs1[v+1]]))
        for u in range(len(gridVertices)-1):
            vs1=gridVertices[u]
            vs2=gridVertices[u+1]
            for v in range(len(vs1)-1):
                faces.append(_Face([vs1[v],vs1[v+1],vs2[v+1],vs2[v]]))
        return faces

def _getVerticesBetween(v1,v2,n):
    row=[]
    deltaV=_vec.subtract(v2,v1)
    deltaV=_vec.div(deltaV,n)
    for i in range(n):
        addV=_vec.scale(deltaV,i)
        row.append(_vec.add(addV,v1))
    row.append(v2)
    return row

def splitRelFreeQuad(face, indexEdge,  split1,  split2):
    """
    Splits a quad in two new quads through the points specified
    by relative position along the edge.

    Arguments:
    ----------
    face : mola.core.Face
        The face to be extruded
    indexEdge : int
        direction of split, 0: 0->2, 1: 1->3
    split1, split2 : float
        relative position of split on each edge (0..1)
    """
    # only works with quads, therefore return original face if triangular
    if len(face.vertices) != 4:
        return face

    # constrain indexEdge to be either 0 or 1
    indexEdge = indexEdge%2

    indexEdge1=(indexEdge+1)%len(face.vertices)
    indexEdge2=(indexEdge+2)%len(face.vertices)
    indexEdge3=(indexEdge+3)%len(face.vertices)
    p1 = _vec.betweenRel(face.vertices[indexEdge], face.vertices[indexEdge1], split1)
    p2 = _vec.betweenRel(face.vertices[indexEdge2 ], face.vertices[indexEdge3], split2)
    faces=[]
    if indexEdge == 0:
        faces.append(_Face([face.vertices[0], p1, p2, face.vertices[3]]))
        faces.append(_Face([p1,face.vertices[1],face.vertices[2],p2]))
    elif indexEdge == 1:
        faces.append(_Face([face.vertices[0], face.vertices[1], p1, p2]))
        faces.append(_Face([p2, p1, face.vertices[2], face.vertices[3]]))
    return faces



def extrude(face, height=0.0, capBottom=False, capTop=True):
    """
    Extrudes the face straight by distance height.

    Arguments:
    ----------
    face : mola.core.Face
        The face to be extruded
    height : float
        The extrusion distance, default 0
    capBottom : bool
        Toggle if bottom face (original face) should be created, default False
    capTop : bool
        Toggle if top face (extrusion face) should be created, default True
    """
    normal=faceUtils.normal(face)
    normal=_vec.scale(normal,height)
    # calculate vertices
    new_vertices=[]
    for i in range(len(face.vertices)):
        new_vertices.append(_vec.add(face.vertices[i], normal))
    # faces
    new_faces=[]
    if capBottom:
        new_faces.append(face)
    for i in range(len(face.vertices)):
        i2=i+1
        if i2>=len(face.vertices):
            i2=0
        v0=face.vertices[i]
        v1=face.vertices[i2]
        v2=new_vertices[i2]
        v3=new_vertices[i]
        new_faces.append(_Face([v0,v1,v2,v3]))
    if capTop:
        new_faces.append(_Face(new_vertices))
    for new_face in new_faces:
        new_face.color=face.color
    return new_faces

def extrudeTapered(face, height=0.0, fraction=0.5,doCap=True):
    """
    Extrudes the face tapered like a window by creating an
    offset face and quads between every original edge and the
    corresponding new edge.

    Arguments:
    ----------
    face : mola.core.Face
        The face to be extruded
    height : float
        The distance of the new face to the original face, default 0
    fraction : float
        The relative offset distance, 0: original vertex, 1: center point
        default 0.5 (halfway)
    """
    center_vertex = faceUtils.center(face)
    normal = faceUtils.normal(face)
    scaled_normal = _vec.scale(normal, height)

    # calculate new vertex positions
    new_vertices = []
    for i in range(len(face.vertices)):
        n1 = face.vertices[i]
        betw = _vec.subtract(center_vertex, n1)
        betw = _vec.scale(betw, fraction)
        nn = _vec.add(n1, betw)
        nn = _vec.add(nn, scaled_normal)
        new_vertices.append(nn)

    new_faces = []
    # create the quads along the edges
    num = len(face.vertices)
    for i in range(num):
        n1 = face.vertices[i]
        n2 = face.vertices[(i+1) % num]
        n3 = new_vertices[(i+1) % num]
        n4 = new_vertices[i]
        new_face = _Face([n1,n2,n3,n4])
        new_faces.append(new_face)

    # create the closing cap face
    if doCap:
        cap_face = _Face(new_vertices)
        new_faces.append(cap_face)

    return new_faces

def splitRoof(face, height):
    """
    Extrudes a pitched roof

    Arguments:
    ----------
    face : mola.core.Face
        The face to be extruded
    height : mola.core.Vertex
        Th height of the roof
    """
    faces = []
    normal = faceUtils.normal(face)
    normal = _vec.scale(normal,height)
    if len(face.vertices)==4:
        ev1=_vec.center(face.vertices[0],face.vertices[1])
        ev1=_vec.add(ev1,normal)
        ev2=_vec.center(face.vertices[2],face.vertices[3])
        ev2=_vec.add(ev2,normal)

        faces.append(_Face([face.vertices[0],face.vertices[1],ev1]))
        faces.append(_Face([face.vertices[1],face.vertices[2],ev2,ev1]))
        faces.append(_Face([face.vertices[2],face.vertices[3],ev2]))
        faces.append(_Face([face.vertices[3],face.vertices[0],ev1,ev2]))
        return faces
    elif len(face.vertices)==3:
        ev1=_vec.center(face.vertices[0],face.vertices[1])
        ev1=_vec.add(ev1,normal)
        ev2=_vec.center(face.vertices[1],face.vertices[2])
        ev2=_vec.add(ev2,normal)

        faces.append(_Face([face.vertices[0],face.vertices[1],ev1]))
        faces.append(_Face([face.vertices[1],ev2,ev1]))
        faces.append(_Face([face.vertices[1],face.vertices[2],ev2]))
        faces.append(_Face([face.vertices[2],face.vertices[0],ev1,ev2]))
        return faces
    return [face]

def extrudeToPoint(face, point):
    """
    Extrudes the face to a point by creating a
    triangular face from each edge to the point.

    Arguments:
    ----------
    face : mola.core.Face
        The face to be extruded
    point : mola.core.Vertex
        The point to extrude to
    """
    numV = len(face.vertices)
    faces = []
    for i in range(numV):
        v1 = face.vertices[i]
        v2 = face.vertices[(i+1)%numV]
        faces.append(_Face([v1,v2,point]))
    return faces

def extrudeToPointCenter(face, height=0.0):
    """
    Extrudes the face to the center point moved by height
    normal to the face and creating a triangular face from
    each edge to the point.

    Arguments:
    ----------
    face : mola.core.Face
        The face to be extruded
    height : float
        The distance of the new point to the face center, default 0
    """
    normal = faceUtils.normal(face)
    normal = _vec.scale(normal,height)
    center = faceUtils.center(face)
    center = _vec.add(center,normal)
    return extrudeToPoint(face,center)
