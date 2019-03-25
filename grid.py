#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import math
from mola.core import Mesh as Mesh
from mola.core import Vertex as Vertex
from mola.core import Face as Face

class GridManager:
    def __init__(self,nX,nY,nZ=1):
        self.nX=nX
        self.nY=nY
        self.nZ=nZ
        self.length=nX*nY*nZ
        self.nYZ=nY*nZ

    def getIndex(self,x,y,z=0):
        return x * self.nYZ + y * self.nZ + z

    def getX(self,index):
        return index // self.nYZ

    def getY(self,index):
        return (index // self.nZ) % self.nY

    def getZ(self,index):
        return index % self.nZ

    def getNbs2DHex(self,index,continuous=False):
        nbs=[]
        x=self.getX(index)
        y=self.getY(index)
        if not continuous:
            if x<self.nX-1:
                nbs.append(self.getIndex(x+1,y))
            if x>0:
                nbs.append(self.getIndex(x-1,y))
            if y>0:
                nbs.append(self.getIndex(x,y-1))
            if y<self.nY-1:
                nbs.append(self.getIndex(x,y+1))
            if y%2==0:
                if x<self.nX-1 and y<self.nY-1:
                    nbs.append(self.getIndex(x+1,y+1))
                if x<self.nX-1 and y>0:
                    nbs.append(self.getIndex(x+1,y-1))
            else:
                if x>0 and y<self.nY-1:
                    nbs.append(self.getIndex(x-1,y+1))
                if x>0 and y>0:
                    nbs.append(self.getIndex(x-1,y-1))
        else:
            xNext= x+1 if x<self.nX-1 else 0
            xPrev= x-1 if x>0 else self.nX-1
            yNext= y+1 if y<self.nY-1 else 0
            yPrev= y-1 if y>0 else self.nY-1
            nbs.append(self.getIndex(xNext,y))
            nbs.append(self.getIndex(xPrev,y))
            nbs.append(self.getIndex(x,yPrev))
            nbs.append(self.getIndex(x,yNext))
            if y%2==0:
                nbs.append(self.getIndex(xNext,yNext))
                nbs.append(self.getIndex(xNext,yPrev))
            else:
                nbs.append(self.getIndex(xPrev,yNext))
                nbs.append(self.getIndex(xPrev,yPrev))
        return nbs

    def getNbs2D(self,index,nbs8=False,continuous=False):
        nbs=[]
        x=self.getX(index)
        y=self.getY(index)
        if not continuous:
            if x<self.nX-1: nbs.append(self.getIndex(x+1,y))
            if nbs8:
                if x<self.nX-1 and y<self.nY-1:
                    nbs.append(self.getIndex(x+1,y+1))
            if y<self.nY-1:
                nbs.append(self.getIndex(x,y+1))
            if nbs8:
                if x>0 and y<self.nY-1:
                    nbs.append(self.getIndex(x-1,y+1))
            if x>0:
                nbs.append(self.getIndex(x-1,y))
            if nbs8:
                if x>0 and y>0:
                    nbs.append(self.getIndex(x-1,y-1))
            if y>0:
                nbs.append(self.getIndex(x,y-1))
            if nbs8:
                if x<self.nX-1 and y>0:
                    nbs.append(self.getIndex(x+1,y-1))
        else:
            xPrev=x-1 if x>0 else self.nX-1
            xNext=x+1 if x<self.nX-1 else 0
            yPrev=y-1 if y>0 else self.nY-1
            yNext=y+1 if y<self.nY-1 else 0
            nbs.append(self.getIndex(xNext,y))
            if nbs8:
                nbs.append(self.getIndex(xNext,yNext))
            nbs.append(self.getIndex(x,yNext))
            if nbs8:
                nbs.append(self.getIndex(xPrev,yNext))
            nbs.append(self.getIndex(xPrev,y))
            if nbs8:
                nbs.append(self.getIndex(xPrev,yPrev))
            nbs.append(self.getIndex(x,yPrev))
            if nbs8:
                nbs.append(self.getIndex(xNext,yPrev))
        return nbs

    def getNbs3D(self,index,mode=3,continuous=False):
        nbs = []
        x=self.getX(index)
        y=self.getY(index)
        z=self.getZ(index)

        # mode: neighbourhood type
        # 1 :  6 nbs, shared face
        # 2 : 18 nbs, shared face or edge
        # 3 : 26 nbs, shared face, edge or vertex
        if not mode:
            mode==3
        if mode<1:
            mode==1
        if mode>3:
            mode==3

        # precalculate distances
        dists = [1, math.sqrt(2), math.sqrt(3)]

        # create a list of directions with x,y and z offsets
        directions = []
        for i in range(-1,2):
            for j in range(-1,2):
                for k in range(-1,2):
                    l = [i,j,k]
                    s = sum([abs(v) for v in l])
                    # check for neighbourhood type
                    if s>0 and s<=mode:
                        l.append(s-1)
                        directions.append(l)

        for d in directions:
            ex = x+d[0]
            ey = y+d[1]
            ez = z+d[2]
            if continuous:
                ex = ex%self.nX
                ey = ey%self.nY
                ez = ez%self.nZ
            if 0<=ex<self.nX and 0<=ey<self.nY and 0<=ez<self.nZ:
                nbs.append(self.getIndex(ex,ey,ez))

        return nbs

class Grid(GridManager):
    def __init__(self,nX,nY,nZ=1,values=None):
        self.nX=nX
        self.nY=nY
        self.nZ=nZ
        self.nYZ=nY*nZ
        if values is None:
            self.values=[0]*nX*nY*nZ
        else:
            self.values = values

    def set(self,value,x,y,z=0):
        self.values[self.getIndex(x,y,z)]=value

    def get(self,x,y,z=0):
        return self.values[self.getIndex(x,y,z)]

    def set_i(self,value,index):
        self.values[index] = value

    def get_i(self,index):
        return self.values[index]

    def getQuadMesh(self,functionIn,functionOut):
        faces=[]
        for x in range(self.nX):
            for y in range(self.nY):
                for z in range(self.nZ):
                    index=self.getIndex(x,y,z)
                    if functionIn(self.values[index]):
                        # (x,y) (x1,y) (x1,y1) (x,y1)
                        if x==self.nX-1 or functionOut(self.get(x+1,y,z)):
                            v1=Vertex(x+1,y,z)
                            v2=Vertex(x+1,y+1,z)
                            v3=Vertex(x+1,y+1,z+1)
                            v4=Vertex(x+1,y,z+1)
                            faces.append(Face([v1,v2,v3,v4]))
                        if x==0 or functionOut(self.get(x-1,y,z)):
                            v1=Vertex(x,y+1,z)
                            v2=Vertex(x,y,z)
                            v3=Vertex(x,y,z+1)
                            v4=Vertex(x,y+1,z+1)
                            faces.append(Face([v1,v2,v3,v4]))
                        if y==self.nY-1 or functionOut(self.get(x,y+1,z)):
                            v1=Vertex(x+1,y+1,z)
                            v2=Vertex(x,y+1,z)
                            v3=Vertex(x,y+1,z+1)
                            v4=Vertex(x+1,y+1,z+1)
                            faces.append(Face([v1,v2,v3,v4]))
                        if y==0 or functionOut(self.get(x,y-1,z)):
                            v1=Vertex(x,y,z)
                            v2=Vertex(x+1,y,z)
                            v3=Vertex(x+1,y,z+1)
                            v4=Vertex(x,y,z+1)
                            faces.append(Face([v1,v2,v3,v4]))
                        if z==self.nZ-1 or functionOut(self.get(x,y,z+1)):
                            v1=Vertex(x,y,z+1)
                            v2=Vertex(x+1,y,z+1)
                            v3=Vertex(x+1,y+1,z+1)
                            v4=Vertex(x,y+1,z+1)
                            faces.append(Face([v1,v2,v3,v4]))
                        if z==0 or functionOut(self.get(x,y,z-1)):
                            v1=Vertex(x,y+1,z)
                            v2=Vertex(x+1,y+1,z)
                            v3=Vertex(x+1,y,z)
                            v4=Vertex(x,y,z)
                            faces.append(Face([v1,v2,v3,v4]))
        mesh=Mesh()
        mesh.faces=faces
        return mesh

class HexGrid(Grid):
    def __init__(self,nX,nY,nZ=1,values=None):
        self.nX=nX
        self.nY=nY
        self.nZ=nZ
        self.nYZ=nY*nZ
        if values==None:
            self.values=[0]*nX*nY*nZ
        self.dimY=math.sqrt(3)*0.5

    def getPosition(self,x,y,z=0):
        return [x+(y%2)*0.5, y*self.dimY,z]
