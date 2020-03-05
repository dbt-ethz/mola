#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import math
from mola.core_vertex import Vertex
from mola.core_face import Face
from mola.core_edge import Edge

class Mesh:
    """A mesh describes a 3D surface made of Vertices connected by Faces.

    Attributes
    ----------
    vertices : list
        The list of `Vertex` objects in the mesh.
    faces : list
        The list of `Face` objects in the mesh.
    edges : list
        The list of edges in the mesh.
    """
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.edges = []

    def scale(self, sx, sy, sz):
        #vs = Vertex(sx, sy, sz)
        for v in self.vertices:
            v.x *= sx
            v.y *= sy
            v.z *= sz

    def translate(self, tx, ty, tz):
        """
        translates a mesh by adding tx,ty and tz
        to the position of the vertices.
        """
        vt = Vertex(tx, ty, tz)
        for v in self.vertices:
            v.add(vt)

    def bounding_box(self):
        """
        returns the bounding box of this mesh as a Box() object
        """
        box=Box()
        for f in self.faces:
            for v in f.vertices:
                box.add_point(v.x,v.y,v.z)
        return box

    def edge_adjacent_to_vertices(self,v1,v2):
        for edge in v1.edges:
            if edge.v2 == v2 or edge.v1 == v2:
                return edge
        return None

    def face_adjacent_to_vertices(self,vertex1,vertex2):
        edge = vertex1.edge_adjacent_to_vertex(vertex2)
        if edge != None:
            if edge.v1 == vertex1:
                return edge.face1
            else:
                return edge.face2
        return None

    def add_vertex(self,x,y,z=0):
        v=Vertex(x,y,z)
        self.vertices.append(v)
        return v

    def add_face(self,vertices):
        f=Face(vertices)
        self.faces.append(f)
        return f

    def weld_vertices(self):
        weldedVertices = {}
        self.vertices = []
        for f in self.faces:
            for i in range(len(f.vertices)):
                v = f.vertices[i]
                vtuple = (v.x, v.y, v.z)
                if vtuple in weldedVertices:
                    f.vertices[i] = weldedVertices[vtuple]
                else:
                    weldedVertices[vtuple] = v
        self.vertices = weldedVertices.values()

    def update_edges(self):
        self.edges = []
        for v in self.vertices:
            v.edges = []
        for f in self.faces:
            v1 = f.vertices[-1]
            for v2 in f.vertices:
                edge = v1.edge_adjacent_to_vertex(v2)
                if edge == None:
                    edge = Edge(v1,v2)
                    v1.edges.append(edge)
                    v2.edges.append(edge)
                    self.edges.append(edge)
                if edge.v1 == v1:
                    edge.face1 = f
                else:
                    edge.face2 = f
                v1 = v2

    def update_topology(self):
        self.weld_vertices()
        self.update_edges()