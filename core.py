#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import math

class Vertex:
    """A vertex defines a point in space.

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

    def getEdgeAdjacentToVertex(self, v):
        """
        Returns the edge connecting this `Vertex` to another `Vertex` or `None` if there's none.

        Arguments:
        ----------
        v : mola.core.Vertex
            The other Vertex
        """
        for edge in self.edges:
            if edge.v2 is v or edge.v1 is v:
                return edge
        return None

    def add(self, vertex):
        """
        adds the position vector of another vertex to
        the position vector of this vertex.
        """
        self.x += vertex.x
        self.y += vertex.y
        self.z += vertex.z
        return self

    def subtract(self, vertex):
        """
        subtracts the position vector of another vertex from
        the position vector of this vertex.
        """
        self.x -= vertex.x
        self.y -= vertex.y
        self.z -= vertex.z
        return self

    def scale(self, factor):
        """
        scales the position vector this vertex
        by a factor (multiplication).
        """
        self.x *= factor
        self.y *= factor
        self.z *= factor
        return self

    def divide(self, factor):
        """
        scales the position vector this vertex
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

class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.face1 = None
        self.face2 = None

    def __str__(self):
        return "from " + str(self.v1)+" to "+ str(self.v2)

    def getOtherVertex(self,vertex):
        """
        if `vertex` is one of the end points of this edge,
        it returns the vertex at the other end point.
        """
        if self.v1 is vertex:
            return self.v2
        if self.v2 is vertex:
            return self.v1
        return None

    def getCenter(self):
        """
        returns the midpoint on an edge
        """
        return Vertex((self.v2.x+self.v1.x)/2.0,(self.v2.y+self.v1.y)/2.0,(self.v2.z+self.v1.z)/2.0)

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

    def getDimX(self):
        """
        Returns the Box's extent in X direction.
        """
        return self.x2 - self.x1

    def getDimY(self):
        """
        Returns the Box's extent in Y direction.
        """
        return self.y2 - self.y1

    def getDimZ(self):
        """
        Returns the Box's extent in Z direction.
        """
        return self.z2 - self.z1

    def getCenterX(self):
        """
        Returns the Box's center in X direction.
        """
        return (self.x2 + self.x1) / 2

    def getCenterY(self):
        """
        Returns the Box's center in Y direction.
        """
        return (self.y2 + self.y1) / 2

    def getCenterZ(self):
        """
        Returns the Box's center in Z direction.
        """
        return (self.z2 + self.z1) / 2

    def addPoint(self,x,y,z):
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

    def getBounds(self):
        """
        returns the bounding box of this mesh
        """
        box=Box()
        for f in self.faces:
            for v in f.vertices:
                box.addPoint(v.x,v.y,v.z)
        return box

    def getEdgeAdjacentToVertices(self,v1,v2):
        for edge in v1.edges:
            if edge.v2 == v2 or edge.v1 == v2:
                return edge
        return None

    def getFaceAdjacentToVertices(self,vertex1,vertex2):
        edge = vertex1.getEdgeAdjacentToVertex(vertex2)
        if edge != None:
            if edge.v1 == vertex1:
                return edge.face1
            else:
                return edge.face2
        return None

    def addVertex(x,y,z=0):
        v=Vertex(x,y,z)
        self.vertices.append(v)
        return v
        
    def addFace(vertices):
        f=Face(vertices)
        self.faces.append(f)
        return f

    def weldVertices(self):
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

    def updateAdjacencies(self):
        self.weldVertices()
        self.edges = []
        for v in self.vertices:
            v.edges = []
        for f in self.faces:
            v1 = f.vertices[-1]
            for v2 in f.vertices:
                edge = v1.getEdgeAdjacentToVertex(v2)
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

    def constructTopology(self):
        self.weldVertices()
        self.updateAdjacencies()
