import math

def VectorAdd(v1,v2):
  return [v1.x+v2.x,v1.y+v2.y,v1.z+v2.z]

def VectorAngle(v1,v2):
  a=VectorUnitize(v1)
  b=VectorUnitize(v2)
  return math.acos(VectorDotProduct(a,b))

def VectorSubtract(v1,v2):
  return [v1.x-v2.x,v1.y-v2.y,v1.z-v2.z]

def VectorScale(v,factor):
  return [v.x*factor,v.y*factor,v.z*factor]

def VectorDivide(v,factor):
  return [v.x/factor,v.y/factor,v.z/factor]

def VectorLength(v):
  return math.sqrt(v.x*v.x+v.y*v.y+v.z*v.z)

def VectorUnitize(v):
  return VectorDivide(v,VectorLength(v))

def VectorCrossProduct(v1,v2):
  return [v1.y * v2.z - v2.y * v1.z,v1.z * v2.x - v2.z * v1.x,v1.x * v2.y - v2.x * v1.y]

def VectorDotProduct(v1,v2):
  return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z

def VectorDistance(v1,v2):
  dX=v2.x-v1.x
  dY=v2.y-v1.y
  dZ=v2.z-v1.z
  return math.sqrt(dX*dX+dY*dY+dZ*dZ)

def VectorCenter(vertices):
  # return the average of all boundarypoints
  center=[0,0,0]
  for vertex in vertices:
    center=VectorAdd(vertex,center)
  return VectorDivide(center,len(vertices))

def VectorPerimeter(vertices):
  perimeter=0
  for i in range(len(vertices)):
    n1=vertices[i]
    n2=vertices[(i+1)%len(self.nodes)]
    perimeter=perimeter+VectorDistance(n1,n2)
  return perimeter

def VectorBetweenRel( v1,  v2,  f):
  return [(v2.x - v1.x) * f + v1.x, (v2.y - v1.y) * f + v1.y, (v2.z - v1.z) * f + v1.z]

def VectorBetweenAbs( v1,  v2,  f):
  d = VectorDistance(v1,v2)
  return VectorBetweenRel(v1, v2, f / d)

def VectorLineLineIntersection(a,b,c,d):
  deltaABX=b.x - a.x
  deltaABY=b.y - a.y
  deltaDCX=d.x - c.x
  deltaDCY=d.y - c.y
  denominator = deltaABX * deltaDCY - deltaABY * deltaDCX
  if denominator == 0:
    return None
  numerator = (a.y - c.y) * deltaDCX - (a.x - c.x) * deltaDCY
  r = numerator / denominator
  x = a.x + r * deltaABX
  y = a.y + r * deltaABY
  return [x,y,0]

def VectorOffsetLine(v1, v2,  offset):
  v = VectorSubtract(v2, v1)
  v=VectorUnitize(v)
  v=VectorScale(v,offset)
  t = v.x
  v.x = -v.y
  v.y = t
  v.z=0
  return [VectorAdd(v1,v),VectorAdd(v2,v)]

def VectorOffsetPoint(v1,  v2,  v3,  offset1,  offset2):
  line1= VectorOffsetLine(v1, v2, offset1);
  line2= VectorOffsetLine(v2, v3, offset2);
  return VectorLineLineIntersection(line1.x,line1.y,line2.x,line2.y)

def VectorNormal(v1,v2,v3):
  v = VectorSubtract(v2, v1)
  u = VectorSubtract(v3, v1)
  cross=VectorCrossProduct(v,u)
  return VectorUnitize(cross)

def VectorNormalFromVertices(vertices):
  if len(vertices)==3:
    return VectorNormal(vertices[0],vertices[1],vertices[2])
  elif len(vertices)==4:
    n1 = VectorNormal(vertices[0],vertices[1],vertices[2])
    n2 = VectorNormal(vertices[2],vertices[3],vertices[0])
    angle = VectorAngle(n1,n2)
    if(angle>math.pi-0.01):
      n2 = VectorScale(n2,-1)
    sum = VectorAdd(n1,n2)
    sum = VectorScale(sum, 0.5)
    sum = VectorUnitize(sum)
    return sum
