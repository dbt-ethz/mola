class Grid:
    def __init__(self,nX,nY,nZ=0):
        self.nX=nX
        self.nY=nY
        self.nZ=nZ
        self.nYZ=nY*nZ
        self.values=[0]*nX*nY*nZ
    def set(value,x,y,z=0):
        self.values[getIndex(x,y,z)]=value
    def get(x,y,z):
        return self.values[getIndex(x,y,z)]
    def getIndex( x,  y,  z):
		return x * self.nYZ + y * self.nZ + z
    def getX(index):
        return index / self.nYZ
    def getY(index):
        return (index / self.nZ) % self.nY
    def getZ(index):
        return index % self.nZ
