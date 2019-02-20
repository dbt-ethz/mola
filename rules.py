import reticula.vecmath as vec
import math

class Face:
    def __init__(self,vertices):
        self.vertices = vertices
        self.color=(1,1,1,1)
def splitRelFreeQuad(face, indexEdge,  split1,  split2):
  indexEdge1=(indexEdge+1)%len(face.vertices)
  indexEdge2=(indexEdge+2)%len(face.vertices)
  indexEdge3=(indexEdge+3)%len(face.vertices)
  p1 = vec.VectorBetweenRel(face.vertices[indexEdge], face.vertices[indexEdge1], split1)
  p2 = vec.VectorBetweenRel(face.vertices[indexEdge2 ], face.vertices[indexEdge3], split2)
  faces=[]
  if indexEdge == 0:
    faces.append(Face([face.vertices[0], p1, p2, face.vertices[3]]))
    faces.append(Face([p1,face.vertices[1],face.vertices[2],p2]))
  elif indexEdge == 1:
    faces.append(Face([face.vertices[0], face.vertices[1], p1, p2]))
    faces.append(Face([p2, p1, face.vertices[2], face.vertices[3]]))
  return faces
  
def extrude(face,extrusion,capBottom=False,capTop=True):
  normal=vec.VectorNormal(face.vertices[0],face.vertices[1],face.vertices[2])
  normal=vec.VectorScale(normal,extrusion)
  # calculate vertices
  new_vertices=[]
  for i in range(len(face.vertices)):
    new_vertices.append(vec.VectorAdd(face.vertices[i], normal))
  # faces
  new_faces=[] 
  if capBottom:
    new_faces.append(face)     
  for i in range(len(face.vertices)):
    i2=i+1
    if i2>=len(face.vertices):
      i2=0
    v0=face.vertices[i]
    v1=face.vertices[i2]
    v2=new_vertices[i2]
    v3=new_vertices[i]
    new_faces.append(Face([v0,v1,v2,v3]))                   
  if capTop:
    new_faces.append(Face(new_vertices)) 
  for new_face in new_faces:
    new_face.color=face.color
  return new_faces
  
def extrudeToPoint(face, point):
  numV = len(face.vertices)
  faces = []
  for i in range(numV):
    v1 = face.vertices[i]
    v2 = face.vertices[(i+1)%numV]
    faces.append(Face([v1,v2,point]))
  return faces

def extrudeToPointCenter(face, extrusionHeight):
  normal = vec.VectorNormalFromVertices(face.vertices)
  normal = vec.VectorScale(normal,extrusionHeight)
  center = vec.VectorCenter(face.vertices)
  center = vec.VectorAdd(center,normal)
  return extrudeToPoint(face,center)

def constructBoxFaces(x1,y1,z1,x2,y2,z2):
  v1 = [x1,y1,z1]
  v2 = [x1,y2,z1]
  v3 = [x2,y2,z1]
  v4 = [x2,y1,z1]
  v5 = [x1,y1,z2]
  v6 = [x1,y2,z2]
  v7 = [x2,y2,z2]
  v8 = [x2,y1,z2]
  f1 = Face([v1, v2, v3, v4])
  f2 = Face([v8, v7, v6, v5])
  f3 = Face([v4, v3, v7, v8])
  f4 = Face([v3, v2, v6, v7])
  f5 = Face([v2, v1, v5, v6])
  f6 = Face([v1, v4, v8, v5])
  faces = []
  faces.extend([f1,f2,f3,f4,f5,f6])
  return faces
