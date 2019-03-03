from mola.core import *
import mola.vec as _vec

def subdivide(_mesh):
    new_mesh=_mesh()
    new_mesh.faces=[]
    new_mesh.edges=[]
    new_mesh.vertices=[]
    for face in _mesh.faces:
        face.vertex=_vec.VectorCenter(face.vertices)
    for edge in _mesh.edges:
        edge.vertex = edge.getCenter()
    for vertex in _mesh.vertices:
        vertex.vertex = Vertex(vertex.x,vertex.y,vertex.z)
    for face in _mesh.faces:
        v1=face.vertices[-2]
        v2=face.vertices[-1]
        for v3 in face.vertices:
            edge1=_mesh.getEdgeAdjacentToVertices(v1,v2)
            edge2=_mesh.getEdgeAdjacentToVertices(v2,v3)
            if (edge1 != None) and (edge2!= None):
                newFace=Face([edge1.vertex,v2.vertex,edge2.vertex,face.vertex])
                newFace.color=face.color
                new_mesh.faces.append(newFace)
            v1=v2
            v2=v3
    new_mesh.weldVertices()
    new_mesh.updateAdjacencies()
    return new_mesh

def subdivideCatmull(_mesh):
    newMesh=Mesh()

    # why do i have faces in the lists?
    newMesh.faces=[]
    newMesh.edges=[]
    newMesh.vertices=[]

    for face in _mesh.faces:
        face.vertex=_vec.VectorCenter(face.vertices)

    for edge in _mesh.edges:
        edge.vertex = edge.getCenter()

    for edge in _mesh.edges:
        vsum=Vertex()
        vsum=_vec.VectorAdd(vsum,edge.v1)
        vsum=_vec.VectorAdd(vsum,edge.v2)
        vsum=_vec.VectorAdd(vsum,edge.face1.vertex)
        vsum=_vec.VectorAdd(vsum,edge.face2.vertex)
        vsum=_vec.VectorScale(vsum,0.25)
        edge.vertex=vsum

    for vertex in _mesh.vertices:
        averageFaces=Vertex()
        averageEdges=Vertex()
        nEdges=len(vertex.edges)

        for edge in vertex.edges:
            face=edge.face1
            if edge.v2==vertex:
                face=edge.face2
            averageFaces=_vec.VectorAdd(averageFaces,face.vertex)
            averageEdges=_vec.VectorAdd(averageEdges,edge.getCenter())
        averageEdges=_vec.VectorScale(averageEdges,2.0/nEdges)
        averageFaces=_vec.VectorScale(averageFaces,1.0/nEdges)

        v=Vertex(vertex.x,vertex.y,vertex.z)
        v=_vec.VectorScale(v,nEdges-3)
        v=_vec.VectorAdd(v,averageFaces)
        v=_vec.VectorAdd(v,averageEdges)
        v=_vec.VectorScale(v,1.0/nEdges)
        vertex.vertex=v

    for face in _mesh.faces:
        v1=face.vertices[-2]
        v2=face.vertices[-1]
        for v3 in face.vertices:
            edge1=_mesh.getEdgeAdjacentToVertices(v1,v2)
            edge2=_mesh.getEdgeAdjacentToVertices(v2,v3)
            if (edge1 != None) and (edge2!= None):
                newFace=Face([edge1.vertex,v2.vertex,edge2.vertex,face.vertex])
                newFace.color=face.color
                newMesh.faces.append(newFace)
            v1=v2
            v2=v3

    newMesh.weldVertices()
    newMesh.updateAdjacencies()
    return newMesh
