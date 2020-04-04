#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

from mola.core_mesh import Mesh
from mola.core_vertex import Vertex
from mola.core_face import Face

from mola import utils_face


def mesh_smooth_laplacian(mesh, factor=0.3):
    """
    Applies Laplacian smoothing to a mesh.
    It works by moving each vertex in the direction of the average position of its neighbors.
    Note: this does not increase the face count.
    """
    smoothed = mesh.copy()
    #smoothed.update_topology()
    for i,v in enumerate(mesh.vertices):
        adjacent_vertices = [e.other_vertex(v) for e in v.edges]
        v_sum = Vertex()
        [v_sum.add(av) for av in adjacent_vertices]
        v_sum.divide(len(adjacent_vertices))
        delta = v_sum - v
        sv = smoothed.vertices[i]
        delta.scale(factor)
        sv.add(delta)
    return smoothed


def mesh_offset(mesh,offset=1,doclose=True):
    """
    Creates an offset of a mesh.
    If `doclose` is `True`, it will create quad faces
    along the naked edges of an open input mesh.
    """
    newMesh=Mesh()
    # calculate vertex normals
    for vertex in mesh.vertices:
        vertex.vertex = Vertex(0,0,0)
        vertex.nfaces = 0
    for face in mesh.faces:
        normal = utils_face.face_normal(face)
        for vertex in face.vertices:
            vertex.vertex.add(normal)
            vertex.nfaces += 1
    for vertex in mesh.vertices:
        vertex.vertex.scale(offset / vertex.nfaces)
        vertex.vertex.add(vertex)
    # create faces
    for face in mesh.faces:
        offsetVertices = []
        for vertex in face.vertices:
            offsetVertices.append(vertex.vertex)
        offsetVertices.reverse()
        newFace = Face(offsetVertices)
        newMesh.faces.append(newFace)
        newMesh.faces.append(face)
    # create sides
    if doclose:
        for edge in mesh.edges:
            if edge.face1 == None or edge.face2 == None:
                offsetVertices = [edge.v1, edge.v2, edge.v2.vertex, edge.v1.vertex]
                if edge.face2 == None:
                    offsetVertices.reverse()
                newFace = Face(offsetVertices)
                newMesh.faces.append(newFace)
    newMesh.update_topology()
    return newMesh

'''
def mesh_smooth_laplacian2(mesh, factor=0.3):
    # manipulates the input mesh
    # requires an oriented mesh
    # behaviour on holes different to above version
    for v in mesh.vertices:
        v.vertex=Vertex()
        v.nNbs=0
    for face in mesh.faces:
        nVertices=len(face.vertices)
        for i,cv in enumerate(face.vertices):
            cv.vertex.add(face.vertices[i-1])
            cv.nNbs+=1
            # optional
            # cv.vertex.add(face.vertices[(i+1)%nVertices])
            # cv.nNbs+=1
    for v in mesh.vertices:
        v.vertex.divide(v.nNbs)
        v.vertex.subtract(v).scale(factor)
        v.add(v.vertex)
'''
