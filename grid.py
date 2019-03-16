class GridManager:
    def __init__(self,nX,nY,nZ=0):
        self.nX=nX
        self.nY=nY
        self.nZ=nZ
        self.length=nX*nY*nZ
        self.nYZ=nY*nZ
    def getIndex(self, x,  y,  z):
		return x * self.nYZ + y * self.nZ + z
    def getX(self,index):
        return index / self.nYZ
    def getY(self,index):
        return (index / self.nZ) % self.nY
    def getZ(self,index):
        return index % self.nZ

    def getNbs2DHex(self,index,continous=False):
        nbs=[]
        x=getX(index)
        y=getY(index)
        if !continous:
            if x<nX-1:nbs.append(gm.getIndex(x+1,y))
            if x>0:nbs.append(gm.getIndex(x-1,y))
            if y>0:nbs.append(gm.getIndex(x,y-1))
            if y<nY-1:nbs.append(gm.getIndex(x,y+1))
            if y%2==0:
                if x<nX-1 and y<nY-1: nbs.append(gm.getIndex(x+1,y+1))
                if x<nX-1 and y>0: nbs.append(gm.getIndex(x+1,y-1))
            else:
                if x>0 and y<nY-1: nbs.append(gm.getIndex(x-1,y+1))
                if x>0 and y>0: nbs.append(gm.getIndex(x-1,y-1))
        else:
            xNext= x+1 if x<nX-1 else xNext=0
            xPrev= x-1 if x>0 else xPrev=nX-1
            yNext= y+1 if y<nY-1 else yNext=0
            yPrev= y-1 if y>0 else yPrev=nY-1
            nbs.append(gm.getIndex(xNext,y))
            nbs.append(gm.getIndex(xPrev,y))
            nbs.append(gm.getIndex(x,yPrev))
            nbs.append(gm.getIndex(x,yNext))
            if y%2==0:
                nbs.append(gm.getIndex(xNext,yNext))
                nbs.append(gm.getIndex(xNext,yPrev))
            else:
                nbs.append(gm.getIndex(xPrev,yNext))
                nbs.append(gm.getIndex(xPrev,yPrev))
        return nbs

    def getNbs2D(self,index,nbs8=False,continous=False):
        nbs=[]
        x=getX(index)
        y=getY(index)
        if !continous:
            if x<nX-1:nbs.append(gm.getIndex(x+1,y))
            if nbs8:
                if x<nX-1 and y<nY-1:nbs.append(gm.getIndex(x+1,y+1))
            if y<nY-1:nbs.append(gm.getIndex(x,y+1))
            if nbs8:
                if x>0 and y<nY-1: nbs.append(gm.getIndex(x-1,y+1))
            if x>0: nbs.append(gm.getIndex(x-1,y))
            if nbs8:
                if x>0 and y>0: nbs.append(gm.getIndex(x-1,y-1))
            if y>0: nbs.append(gm.getIndex(x,y-1))
            if nbs8:
                if x<nX-1 and y>0: nbs.append(gm.getIndex(x+1,y-1))
        else:
            xPrev=x-1 if x>0 else xPrev=nX-1
            xNext=x+1 if x<nX-1 else xNext=0
            yPrev=y-1 if y>0 else yPrev=nY-1
            yNext=y+1 if y<nY-1 else yNext=0
            nbs.append(gm.getIndex(xNext,y))
            if nbs8:
                nbs.append(gm.getIndex(xNext,yNext))
            nbs.append(gm.getIndex(x,yNext))
            if nbs8:
                nbs.append(gm.getIndex(xPrev,yNext))
            nbs.append(gm.getIndex(xPrev,y))
            if nbs8:
                nbs.append(gm.getIndex(xPrev,yPrev))
            nbs.append(gm.getIndex(x,yPrev))
            if nbs8:
                nbs.append(gm.getIndex(xNext,yPrev))
        return nbs

class Grid(GridManager):
    def __init__(self,nX,nY,nZ=0,values=None):
        self.nX=nX
        self.nY=nY
        self.nZ=nZ
        self.nYZ=nY*nZ
        if values==None:
            self.values=[0]*nX*nY*nZ
    def set(self,value,x,y,z=0):
        self.values[getIndex(x,y,z)]=value
    def get(self,x,y,z=0):
        return self.values[getIndex(x,y,z)]
