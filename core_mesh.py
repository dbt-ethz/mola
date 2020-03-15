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
from mola.core_box import Box
from mola import utils_face

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
        """
        scales a mesh by adding multiplying
        the position of its vertices by sx, sy and sz.
        """
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
        box = Box()
        for f in self.faces:
            for v in f.vertices:
                box.add_point(v.x,v.y,v.z)
        return box

    def center(self):
        """
        Returns the center of the Mesh as a Vertex() object
        Note: not the center of gravity, just the average of its vertices.
        """
        return self.bounding_box().center()

    def edge_adjacent_to_vertices(self, v1, v2):
        for edge in v1.edges:
            if edge.v2 == v2 or edge.v1 == v2:
                return edge
        return None

    def face_adjacent_to_vertices(self, v1, v2):
        edge = v1.edge_adjacent_to_vertex(v2)
        if edge != None:
            if edge.v1 == v1:
                return edge.face1
            else:
                return edge.face2
        return None

    def add_vertex(self, x, y, z=0):
        v = Vertex(x,y,z)
        self.vertices.append(v)
        return v

    def add_face(self, vertices):
        f = Face(vertices)
        self.faces.append(f)
        return f

    def face_properties(self,face_analyse):
        values=[]
        for face in self.faces:
            values.append(face_analyse(face))
        return values

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
        self.vertices = [v for v in weldedVertices.values()]

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

    def copy(self):
        meshcopy = Mesh()

        # if mesh has no topolgy constructed
        if len(self.edges) == 0:
            for f in self.faces:
                vs = [Vertex(v.x,v.y,v.z) for v in f.vertices]
                for nv,ov in zip(vs, f.vertices):
                    nv.fix = ov.fix
                    nv.generation = ov.generation
                nf = meshcopy.add_face(vs)
                utils_face.face_copy_properties(f,nf)
        else:
            meshcopy.vertices = [Vertex(v.x,v.y,v.z) for v in self.vertices]
            for nv,ov in zip(meshcopy.vertices, self.vertices):
                nv.fix = ov.fix
                nv.generation = ov.generation

            for f in self.faces:
                vs = [meshcopy.vertices[self.vertices.index(v)] for v in f.vertices]
                nf = meshcopy.add_face(vs)
                utils_face.face_copy_properties(f,nf)
            
            for e in self.edges:
                iv1 = self.vertices.index(e.v1)
                iv2 = self.vertices.index(e.v1)
                ie1 = self.faces.index(e.face1)
                ie2 = self.faces.index(e.face2)
                v1c = meshcopy.vertices[iv1]
                v2c = meshcopy.vertices[iv2]
                edge = Edge(v1c,v2c)
                v1c.edges.append(edge)
                v2c.edges.append(edge)
                meshcopy.edges.append(edge)
                edge.face1 = meshcopy.faces[ie1]
                edge.face2 = meshcopy.faces[ie2]

        return meshcopy
