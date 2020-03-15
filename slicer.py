from __future__ import division

#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

from mola.core_vertex import Vertex
from mola.core_edge import Edge

def slice(mesh,z):
    edges=[]
    for face in mesh.faces:
        if len(face.vertices)==4:
            edge=sliceTriangle((face.vertices[0],face.vertices[1],face.vertices[2]),z)
            if edge!=None:
                edges.append(edge)
            edge=sliceTriangle((face.vertices[2],face.vertices[3],face.vertices[0]),z)
            if edge!=None:
                edges.append(edge)
        if len(face.vertices)==3:
            edge=sliceTriangle(face.vertices,z)
            if edge!=None:
                edges.append(edge)
    return edges

def sliceWithZ(v1,v2,z):
    if v1.z==z: return Vertex(v1.x,v1.y,z)
    if v1.z<=z and v2.z<=z:
        return None
    if v1.z>=z and v2.z>=z:
        return None
    dX=v2.x-v1.x
    dY=v2.y-v1.y
    dZ=v2.z-v1.z
    if dZ==0:return None
    f=(z-v1.z)/dZ
    return Vertex(f*dX+v1.x,f*dY+v1.y,z)

def sliceTriangle(_vertices,z):
    intersections=[]
    vPrev=_vertices[-1]
    for v in _vertices:
        intersection=sliceWithZ(vPrev,v,z)
        if intersection!=None:
            intersections.append(intersection)
        vPrev=v
    if len(intersections)==2:
        dX=intersections[0].x-intersections[1].x
        dY=intersections[0].y-intersections[1].y
        if dX!=0 or dY!=0:
            return Edge(intersections[0],intersections[1])
    return None

def weldVertices(edges):
    dictVertices={}
    for edge in edges:
        tuple=(edge.v1.x,edge.v1.y)
        if tuple in dictVertices:
            edge.v1=dictVertices[tuple]
        else:
            dictVertices[tuple]=edge.v1
        edge.v1.edges.append(edge)

        tuple=(edge.v2.x,edge.v2.y)
        if tuple in dictVertices:
            edge.v2=dictVertices[tuple]
        else:
            dictVertices[tuple]=edge.v2
        edge.v2.edges.append(edge)
#
# def edgesToRing(edges):
#     # can be multiple rings
#     rings=[]
#     edgesToCheck=set(edges)
#
#     # find segments between vertices with not 2 edges
#     for e in edges:
#         if len(e.v1.edges)!=2:
#             ring=[]
#             rings.append(ring)
#             nextE=e
#             while len(nextE.v2.edges)==2:
#                 ring.append(nextE.v1)
#                 edgesToCheck.remove(nextE)
#                 for nE in nextE.v2.edges:
#                     if nE!=nextE:
#                         nextE=nE
#                         break
#             ring.append(nextE.v2)
#
#     # find closed rings
#     while len(edgesToCheck)>0:
#         nextE=edgesToCheck.pop()
#         startE=nextE
#         ring=[]
#         rings.append(ring)
#         while True:
#             ring.append(nextE.v1)
#             edgesToCheck.remove(nextE)
#             for nE in nextE.v2.edges:
#                 if nE!=nextE:
#                     nextE=nE
#                     break
#             if nextE==startE:
#                 ring.append(nextE.v1)
#                 break
#     return rings
