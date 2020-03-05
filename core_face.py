#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import math
from mola import utils_vertex
from mola import utils_face

class Face:
    """A `Face` is the surface between a set of vertices.

    Attributes
    ----------
    vertices : list
        A list of `Vertex` objects defining the `Face`.
    color : tuple (r, g, b, a)
        The color of the face (0..1).
    group : integer
        The group index the `Face` belongs to.
    """

    def __init__(self, vertices=None):
        if (vertices == None):
            self.vertices = []
        else:
            self.vertices = vertices
        self.color = (1,1,1,1)
        self.group = 0

    def area(self):
        """
        Returns the area of the face.
        """
        if(len(self.vertices) == 3):
            return utils_vertex.triangle_area(self.vertices[0], self.vertices[1], self.vertices[2])
        else:
            return utils_vertex.triangle_area(self.vertices[0], self.vertices[1], self.vertices[2]) + utils_vertex.triangle_area(self.vertices[2], self.vertices[3], self.vertices[0])

    def perimeter(self):
        """
        Returns the perimeter of the face as the sum of all the edges' lengths.
        """
        sum = 0
        for i in range(len(self.vertices)):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % len(self.vertices)]
            sum += utils_vertex.vertex_distance(v1,v2)
        return sum

    def compactness(self):
        """
        Returns the compactness of the face as the ratio between area and perimeter.
        """
        return self.area() / self.perimeter()

    def angle_horizontal(self):
        """
        Returns the azimuth, the orientation of the face around the z-axis in the XY-plane
        """
        n = self.normal()
        return math.atan2(n.y, n.x)

    def angle_vertical(self):
        """
        Returns the altitude, 0 if the face is vertical, -Pi/2 if it faces downwards, +Pi/2 if it faces upwards.
        """
        n = self.normal()
        #nXY = Vertex(n.x, n.y, 0.0)
        #return vecUtils.angle(n, nXY)
        # alternative, probably less computationally intense:
        return math.asin(n.z)

    def curvature(self):
        """
        Returns the local curvature of a mesh face, by measuring the angle to the neighbour faces.
        """
        facenormal = self.normal()
        sumD = 0
        vPrev = self.vertices[-1]
        num_faces = 1
        for v in self.vertices:
            edge = v.edge_adjacent_to_vertex(vPrev)
            if edge != None:
                nbFace = edge.face1
                if edge.face1 == self:
                    nbFace = edge.face2
                if nbFace != None:
                    num_faces += 1
                    nbNormal = utils_face.face_normal(nbFace)
                    sumD += utils_vertex.vertex_distance(nbNormal,facenormal)
            vPrev = v
        return sumD / num_faces

    def center(self):
        """
        Returns the center point (type Vertex) of the face.
        Note: not the center of gravity, just the average of its vertices.
        """
        return utils_vertex.vertices_list_center(self.vertices)

    def normal(self):
        """
        Returns the normal of the face, a vector of length 1 perpendicular to the plane of the triangle.
        """
        return utils_vertex.triangle_normal(self.vertices[0], self.vertices[1], self.vertices[2])
