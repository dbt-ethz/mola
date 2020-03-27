#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import math

class Vertex:
    """A Vertex defines a point in space.

    Attributes
    ----------
    x, y, z : float
        The coordinates of the `Vertex`.
    fix : boolean
        Flag to set a Vertex to be fixed or not.
    generation : integer
        Number in what generation of subdivision the face was created.
    edges : list
        List of edges connected to the `Vertex`.
    """
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.fix = False
        self.generation = 0
        self.edges = []

    def __str__(self):
        """
        Returns a string representation of the Vertex ("x.xx y.yy z.zz")
        """
        return ' '.join([str(v) for v in [self.x,self.y,self.z]])

    def __repr__(self):
        return 'Vertex('+','.join([str(v) for v in [self.x,self.y,self.z]])+')'

    def __eq__(self, other):
        """
        Compares this `Vertex` to another `Vertex`. Returns true if all their 3 coordinates are equal.
        """
        if isinstance(other, self.__class__):
            return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)
        else:
            return False

    def edge_adjacent_to_vertex(self, v):
        """
        Returns the edge connecting this `Vertex` to another `Vertex` or `None` if there's none.

        Arguments:
        ----------
        v : mola.Vertex
            The other Vertex
        """
        for edge in self.edges:
            if edge.v2 is v or edge.v1 is v:
                return edge
        return None

    def add(self, vertex):
        """
        adds the position vector of another Vertex to
        the position vector of this Vertex.
        """
        self.x += vertex.x
        self.y += vertex.y
        self.z += vertex.z
        return self

    def subtract(self, vertex):
        """
        subtracts the position vector of another Vertex from
        the position vector of this Vertex.
        """
        self.x -= vertex.x
        self.y -= vertex.y
        self.z -= vertex.z
        return self

    def scale(self, factor):
        """
        scales the position vector of this Vertex
        by a factor (multiplication).
        """
        self.x *= factor
        self.y *= factor
        self.z *= factor
        return self

    def divide(self, factor):
        """
        scales the position vector of this Vertex
        by a factor (division).
        """
        self.x /= factor
        self.y /= factor
        self.z /= factor
        return self

    def length(self):
        """
        returns the length of the position vector,
        the distance from the origin (0,0,0).
        """
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def unitize(self):
        """
        returns a vector of the same direction
        but of unit length 1
        """
        l = self.length()
        if l==0: return self
        return self.divide(l)

    def __add__(self, other):
        vector = Vertex(self.x, self.y, self.z)
        return vector.add(other)

    def __sub__(self, other):
        vector = Vertex(self.x, self.y, self.z)
        return vector.subtract(other)

    def __mul__(self, factor):
        vector = Vertex(self.x, self.y, self.z)
        return vector.scale(factor)

    # for python 3
    def __truediv__(self, factor):
        vector = Vertex(self.x, self.y, self.z)
        return vector.divide(factor)

    # for python 2
    def __div__(self, factor):
        vector = Vertex(self.x, self.y, self.z)
        return vector.divide(factor)
