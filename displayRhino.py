import rhinoscriptsyntax as rs
def display(faces):
    vertices=[]
    facesIndices=[]
    vertexColors=[]
    for f in faces:
        faceIndices=[]
        for v in f.vertices:
            faceIndices.append(len(points))
            vertices.append(v)
        facesIndices.append(faceIndices)
        vertexColors.append((face.color[0]*255,face.color[1]*255,face.color[2]*255))
    rs.AddMesh(vertices,facesIndices,None,None,vertexColors)
