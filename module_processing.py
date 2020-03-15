#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

def display_lines(lines):
    for l in lines:
        line(l.v1.x,l.v1.y,l.v2.x,l.v2.y)

def display_mesh(mesh):
    return display_faces(mesh.faces)

def create_lines_shape(lines):
    shape = createShape()
    shape.beginShape(LINES)
    for l in lines:
        shape.vertex(l.v1.x,l.v1.y,l.v1.z)
        shape.vertex(l.v2.x,l.v2.y,l.v2.z)
    shape.endShape()
    return shape

def create_mesh_shape(mesh):
    shape = createShape(GROUP)
    trishape = createShape()
    trishape.beginShape(TRIANGLES)
    quadshape = createShape()
    quadshape.beginShape(QUADS)
    for f in mesh.faces:
        cShape = trishape
        if len(f.vertices) == 4:
            cShape = quadshape
        cShape.fill(f.color[0]*255,f.color[1]*255,f.color[2]*255)
        for v in f.vertices:
            cShape.vertex(v.x,v.y,v.z)
    trishape.endShape()
    quadshape.endShape()
    shape.addChild(trishape)
    shape.addChild(quadshape)
    return shape

# split between triangles, quads and more..
def display_faces(faces):
    beginShape(QUADS)
    for f in faces:
        if len(f.vertices)==4:
            fill(f.color[0]*255,f.color[1]*255,f.color[2]*255)
            for v in f.vertices:
                vertex(v.x,v.y,v.z)
    endShape()
    beginShape(TRIANGLES)
    for f in faces:
        if len(f.vertices)==3:
            fill(f.color[0]*255,f.color[1]*255,f.color[2]*255)
            for v in f.vertices:
                vertex(v.x,v.y,v.z)
    endShape()
    for f in faces:
        if len(f.vertices)>4:
            fill(f.color[0]*255,f.color[1]*255,f.color[2]*255)
            beginShape()
            for v in f.vertices:
                vertex(v.x,v.y,v.z)
            endShape(CLOSE)

# def display(faces):
#     for f in faces:
#         fill(f.color[0]*255,f.color[1]*255,f.color[2]*255)
#         beginShape()
#         for v in f.vertices:
#             vertex(v.x,v.y,v.z)
#         endShape(CLOSE)

def display_faces_2D(faces):
    for f in faces:
        beginShape()
        for v in f.vertices:
            vertex(v.x,v.y)
        endShape(CLOSE)
