from mola.core import Mesh as _Mesh
from mola.core import Vertex as _Vertex
from mola.core import Face as _Face
import mola.vec as _vec

def splitRelFreeQuad(face, indexEdge,  split1,  split2):
    """
    Splits a quad in two new quads through the points specified
    by relative position along the edge.

    Arguments:
    ----------
    face : mola.core.Face
        The face to be extruded
    indexEdge : int
        direction of split, 0: 0->2, 1: 1->3
    split1, split2 : float
        relative position of split on each edge (0..1)
    """
    # only works with quads, therefore return original face if triangular
    if len(face.vertices) != 4:
        return face

    # constrain indexEdge to be either 0 or 1
    indexEdge = indexEdge%2

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

def extrude(face, height=0.0, capBottom=False, capTop=True):
    """
    Extrudes the face straight by distance height.

    Arguments:
    ----------
    face : mola.core.Face
        The face to be extruded
    height : float
        The extrusion distance, default 0
    capBottom : bool
        Toggle if bottom face (original face) should be created, default False
    capTop : bool
        Toggle if top face (extrusion face) should be created, default True
    """
    normal=_vec.VectorNormal(face.vertices[0],face.vertices[1],face.vertices[2])
    normal=_vec.VectorScale(normal,height)
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

def extrudeTapered(face, height=0.0, fraction=0.5):
    """
    Extrudes the face tapered like a window by creating an
    offset face and quads between every original edge and the
    corresponding new edge.

    Arguments:
    ----------
    face : mola.core.Face
        The face to be extruded
    height : float
        The distance of the new face to the original face, default 0
    fraction : float
        The relative offset distance, 0: original vertex, 1: center point
        default 0.5 (halfway)
    """
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

def splitRoof(face, height):
    """
    Extrudes a pitched roof

    Arguments:
    ----------
    face : mola.core.Face
        The face to be extruded
    height : mola.core.Vertex
        Th height of the roof
    """
    faces = []
    normal = _vec.VectorNormalFromVertices(face.vertices)
    normal = _vec.VectorScale(normal,height)
    if len(face.vertices)==4:
        ev1=_vec.VectorCenterFromLine(face.vertices[0],face.vertices[1])
        ev1=_vec.VectorAdd(ev1,normal)
        ev2=_vec.VectorCenterFromLine(face.vertices[2],face.vertices[3])
        ev2=_vec.VectorAdd(ev2,normal)

        faces.append(_Face([face.vertices[0],face.vertices[1],ev1]))
        faces.append(_Face([face.vertices[1],face.vertices[2],ev2,ev1]))
        faces.append(_Face([face.vertices[2],face.vertices[3],ev2]))
        faces.append(_Face([face.vertices[3],face.vertices[0],ev1,ev2]))
        return faces
    elif len(face.vertices)==3:
        ev1=_vec.VectorCenterFromLine(face.vertices[0],face.vertices[1])
        ev1=_vec.VectorAdd(ev1,normal)
        ev2=_vec.VectorCenterFromLine(face.vertices[1],face.vertices[2])
        ev2=_vec.VectorAdd(ev2,normal)

        faces.append(_Face([face.vertices[0],face.vertices[1],ev1]))
        faces.append(_Face([face.vertices[1],ev2,ev1]))
        faces.append(_Face([face.vertices[1],face.vertices[2],ev2]))
        faces.append(_Face([face.vertices[2],face.vertices[0],ev1,ev2]))
        return faces
    return [face]

def extrudeToPoint(face, point):
    """
    Extrudes the face to a point by creating a
    triangular face from each edge to the point.

    Arguments:
    ----------
    face : mola.core.Face
        The face to be extruded
    point : mola.core.Vertex
        The point to extrude to
    """
    numV = len(face.vertices)
    faces = []
    for i in range(numV):
        v1 = face.vertices[i]
        v2 = face.vertices[(i+1)%numV]
        faces.append(_Face([v1,v2,point]))
    return faces

def extrudeToPointCenter(face, height=0.0):
    """
    Extrudes the face to the center point moved by height
    normal to the face and creating a triangular face from
    each edge to the point.

    Arguments:
    ----------
    face : mola.core.Face
        The face to be extruded
    height : float
        The distance of the new point to the face center, default 0
    """
    normal = _vec.VectorNormalFromVertices(face.vertices)
    normal = _vec.VectorScale(normal,height)
    center = _vec.VectorCenter(face.vertices)
    center = _vec.VectorAdd(center,normal)
    return extrudeToPoint(face,center)
