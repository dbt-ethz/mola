from mola.core import Mesh as Mesh
from mola.core import Vertex as Vertex
from mola.core import Face as Face
from mola.core import Edge as Edge
from mola.core import Edge as Edge

def split(mesh,z):
    edges=[]
    for face in mesh.faces:
        if len(face.vertices)==4:
            edge=splitTriangle((face.vertices[0],face.vertices[1],face.vertices[2]),z)
            if edge!=None:
                edges.append(edge)
            edge=splitTriangle((face.vertices[2],face.vertices[3],face.vertices[0]),z)
            if edge!=None:
                edges.append(edge)
        if len(face.vertices)==3:
            edge=splitTriangle(face.vertices,z)
            if edge!=None:
                edges.append(edge)
    return edges

def splitTriangle(vertices,z):
    intersections=[]
    vPrev=vertices[-1]
    for v in vertices:
        if v.z==z:

            intersections.append(Vertex(v.x,v.y,v.z))
        elif vPrev.z<z!=v.z<z:
            deltaZ=v.z-vPrev.z

            if deltaZ!=0:
                f=(z-vPrev.z)/deltaZ
                x=f*(v.x-vPrev.x)+vPrev.x
                y=f*(v.y-vPrev.y)+vPrev.y
                intersections.append(Vertex(x,y,z))
        vPrev=v
    if len(intersections)==2:
        dX=intersections[0].x-intersections[1].x
        dY=intersections[0].y-intersections[1].y
        if dX!=0 or dY!=0:
            return Edge(intersections[0],intersections[1])
    return None

# def weldVertices(edges):
#     dictVertices={}
#     for edge in edges:
#         tuple=(edge.v1.x,edge.v1.y)
#         if tuple in dictVertices:
#             edge.v1=dictVertices[tuple]
#         else:
#             dictVertices[tuple]=edge.v1
#         edge.v1.edges.append(edge)
#
#         tuple=(edge.v2.x,edge.v2.y)
#         if tuple in dictVertices:
#             edge.v2=dictVertices[tuple]
#         else:
#             dictVertices[tuple]=edge.v2
#         edge.v2.edges.append(edge)
#
# def edgesToRing(edges):
#     # can be multiple rings
#     rings=[]
#     edgesToCheck=set(edges)
#
#     # find segments between vertices with not 2 edges
#     for e in edges:
#         if len(e.v1.edges)!=2:
#             ring=[]
#             rings.append(ring)
#             nextE=e
#             while len(nextE.v2.edges)==2:
#                 ring.append(nextE.v1)
#                 edgesToCheck.remove(nextE)
#                 for nE in nextE.v2.edges:
#                     if nE!=nextE
#                         nextE=nE
#                         break
#             ring.append(nextE.v2)
#
#     # find closed rings
#     while len(edgesToCheck)>0:
#         nextE=edgesToCheck.pop()
#         startE=nextE
#         ring=[]
#         rings.append(ring)
#         while True:
#             ring.append(nextE.v1)
#             edgesToCheck.remove(nextE)
#             for nE in nextE.v2.edges:
#                 if nE!=nextE
#                     nextE=nE
#                     break
#             if nextE==startE:
#                 ring.append(nextE.v1)
#                 break
#     return rings
