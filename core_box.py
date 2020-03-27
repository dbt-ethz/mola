#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import math
from mola.core_vertex import Vertex

class Box:
    """A `Box` is defined by by two opposite corners with x,y,z coordinates.
    Mostly used for getting the bounding box of a set of points.

    Attributes
    ----------
    x1, y1, z1 : float
        The coordinates of the bottom left front corner.
    x2, y2, z2 : float
        The coordinates of the top right back corner.
    """
    def __init__(self, x1=float('inf'), y1=float('inf'), z1=float('inf'), x2=-float('inf'), y2=-float('inf'), z2=-float('inf')):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2

    def dim_x(self):
        """
        Returns the Box's extent in X direction.
        """
        return self.x2 - self.x1

    def dim_y(self):
        """
        Returns the Box's extent in Y direction.
        """
        return self.y2 - self.y1

    def dim_z(self):
        """
        Returns the Box's extent in Z direction.
        """
        return self.z2 - self.z1

    def center(self):
        """
        returns the Box's center as a Vertex() object
        """
        return Vertex((self.x2+self.x1)/2.0,(self.y2+self.y1)/2.0,(self.z2+self.z1)/2.0)

    def add_point(self,x,y,z):
        """
        adds a point to the bounding box,
        increases the box's size if the point is outside.
        """
        self.x1 = min(x,self.x1)
        self.y1 = min(y,self.y1)
        self.z1 = min(z,self.z1)
        self.x2 = max(x,self.x2)
        self.y2 = max(y,self.y2)
        self.z2 = max(z,self.z2)
