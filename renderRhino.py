import rhinoscriptsyntax as rs
def displayMesh(mesh):
    display(mesh.faces)

def display(faces):
    vertices=[]
    facesIndices=[]
    vertexColors=[]
    for f in faces:
        faceIndices=[]
        for v in f.vertices:
            faceIndices.append(len(vertices))
            vertices.append((v.x,v.y,v.z))
            vertexColors.append((f.color[0]*255,f.color[1]*255,f.color[2]*255))
        facesIndices.append(faceIndices)
    rs.AddMesh(vertices,facesIndices,None,None,vertexColors)
