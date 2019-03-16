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

    def getNbs2DHex(self,index,continous=False):
        nbs=[]
        x=self.getX(index)
        y=self.getY(index)
        if not continous:
            if x<self.nX-1:nbs.append(self.getIndex(x+1,y))
            if x>0:nbs.append(self.getIndex(x-1,y))
            if y>0: nbs.append(self.getIndex(x,y-1))
            if y<self.nY-1:nbs.append(self.getIndex(x,y+1))
            if y%2==0:
                if x<self.nX-1 and y<self.nY-1:nbs.append(self.getIndex(x+1,y+1))
                if x<self.nX-1 and y>0:nbs.append(self.getIndex(x+1,y-1))
            else:
                if x>0 and y<self.nY-1:nbs.append(self.getIndex(x-1,y+1))
                if x>0 and y>0:nbs.append(self.getIndex(x-1,y-1))
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

    def getNbs2D(self,index,nbs8=False,continous=False):
        nbs=[]
        x=self.getX(index)
        y=self.getY(index)
        if not continous:
            if x<self.nX-1: nbs.append(self.getIndex(x+1,y))
            if nbs8:
                if x<self.nX-1 and y<self.nY-1:nbs.append(self.getIndex(x+1,y+1))
            if y<self.nY-1: nbs.append(self.getIndex(x,y+1))
            if nbs8:
                if x>0 and y<self.nY-1:nbs.append(self.getIndex(x-1,y+1))
            if x>0:nbs.append(self.getIndex(x-1,y))
            if nbs8:
                if x>0 and y>0:nbs.append(self.getIndex(x-1,y-1))
            if y>0: nbs.append(self.getIndex(x,y-1))
            if nbs8:
                if x<self.nX-1 and y>0:nbs.append(self.getIndex(x+1,y-1))
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

class Grid(GridManager):
    def __init__(self,nX,nY,nZ=1,values=None):
        self.nX=nX
        self.nY=nY
        self.nZ=nZ
        self.nYZ=nY*nZ
        if values==None:
            self.values=[0]*nX*nY*nZ
    def set(self,value,x,y,z=0):
        self.values[self.getIndex(x,y,z)]=value
    def get(self,x,y,z=0):
        return self.values[self.getIndex(x,y,z)]

    def getQuadMesh(functionIn,functionOut):
        faces=[]
        for x in range(self.nX):
            for y in range(self.nY):
                for z in range(self.nZ):
                    index=self.getIndex(x,y,z)
                    if functionIn(values[index]):
                        if x==self.nX-1 or functionOut(get(x+1,y.z):
                            v1=Vertex(x+1,y,z)
                            v2=Vertex(x+1,y+1,z)
                            v3=Vertex(x+1,y+1,z+1)
                            v4=Vertex(x+1,y,z+1)
                            faces.append(Face([v1,v2,v3,v3]))
                        if x==0 or functionOut(get(x-1,y.z):
                            v1=Vertex(x,y,z)
                            v2=Vertex(x,y+1,z)
                            v3=Vertex(x,y+1,z+1)
                            v4=Vertex(x,y,z+1)
                            faces.append(Face([v1,v2,v3,v3]))
                        if y==self.nY-1 or functionOut(get(x,y+1,z):
                            v1=Vertex(x,y,z)
                            v2=Vertex(x+1,y,z)
                            v3=Vertex(x+1,y,z+1)
                            v4=Vertex(x,y,z+1)
                            faces.append(Face([v1,v2,v3,v3]))
                        if y==0 or functionOut(get(x,y-1,z):
                            v1=Vertex(x,y+1,z)
                            v2=Vertex(x+1,y+1,z)
                            v3=Vertex(x+1,y+1,z+1)
                            v4=Vertex(x,y+1,z+1)
                            faces.append([v1,v2,v3,v3]))
                        if z==self.nZ-1 or functionOut(get(x,y,z+1):
                            v1=Vertex(x,y,z)
                            v2=Vertex(x+1,y,z)
                            v3=Vertex(x+1,y+1,z)
                            v4=Vertex(x,y_1,z)
                            faces.append(Face([v1,v2,v3,v3]))
                        if z==0 or functionOut(get(x,y,z-1):
                            v1=Vertex(x,y,z+1)
                            v2=Vertex(x+1,y,z+1)
                            v3=Vertex(x+1,y+1,z+1)
                            v4=Vertex(x,y+1,z+1)
                            faces.append(Face([v1,v2,v3,v3]))
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
