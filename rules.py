import reticula.vecmath as vec
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
  normal = vec.VectorNormalFromVertices(face)
  normal = vec.VectorScale(normal,extrusionHeight)
  center = vec.VectorCenter(face)
  center = vec.VectorAdd(center,normal)
  return extrudeToPoint(face,center)
