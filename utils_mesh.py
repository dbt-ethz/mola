#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

from mola.core_mesh import Mesh
from mola.core_vertex import Vertex

def mesh_smooth_laplacian(mesh, factor=0.3):
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
