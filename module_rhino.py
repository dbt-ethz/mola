#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import rhinoscriptsyntax as rs
from mola.core_mesh import Mesh
from mola.core_vertex import Vertex
from mola.core_face import Face

def mesh_from_rhino_mesh(obj):
    mesh=Mesh()
    vertices = rs.MeshVertices(obj)
    for v in vertices:
        mesh.vertices.append(Vertex(v[0],v[1],v[2]))
    faceVerts = rs.MeshFaceVertices(obj)
    for face in faceVerts:
        if face[2]==face[3]:
            mesh.faces.append(Face([mesh.vertices[face[0]],mesh.vertices[face[1]],mesh.vertices[face[2]]]))
        else:
            mesh.faces.append(Face([mesh.vertices[face[0]],mesh.vertices[face[1]],mesh.vertices[face[2]],mesh.vertices[face[3]]]))
    return mesh

def display_mesh(mesh):
    display_faces(mesh.faces)

#todo: method to turn rhino mesh into molamesh

def display_faces(faces):
    vertices=[]
    facesIndices=[]
    vertexColors=[]
    for f in faces:
        faceIndices=[]
        for v in f.vertices:
            faceIndices.append(len(vertices))
            vertices.append((v.x,v.y,v.z))
            vertexColors.append((f.color[0]*255,f.color[1]*255,f.color[2]*255))
        facesIndices.append(faceIndices)
    mesh = rs.AddMesh(vertices,facesIndices,None,None,vertexColors)
    
    return mesh
