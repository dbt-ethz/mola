from __future__ import division
import math as _math
from mola.core import Vertex as _Vertex

def VectorAdd(v1,v2):
    return _Vertex(v1.x+v2.x,v1.y+v2.y,v1.z+v2.z)

def add(v1,v2):
    return _Vertex(v1.x+v2.x,v1.y+v2.y,v1.z+v2.z)

def VectorAngle(v1,v2):
  a=VectorUnitize(v1)
  b=VectorUnitize(v2)
  return _math.acos(VectorDotProduct(a,b))

def angle(v1,v2):
    a=unitize(v1)
    b=unitize(v2)
    return _math.acos(dot(a,b))

def VectorSubtract(v1,v2):
    return _Vertex(v1.x-v2.x,v1.y-v2.y,v1.z-v2.z)

def subtract(v1,v2):
    return _Vertex(v1.x-v2.x,v1.y-v2.y,v1.z-v2.z)

def VectorScale(v,factor):
    return _Vertex(v.x*factor,v.y*factor,v.z*factor)
    #return [v.x*factor,v.y*factor,v.z*factor]

def scale(v,factor):
    return _Vertex(v.x*factor,v.y*factor,v.z*factor)

def VectorDivide(v,factor):
    return _Vertex(v.x/factor,v.y/factor,v.z/factor)
    #return [v.x/factor,v.y/factor,v.z/factor]

def divide(v,factor):
    return _Vertex(v.x/factor,v.y/factor,v.z/factor)
    #return [v.x/factor,v.y/factor,v.z/factor]

def VectorLength(v):
  return _math.sqrt(v.x*v.x+v.y*v.y+v.z*v.z)

def length(v):
    return _math.sqrt(v.x*v.x+v.y*v.y+v.z*v.z)

def VectorUnitize(v):
  return divide(v,length(v))

def unitize(v):
  return divide(v,length(v))

def VectorCrossProduct(v1,v2):
    return _Vertex(v1.y * v2.z - v2.y * v1.z, v1.z * v2.x - v2.z * v1.x, v1.x * v2.y - v2.x * v1.y)

def cross(v1,v2):
    return _Vertex(v1.y * v2.z - v2.y * v1.z, v1.z * v2.x - v2.z * v1.x, v1.x * v2.y - v2.x * v1.y)

def VectorDotProduct(v1,v2):
  return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z

def dot(v1,v2):
  return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z

def VectorDistance(v1,v2):
  dX=v2.x-v1.x
  dY=v2.y-v1.y
  dZ=v2.z-v1.z
  return _math.sqrt(dX*dX+dY*dY+dZ*dZ)

def distance(v1,v2):
  dX=v2.x-v1.x
  dY=v2.y-v1.y
  dZ=v2.z-v1.z
  return _math.sqrt(dX*dX+dY*dY+dZ*dZ)

def VectorCenter(vertices):
  '''
  return the average of all boundarypoints
  center=[0,0,0]
  for vertex in vertices:
    center=VectorAdd(vertex,center)
  return VectorDivide(center,len(vertices))
  '''
  n = len(vertices)
  cx = sum([v.x for v in vertices])/n
  cy = sum([v.y for v in vertices])/n
  cz = sum([v.z for v in vertices])/n
  return _Vertex(cx,cy,cz)

def center(vertices):
  # return the average of all boundarypoints
  n = len(vertices)
  cx = sum([v.x for v in vertices])/n
  cy = sum([v.y for v in vertices])/n
  cz = sum([v.z for v in vertices])/n
  return _Vertex(cx,cy,cz)

def VectorCenterFromLine(v1,v2):
  return _Vertex((v1.x+v2.x)/2,(v1.y+v2.y)/2,(v1.z+v2.z)/2)

def centerFromLine(v1,v2):
  return _Vertex((v1.x+v2.x)/2,(v1.y+v2.y)/2,(v1.z+v2.z)/2)

def VectorPerimeter(vertices):
  per=0
  for i in range(len(vertices)):
    n1=vertices[i]
    n2=vertices[(i+1)%len(vertices)]
    per+=VectorDistance(n1,n2)
  return per

def perimeter(vertices):
  per=0
  for i in range(len(vertices)):
    n1=vertices[i]
    n2=vertices[(i+1)%len(vertices)]
    per+=distance(n1,n2)
  return per

def VectorBetweenRel( v1,  v2,  f):
    return _Vertex((v2.x - v1.x) * f + v1.x, (v2.y - v1.y) * f + v1.y, (v2.z - v1.z) * f + v1.z)

