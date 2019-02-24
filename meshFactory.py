from mola.core import Mesh
from mola.core import Vertex
from mola.core import Face
import mola.meshMath as vec

def constructBoxMesh(x1,y1,z1,x2,y2,z2):
    mesh = Mesh()
    v1 = Vertex(x1,y1,z1)
    v2 = Vertex(x1,y2,z1)
    v3 = Vertex(x2,y2,z1)
    v4 = Vertex(x2,y1,z1)
    v5 = Vertex(x1,y1,z2)
    v6 = Vertex(x1,y2,z2)
    v7 = Vertex(x2,y2,z2)
    v8 = Vertex(x2,y1,z2)
    mesh.vertices=[v1,v2,v3,v4,v5,v6,v7,v8]
    f1 = Face([v1, v2, v3, v4])
    f2 = Face([v8, v7, v6, v5])
    f3 = Face([v4, v3, v7, v8])
    f4 = Face([v3, v2, v6, v7])
    f5 = Face([v2, v1, v5, v6])
    f6 = Face([v1, v4, v8, v5])
    mesh.faces=[f1,f2,f3,f4,f5,f6]
    return mesh

def constructIcosahedronMesh(cx,cy,cz,radius):
    mesh=Mesh()
    phi = (1 + 5 ** 0.5) / 2
    coordA = 1/(2*math.sin(2*math.pi/5))
    coordB = phi/(2*math.sin(2*math.pi/5))
    mesh.vertices = [Vertex(0,-coordA,coordB),
                Vertex(coordB, 0, coordA),
                Vertex(coordB, 0, -coordA),
                Vertex(-coordB, 0, -coordA),
                Vertex(-coordB, 0, coordA),
                Vertex(-coordA, coordB, 0),
                Vertex(coordA, coordB, 0),
                Vertex(coordA, -coordB, 0),
                Vertex(-coordA, -coordB, 0),
                Vertex(0, -coordA, -coordB),
                Vertex(0, coordA, -coordB),
                Vertex(0, coordA, coordB)]

    for i in range(len(mesh.vertices)):
        mesh.vertices[i] = vec.VectorScale(mesh.vertices[i],radius)
        mesh.vertices[i] = vec.VectorAdd(mesh.vertices[i],Vertex(cx,cy,cz))

    indices = [1, 2, 6, 1, 7, 2, 3, 4, 5, 4, 3, 8, 6, 5, 11, 5, 6, 10, 9, 10, 2, 10, 9, 3, 7, 8, 9, 8, 7, 0, 11, 0, 1, 0, 11, 4, 6, 2, 10, 1, 6, 11, 3, 5, 10, 5, 4, 11, 2, 7, 9, 7, 1, 0, 3, 9, 8, 4, 8, 0]
    faces = []

    for i in range(0,len(indices),3):
        f = Face([mesh.vertices[indices[i]],mesh.vertices[indices[i + 1]],mesh.vertices[indices[i + 2]]])
        faces.append(f)
    mesh.faces=faces
    return mesh

def constructDodecahedronMesh(cx,cy,cz,radius):
    mesh=Mesh()
    phi = (1 + 5**0.5)/2
    mesh.vertices = [Vertex( 1, 1, 1),
                Vertex( 1, 1,-1),
                Vertex( 1,-1, 1),
                Vertex( 1,-1,-1),
                Vertex(-1, 1, 1),
                Vertex(-1, 1,-1),
                Vertex(-1,-1, 1),
                Vertex(-1,-1,-1),
                Vertex(0,-phi,-1/phi),
                Vertex(0,-phi, 1/phi),
                Vertex(0, phi,-1/phi),
                Vertex(0, phi, 1/phi),
                Vertex(-phi,-1/phi,0),
                Vertex(-phi, 1/phi,0),
                Vertex( phi,-1/phi,0),
                Vertex( phi, 1/phi,0),
                Vertex(-1/phi,0,-phi),
                Vertex( 1/phi,0,-phi),
                Vertex(-1/phi,0, phi),
                Vertex( 1/phi,0, phi)]

    for i in range(len(mesh.vertices)):
        mesh.vertices[i] = vec.VectorScale(mesh.vertices[i],radius)
        mesh.vertices[i] = vec.VectorAdd(mesh.vertices[i],Vertex(cx,cy,cz))
    indices = [2,9,6,18,19,
               4,11,0,19,18,
               18,6,12,13,4,
               19,0,15,14,2,
               4,13,5,10,11,
               14,15,1,17,3,
               1,15,0,11,10,
               3,17,16,7,8,
               2,14,3,8,9,
               6,9,8,7,12,
               1,10,5,16,17,
               12,7,16,5,13]

    faces = []
    for i in range(0,len(indices),5):
        f = Face([mesh.vertices[indices[i]],
                  mesh.vertices[indices[i + 1]],
                  mesh.vertices[indices[i + 2]],
                  mesh.vertices[indices[i + 3]],
                  mesh.vertices[indices[i + 4]]])
        faces.append(f)
    mesh.faces=faces
    return mesh

def constructTetrahedronMesh(cx,cy,cz,side):
    mesh=Mesh()
    coord = 1/math.sqrt(2)
    mesh.vertices = [Vertex(+1,0,-coord),
                     Vertex(-1,0,-coord),
                     Vertex(0,+1,+coord),
                     Vertex(0,-1,+coord)]

    for i in range(len(vertices)):
        mesh.vertices[i] = vec.VectorScale(mesh.vertices[i],side/2)
        mesh.vertices[i] = vec.VectorAdd(mesh.vertices[i],Vertex(cx,cy,cz))

    f1 = Face([mesh.vertices[0],mesh.vertices[1],mesh.vertices[2]])
    f2 = Face([mesh.vertices[1],mesh.vertices[0],mesh.vertices[3]])
    f3 = Face([mesh.vertices[2],mesh.vertices[3],mesh.vertices[0]])
    f4 = Face([mesh.vertices[3],mesh.vertices[2],mesh.vertices[1]])

    mesh.faces = [f1,f2,f3,f4]
    return mesh
