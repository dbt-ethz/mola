#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import math
from mola.core_vertex import Vertex

class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.face1 = None
        self.face2 = None

    def __str__(self):
        return "from " + str(self.v1)+" to "+ str(self.v2)

    def center(self):
        """
        returns the midpoint on an edge as a Vertex() object
        """
        return Vertex((self.v2.x+self.v1.x)/2.0,(self.v2.y+self.v1.y)/2.0,(self.v2.z+self.v1.z)/2.0)

    def other_vertex(self,vertex):
        """
        if `vertex` is one of the end points of this edge,
        it returns the Vertex at the other end point.
        """
        if self.v1 is vertex:
            return self.v2
        if self.v2 is vertex:
            return self.v1
        return None
