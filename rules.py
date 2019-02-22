import mola.vecmath as vec
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

def constructIcosahedronFaces(cx,cy,cz,radius):
    phi = (1 + 5 ** 0.5) / 2
    coordA = 1/(2*math.sin(2*math.pi/5))
    coordB = phi/(2*math.sin(2*math.pi/5))
    vertices = [(0,-coordA,coordB),
                (coordB, 0, coordA),
                (coordB, 0, -coordA),
                (-coordB, 0, -coordA),
                (-coordB, 0, coordA),
                (-coordA, coordB, 0),
                (coordA, coordB, 0),
                (coordA, -coordB, 0),
                (-coordA, -coordB, 0),
                (0, -coordA, -coordB),
                (0, coordA, -coordB),
                (0, coordA, coordB)]

    for i in range(len(vertices)):
        vertices[i] = vec.VectorScale(vertices[i],radius)
        vertices[i] = vec.VectorAdd(vertices[i],(cx,cy,cz))

    indices = [1, 2, 6, 1, 7, 2, 3, 4, 5, 4, 3, 8, 6, 5, 11, 5, 6, 10, 9, 10, 2, 10, 9, 3, 7, 8, 9, 8, 7, 0, 11, 0, 1, 0, 11, 4, 6, 2, 10, 1, 6, 11, 3, 5, 10, 5, 4, 11, 2, 7, 9, 7, 1, 0, 3, 9, 8, 4, 8, 0]
    faces = []

    for i in range(0,len(indices),3):
        f = Face([vertices[indices[i]],vertices[indices[i + 1]],vertices[indices[i + 2]]])
        faces.append(f)
    return faces

def construct DodecahedronFaces(cx,cy,cz,radius):
    phi = (1 + 5**0.5)/2
    vertices = [( 1, 1, 1),
                ( 1, 1,-1),
                ( 1,-1, 1),
                ( 1,-1,-1),
                (-1, 1, 1),
                (-1, 1,-1),
                (-1,-1, 1),
                (-1,-1,-1),
                (0,-phi,-1/phi),
                (0,-phi, 1/phi),
                (0, phi,-1/phi),
                (0, phi, 1/phi),
                (-phi,-1/phi,0),
                (-phi, 1/phi,0),
                ( phi,-1/phi,0),
                ( phi, 1/phi,0),
                (-1/phi,0,-phi),
                ( 1/phi,0,-phi),
                (-1/phi,0, phi),
                ( 1/phi,0, phi)]

    for i in range(len(vertices)):
        vertices[i] = vec.VectorScale(vertices[i],radius)
        vertices[i] = vec.VectorAdd(vertices[i],(cx,cy,cz))
    indices = []
    faces = []

def constructTetrahedronFaces(cx,cy,cz,side):
  coord = 1/math.sqrt(2)
  vertices = [(+1,0,-coord),
             (-1,0,-coord),
             (0,+1,+coord),
             (0,-1,+coord)]

  for i in range(len(vertices)):
    vertices[i] = vec.VectorScale(vertices[i],side/2)
    vertices[i] = vec.VectorAdd(vertices[i],(cx,cy,cz))

  f1 = Face([vertices[0],vertices[1],vertices[2]])
  f2 = Face([vertices[1],vertices[0],vertices[3]])
  f3 = Face([vertices[2],vertices[3],vertices[0]])
  f4 = Face([vertices[3],vertices[2],vertices[1]])

  faces = [f1,f2,f3,f4]
  return faces