def betweenRel( v1,  v2,  f):
    return _Vertex((v2.x - v1.x) * f + v1.x, (v2.y - v1.y) * f + v1.y, (v2.z - v1.z) * f + v1.z)

def VectorBetweenAbs( v1,  v2,  f):
  d = VectorDistance(v1,v2)
  return VectorBetweenRel(v1, v2, f / d)

def betweenAbs( v1,  v2,  f):
  d = distance(v1,v2)
  return betweenRel(v1, v2, f / d)

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
  return _Vertex(x,y,0)

def lineLineIntersection(a,b,c,d):
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
  return _Vertex(x,y,0)

def VectorOffsetLine(v1, v2,  offset):
  v = VectorSubtract(v2, v1)
  v=VectorUnitize(v)
  v=VectorScale(v,offset)
  t = v.x
  v.x = -v.y
  v.y = t
  v.z=0
  return _Vertex(VectorAdd(v1,v),VectorAdd(v2,v))

def offsetLine(v1, v2,  offset):
  v =subtract(v2, v1)
  v=unitize(v)
  v=scale(v,offset)
  t = v.x
  v.x = -v.y
  v.y = t
  v.z=0
  return _Vertex(add(v1,v),add(v2,v))

def VectorOffsetPoint(v1,  v2,  v3,  offset1,  offset2):
  line1= VectorOffsetLine(v1, v2, offset1);
  line2= VectorOffsetLine(v2, v3, offset2);
  return VectorLineLineIntersection(line1.x,line1.y,line2.x,line2.y)

def offsetPoint(v1,  v2,  v3,  offset1,  offset2):
  line1= offsetLine(v1, v2, offset1);
  line2= offsetLine(v2, v3, offset2);
  return lineLineIntersection(line1.x,line1.y,line2.x,line2.y)


def VectorNormal(v1,v2,v3):
  v = VectorSubtract(v2, v1)
  u = VectorSubtract(v3, v1)
  c=VectorCrossProduct(v,u)
  return VectorUnitize(c)

def normal(v1,v2,v3):
  v = subtract(v2, v1)
  u = subtract(v3, v1)
  crossProduct=cross(v,u)
  return unitize(crossProduct)

def areaTriangle(v0,v1,v2):
    d1 = distance(v0, v1)
    d2 = distance(v1, v2)
    d3 = distance(v2, v0)
    s = (d1+d2+d3)/2.0
    a = _math.sqrt(s*(s-d1)*(s-d2)*(s-d3))
    return a

def area(vertices):
    if len(vertices) == 3:
        return areaTriangle(vertices[0],vertices[1],vertices[2])
    elif len(vertices) == 4:
        a1 = areaTriangle(vertices[0],vertices[1],vertices[2])
        a2 = areaTriangle(vertices[2],vertices[3],vertices[0])
        return a1+a2

def VectorNormalFromVertices(vertices):
    return VectorNormal(vertices[0],vertices[1],vertices[2])
    # if len(vertices)==3:
    #     return VectorNormal(vertices[0],vertices[1],vertices[2])
    # elif len(vertices)==4:
    #     n1 = VectorNormal(vertices[0],vertices[1],vertices[2])
    #     n2 = VectorNormal(vertices[2],vertices[3],vertices[0])
    # there there is an error. planar surfaces will have identical normals. angle calculation fails?
    #     angle = VectorAngle(n1,n2)
    #     if(angle>_math.pi-0.01):
    #         n2 = VectorScale(n2,-1)
    #         sum = VectorAdd(n1,n2)
    #         sum = VectorScale(sum, 0.5)
    #         sum = VectorUnitize(sum)
    #         return sum

def normalFromVertices(vertices):
    return normal(vertices[0],vertices[1],vertices[2])
    # if len(vertices)==3:
    #     return VectorNormal(vertices[0],vertices[1],vertices[2])
    # elif len(vertices)==4:
    #     n1 = VectorNormal(vertices[0],vertices[1],vertices[2])
    #     n2 = VectorNormal(vertices[2],vertices[3],vertices[0])
    # there there is an error. planar surfaces will have identical normals. angle calculation fails?
    #     angle = VectorAngle(n1,n2)
    #     if(angle>_math.pi-0.01):
    #         n2 = VectorScale(n2,-1)
    #         sum = VectorAdd(n1,n2)
    #         sum = VectorScale(sum, 0.5)
    #         sum = VectorUnitize(sum)
    #         return sum
