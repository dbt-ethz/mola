from mola.core import Mesh as _Mesh
from mola.core import Vertex as _Vertex
from mola.core import Face as _Face
import mola.meshMath as _vec

def splitRelFreeQuad(face, indexEdge,  split1,  split2):
    indexEdge1=(indexEdge+1)%len(face.vertices)
    indexEdge2=(indexEdge+2)%len(face.vertices)
    indexEdge3=(indexEdge+3)%len(face.vertices)
    p1 = _vec.VectorBetweenRel(face.vertices[indexEdge], face.vertices[indexEdge1], split1)
    p2 = _vec.VectorBetweenRel(face.vertices[indexEdge2 ], face.vertices[indexEdge3], split2)
    faces=[]
    if indexEdge == 0:
        faces.append(_Face([face.vertices[0], p1, p2, face.vertices[3]]))
        faces.append(_Face([p1,face.vertices[1],face.vertices[2],p2]))
    elif indexEdge == 1:
        faces.append(_Face([face.vertices[0], face.vertices[1], p1, p2]))
        faces.append(_Face([p2, p1, face.vertices[2], face.vertices[3]]))
    return faces

def extrude(face,extrusion,capBottom=False,capTop=True):
    normal=_vec.VectorNormal(face.vertices[0],face.vertices[1],face.vertices[2])
    normal=_vec.VectorScale(normal,extrusion)
    # calculate vertices
    new_vertices=[]
    for i in range(len(face.vertices)):
        new_vertices.append(_vec.VectorAdd(face.vertices[i], normal))
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
    new_faces.append(_Face([v0,v1,v2,v3]))
    if capTop:
        new_faces.append(_Face(new_vertices))
    for new_face in new_faces:
        new_face.color=face.color
    return new_faces

def extrudeTapered(face, height, fraction):
    center_vertex = _vec.VectorCenter(face.vertices)
    normal = _vec.VectorNormalFromVertices(face.vertices)
    scaled_normal = _vec.VectorScale(normal, height)

    # calculate new vertex positions
    new_vertices = []
    for i in range(len(face.vertices)):
        n1 = face.vertices[i]
        betw = _vec.VectorSubtract(center_vertex, n1)
        betw = _vec.VectorScale(betw, fraction)
        nn = _vec.VectorAdd(n1, betw)
        nn = _vec.VectorAdd(nn, scaled_normal)
        new_vertices.append(nn)

    new_faces = []
    # create the quads along the edges
    num = len(face.vertices)
    for i in range(num):
        n1 = face.vertices[i]
        n2 = face.vertices[(i+1) % num]
        n3 = new_vertices[(i+1) % num]
        n4 = new_vertices[i]
        new_face = _Face([n1,n2,n3,n4])
        new_faces.append(new_face)

    # create the closing cap face
    cap_face = _Face(new_vertices)
    new_faces.append(cap_face)

    return new_faces

def extrudeToPoint(face, point):
    numV = len(face.vertices)
    faces = []
    for i in range(numV):
        v1 = face.vertices[i]
        v2 = face.vertices[(i+1)%numV]
        faces.append(_Face([v1,v2,point]))
    return faces

def extrudeToPointCenter(face, extrusionHeight):
    normal = _vec.VectorNormalFromVertices(face.vertices)
    normal = _vec.VectorScale(normal,extrusionHeight)
    center = _vec.VectorCenter(face.vertices)
    center = _vec.VectorAdd(center,normal)
    return extrudeToPoint(face,center)
