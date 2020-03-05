#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import bpy
import numpy as np

def display_mesh(mesh):
    # Example of creating a polygonal mesh in Python from numpy arrays
    # Note: this is Python 3.x code
    #
    # $ blender -P create_mesh.py
    #
    # See this link for more information on this part of the API:
    # https://docs.blender.org/api/blender2.8/bpy.types.Mesh.html
    #
    # Paul Melis (paul.melis@surfsara.nl), SURFsara, 24-05-2019


    # Note: we DELETE all objects in the scene and only then create the new mesh!
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()


    # For each polygon the start of its vertex indices in the vertex_index array
    loop_start = np.zeros(len(mesh.faces), dtype=np.int32)
    # Length of each polygon in number of vertices
    loop_total = np.zeros(len(mesh.faces), dtype=np.int32)

    startIndex=0
    faceIndex=0
    num_vertices=0
    for f in mesh.faces:
        loop_start[faceIndex]=startIndex
        loop_total[faceIndex]=len(f.vertices)
        faceIndex+=1
        startIndex+=len(f.vertices)
        num_vertices+=len(f.vertices)
    # Vertices and edges (straightforward)
    vertices=np.zeros(num_vertices*3,dtype=np.float32)

    vertex_index = np.zeros(num_vertices,dtype=np.int32)

    # Vertex color per vertex *per polygon loop* v from 0 to 1
    vertex_colors = np.zeros(num_vertices*3,dtype=np.float32)

    vI=0
    for f in mesh.faces:

        for v in f.vertices:
            vertex_index[vI]=vI
            coordinateIndex=vI*3
            vertices[coordinateIndex]=v.x
            vertices[coordinateIndex+1]=v.y
            vertices[coordinateIndex+2]=v.z

            vertex_colors[coordinateIndex]=f.color[0]
            vertex_colors[coordinateIndex+1]=f.color[1]
            vertex_colors[coordinateIndex+2]=f.color[2]

            vI+=1


    num_vertex_indices = vertex_index.shape[0]
    num_loops = loop_start.shape[0]



    # Create mesh object based on the arrays above
    mesh = bpy.data.meshes.new(name='created mesh')
    mesh.vertices.add(num_vertices)
    mesh.vertices.foreach_set("co", vertices)
    mesh.loops.add(num_vertex_indices)
    mesh.loops.foreach_set("vertex_index", vertex_index)
    mesh.polygons.add(num_loops)
    mesh.polygons.foreach_set("loop_start", loop_start)
    mesh.polygons.foreach_set("loop_total", loop_total)

    # Create vertex color layer and set values
    vcol_lay = mesh.vertex_colors.new()
    for i, col in enumerate(vcol_lay.data):
        col.color[0] = vertex_colors[3*i+0]
        col.color[1] = vertex_colors[3*i+1]
        col.color[2] = vertex_colors[3*i+2]
        col.color[3] = 1.0                     # Alpha?

    # We're done setting up the mesh values, update mesh object and
    # let Blender do some checks on it
    mesh.update()
    mesh.validate()

    # Create Object whose Object Data is our new mesh
    obj = bpy.data.objects.new('created object', mesh)

    # Add *Object* to the scene, not the mesh
    scene = bpy.context.scene
    scene.collection.objects.link(obj)

    # Select the new object and make it active
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
