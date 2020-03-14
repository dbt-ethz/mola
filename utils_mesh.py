#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

from mola.core_mesh import Mesh
from mola.core_vertex import Vertex

def mesh_smooth_laplacian(mesh, factor=1.0):
    smoothed = mesh.copy()
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