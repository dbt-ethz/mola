class Grid:
    def __init__(self,nX,nY,nZ=0):
        self.nX=nX
        self.nY=nY
        self.nZ=nZ
        self.nYZ=nY*nZ
        self.values=[0]*nX*nY*nZ
    def set(self,value,x,y,z=0):
        self.values[getIndex(x,y,z)]=value
    def get(self,x,y,z):
        return self.values[getIndex(x,y,z)]
    def getIndex(self, x,  y,  z):
		return x * self.nYZ + y * self.nZ + z
    def getX(self,index):
        return index / self.nYZ
    def getY(self,index):
        return (index / self.nZ) % self.nY
    def getZ(self,index):
        return index % self.nZ
