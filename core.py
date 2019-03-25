#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

class Vertex:
    def __init__(self,x=0,y=0,z=0):
        self.x=x
        self.y=y
        self.z=z
        self.fix=False
        self.generation=0
        self.edges=[]

    def __str__(self):
        return ' '.join([str(v) for v in [self.x,self.y,self.z]])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.x== other.x) and (self.y== other.y) and (self.z== other.z)
        else:
            return False

    def getEdgeAdjacentToVertex(self,v):
        for edge in self.edges:
            if edge.v2==v or edge.v1==v:
                return edge
        return None

    def add(self,vertex):
        self.x+=vertex.x
        self.y+=vertex.y
        self.z+=vertex.z
        return self

    def subtract(self,vertex):
        self.x-=vertex.x
        self.y-=vertex.y
        self.z-=vertex.z
        return self

    def scale(self,factor):
        self.x*=factor
        self.y*=factor
        self.z*=factor
        return self

    def divide(self,factor):
        self.x/=factor
        self.y/=factor
        self.z/=factor
        return self

    def length(self):
        return _math.sqrt(self.x*self.x+self.y*self.y+self.z*self.z)

    def unitize(self):
        l=length()
        if l==0: return self
        return divide(l)

class Face:
    def __init__(self,vertices=None):
        if (vertices==None):
            self.vertices=[]
        else:
            self.vertices = vertices
        self.color=(1,1,1,1)
        self.group=0

class Edge:
    def __init__(self,_v1,_v2):
        self.v1=_v1
        self.v2=_v2
        self.face1=None
        self.face2=None

    def __str__(self):
        return "from " + str(self.v1)+" to "+ str(self.v2)

    def getOtherVertex(self,vertex):
        if self.v1 is vertex:
            return self.v2
        if self.v2 is vertex:
            return self.v1
        return None

    def getCenter(self):
        return Vertex((self.v2.x+self.v1.x)/2.0,(self.v2.y+self.v1.y)/2.0,(self.v2.z+self.v1.z)/2.0)

class Box:

    def __init__(self,x1=float('inf'),y1=float('inf'),z1=float('inf'),x2=-float('inf'),y2=-float('inf'),z2=-float('inf')):
        self.x1=x1
        self.y1=y1
        self.z1=z1
        self.x2=x2
        self.y2=y2
        self.z2=z2

    def getDimX(self):
        return self.x2-self.x1

    def getDimY(self):
        return self.y2-self.y1

    def getDimZ(self):
        return self.z2-self.z1

    def getCenterX(self):
        return (self.x2+self.x1)/2

    def getCenterY(self):
        return (self.y2+self.y1)/2

    def getCenterZ(self):
        return (self.z2+self.z1)/2

    def addPoint(self,x,y,z):
        self.x1=min(x,self.x1)
        self.y1=min(y,self.y1)
        self.z1=min(z,self.z1)
        self.x2=max(x,self.x2)
        self.y2=max(y,self.y2)
        self.z2=max(z,self.z2)

class Mesh:
    def __init__(self):
        self.vertices=[]
        self.faces=[]
        self.edges=[]

    def scale(self,sx,sy,sz):
        vs=Vertex(sx,sy,sz)
        for v in self.vertices:
            v.x*=sx
            v.y*=sy
            v.z*=sz

    def translate(self,tx,ty,tz):
        vt=Vertex(tx,ty,tz)
        for v in self.vertices:
            v.add(vt)

    def getBounds(self):
        box=Box()
        for f in self.faces:
            for v in f.vertices:
                box.addPoint(v.x,v.y,v.z)
        return box

    def getEdgeAdjacentToVertices(self,v1,v2):
        for edge in v1.edges:
            if edge.v2==v2 or edge.v1==v2:
                return edge
        return None

    def getFaceAdjacentToVertices(self,vertex1,vertex2):
        edge=vertex1.getEdgeAdjacentToVertex(vertex2)
        if edge != None:
            if edge.v1==vertex1: return edge.face1
            else: return edge.face2
        return None

    def weldVertices(self):
        weldedVertices={}
        self.vertices=[]
        for f in self.faces:
            for i in range(len(f.vertices)):
                v=f.vertices[i]
                vtuple=(v.x,v.y,v.z)
                if vtuple in weldedVertices:
                    f.vertices[i]=weldedVertices[vtuple]
                else:
                    weldedVertices[vtuple]=v
        self.vertices=weldedVertices.values()

    def updateAdjacencies(self):
        self.weldVertices()
        self.edges=[]
        for v in self.vertices:
            v.edges=[]
        for f in self.faces:
            v1=f.vertices[-1]
            for v2 in f.vertices:
                edge=v1.getEdgeAdjacentToVertex(v2)
                if edge == None:
                    edge=Edge(v1,v2)
                    v1.edges.append(edge)
                    v2.edges.append(edge)
                    self.edges.append(edge)
                if edge.v1==v1:
                    edge.face1=f
                else:
                    edge.face2=f
                v1=v2
