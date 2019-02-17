def VectorAdd(v1,v2):
  return [v1[0]+v2[0],v1[1]+v2[1],v1[2]+v2[2]]

def VectorAngle(v1,v2):
  a=VectorUnitize(v1)
  b=VectorUnitize(v2)
  return math.acos(VectorDotProduct(a,b))

def VectorSubtract(v1,v2):
  return [v1[0]-v2[0],v1[1]-v2[1],v1[2]-v2[2]]

def VectorScale(v,factor):
  return [v[0]*factor,v[1]*factor,v[2]*factor]

def VectorDivide(v,factor):
  return [v[0]/factor,v[1]/factor,v[2]/factor]

def VectorLength(v):
  return math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])

def VectorUnitize(v):
  return VectorDivide(v,VectorLength(v))

def VectorCrossProduct(v1,v2):
  return [v1[1] * v2[2] - v2[1] * v1[2],v1[2] * v2[0] - v2[2] * v1[0],v1[0] * v2[1] - v2[0] * v1[1]]

def VectorDotProduct(v1,v2):
  return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def VectorDistance(v1,v2):
  dX=v2[0]-v1[0]
  dY=v2[1]-v1[1]
  dZ=v2[2]-v1[2]
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
  return [(v2[0] - v1[0]) * f + v1[0], (v2[1] - v1[1]) * f + v1[1], (v2[2] - v1[2]) * f + v1[2]]

def VectorBetweenAbs( v1,  v2,  f):
  d = VectorDistance(v1,v2)
  return VectorBetweenRel(v1, v2, f / d)

def VectorLineLineIntersection(a,b,c,d):
  deltaABX=b[0] - a[0]
  deltaABY=b[1] - a[1]
  deltaDCX=d[0] - c[0]
  deltaDCY=d[1] - c[1]
  denominator = deltaABX * deltaDCY - deltaABY * deltaDCX
  if denominator == 0:
    return None
  numerator = (a[1] - c[1]) * deltaDCX - (a[0] - c[0]) * deltaDCY
  r = numerator / denominator
  x = a[0] + r * deltaABX
  y = a[1] + r * deltaABY
  return [x,y,0]

def VectorOffsetLine(v1, v2,  offset):
  v = VectorSubtract(v2, v1)
  v=VectorUnitize(v)
  v=VectorScale(v,offset)
  t = v[0]
  v[0] = -v[1]
  v[1] = t
  v[2]=0
  return [VectorAdd(v1,v),VectorAdd(v2,v)]

def VectorOffsetPoint(v1,  v2,  v3,  offset1,  offset2):
  line1= VectorOffsetLine(v1, v2, offset1);
  line2= VectorOffsetLine(v2, v3, offset2);
  return VectorLineLineIntersection(line1[0],line1[1],line2[0],line2[1])

def VectorNormal(v1,v2,v3):
  v = VectorSubtract(v2, v1)
  u = VectorSubtract(v3, v1)
  cross=VectorCrossProduct(v,u)
  return VectorUnitize(cross)

def VectorNormalFromVertices(vertices):
  if len(vertices)==3:  
    return VectorNormal(vertices[0],vertices[1],vertices[2])
  elif len(face.vertices)==4:
    n1 = VectorNormal(vertices[0],vertices[1],vertices[2])
    n2 = VectorNormal(vertices[2],vertices[3],vertices[0])
    angle = VectorAngle(n1,n2)
    if(angle>math.pi-0.01):
      n2 = VectorScale(n2,-1)
    sum = VectorAdd(n1,n2)
    sum = VectorScale(sum, 0.5)
    sum = VectorUnitize(sum)
    return sum