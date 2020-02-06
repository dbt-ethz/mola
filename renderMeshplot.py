#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2020 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

def displayMesh(mesh):
    import meshplot as mp
    vs, fs, cs = get_meshlab_arrays(mesh.faces)
    mp.plot(vs, fs, cs)

def get_meshlab_arrays(faces):
    import numpy as np
    vlist = []
    flist = []
    colors = []
    cIndex=0
    for face in faces:
        for v in face.vertices:
            vlist.append([v.x,v.y,v.z])
            colors.extend(face.color)
        flist.append([cIndex,cIndex+1,cIndex+2])
        if len(face.vertices)==4:
            flist.append([cIndex+2,cIndex+3,cIndex])
        cIndex+=len(face.vertices)
    varray = np.array(vlist)
    farray = np.array(flist)
    carray = np.array(colors)
    return varray, farray, carray
