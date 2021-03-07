#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import rhinoscriptsyntax as rs

def mesh_from_rhino_mesh(obj):
    mesh=Mesh()
    vertices = rs.MeshVertices(obj)
    for v in vertices:
        mesh.vertices.append(Vertex(v[0],v[1],v[2]))
    faceVerts = rs.MeshFaceVertices(obj)
    for face in faceVerts:
        if face[2]==face[3]:
            mesh.faces.append(Face(mesh.vertices[face[0]],mesh.vertices[face[1]],mesh.vertices[face[2]]))
        else:
            mesh.faces.append(Face(mesh.vertices[face[0]],mesh.vertices[face[1]],mesh.vertices[face[2]],mesh.vertices[face[3]]))
    return mesh

def display_mesh(mesh):
    display_faces(mesh.faces)

#todo: method to turn rhino mesh into molamesh

def display_faces(faces):
    vertices = []
    vertexColors = []
    facesIndices = []

    for f in faces:
        faceIndices = []
        # add vertices
        for v in f.vertices:
            faceIndices.append(len(vertices))
            vertices.append((v.x,v.y,v.z))
            vertexColors.append((f.color[0]*255,f.color[1]*255,f.color[2]*255))
            
        p = len(f.vertices)
        if p <= 4:
            # add one face if it is tri or quad
            facesIndices.append(faceIndices)
  
        else:
            # add multiple faces if it is ngon  
            points = [(v.x, v.y, v.z) for v in f.vertices]
            center_pt = centroid_points(points)
            c_index = len(vertices)
            vertices.append(center_pt)
            vertexColors.append((f.color[0]*255,f.color[1]*255,f.color[2]*255))

            faces = [[a, b, c_index] for a, b in pairwise(faceIndices + faceIndices[0:1])]
            facesIndices.extend(faces)

    a = rs.AddMesh(vertices,facesIndices,None,None,vertexColors)

    return a


def centroid_points(points):
    p = len(points)
    x, y, z = zip(*points)

    return [sum(x) / p, sum(y) / p, sum(z) / p]


def pairwise(iterable):
    a = iterable[:-1]
    b = iterable[1:]

    return zip(a, b)
