import math as _math

class VoxelSpace:
  def __init__(self, nX,nY,nZ):
    self.nX = nX
    self.nY = nY
    self.nZ = nZ
    
    self.values = []
    
  def setValuesWaves(self, freqX, freqY, freqZ):
    self.values = []
    for i in range (self.nX):
      for j in range(self.nY):
        for k in range(self.nZ):
          val0 = _math.sin((i/float(self.nX)) * freqX)
          val1 = _math.sin((j/float(self.nY)) * freqY)
          val2 = _math.sin((k/float(self.nZ)) * freqZ)
          
          v = (val0+val1+val2)/3.0
          self.values.append(v)
    
  def setValueToBorders(self, value):
    for i in range (self.nX):
      for j in range(self.nY):
        for k in range(self.nZ):
          if(i==0 or i==self.nX-1):
            self.values[self.getIndex(i,j,k)] = value
          if(j==0 or j==self.nY-1):
            self.values[self.getIndex(i,j,k)] = value
          if(k==0 or k==self.nZ-1):
            self.values[self.getIndex(i,j,k)] = value
            
  def getIndex(self, x,y,z):
    return x * (self.nY * self.nZ) + y * self.nZ + z; 
