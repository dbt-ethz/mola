from mola.core import *
import mola.vec as _vec

def _collectNewFaces(_mesh):
    newMesh=Mesh()
    for face in _mesh.faces:
        v1=face.vertices[-2]
        v2=face.vertices[-1]
        for v3 in face.vertices:
            edge1=_mesh.getEdgeAdjacentToVertices(v1,v2)
            edge2=_mesh.getEdgeAdjacentToVertices(v2,v3)
            if (edge1 != None) and (edge2!= None):
                newFace=Face([edge1.vertex,v2.vertex,edge2.vertex,face.vertex])
                newFace.color=face.color
                newFace.group=face.group
                newMesh.faces.append(newFace)
            v1=v2
            v2=v3
    newMesh.updateAdjacencies()
    return newMesh

def subdivide(_mesh):
    for face in _mesh.faces:
        face.vertex=_vec.center(face.vertices)
    for edge in _mesh.edges:
        edge.vertex = edge.getCenter()
    for vertex in _mesh.vertices:
        vertex.vertex = Vertex(vertex.x,vertex.y,vertex.z)
    return _collectNewFaces(_mesh)

def subdivideCatmull(_mesh):
    for face in _mesh.faces:
        face.vertex=_vec.center(face.vertices)

    for edge in _mesh.edges:
        edge.vertex = edge.getCenter()

    for edge in _mesh.edges:
        vsum=Vertex()
        vsum=_vec.add(vsum,edge.v1)
        vsum=_vec.add(vsum,edge.v2)
        vsum=_vec.add(vsum,edge.face1.vertex)
        vsum=_vec.add(vsum,edge.face2.vertex)
        vsum=_vec.scale(vsum,0.25)
        edge.vertex=vsum

    for vertex in _mesh.vertices:
        averageFaces=Vertex()
        averageEdges=Vertex()
        nEdges=len(vertex.edges)

        for edge in vertex.edges:
            face=edge.face1
            if edge.v2==vertex:
                face=edge.face2
            averageFaces=_vec.add(averageFaces,face.vertex)
            averageEdges=_vec.add(averageEdges,edge.getCenter())
        averageEdges=_vec.scale(averageEdges,2.0/nEdges)
        averageFaces=_vec.scale(averageFaces,1.0/nEdges)

        v=Vertex(vertex.x,vertex.y,vertex.z)
        v=_vec.scale(v,nEdges-3)
        v=_vec.add(v,averageFaces)
        v=_vec.add(v,averageEdges)
        v=_vec.scale(v,1.0/nEdges)
        vertex.vertex=v

    return _collectNewFaces(_mesh)
