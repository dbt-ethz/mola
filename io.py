from mola.core import Mesh as _Mesh
from mola.core import Vertex as _Vertex
from mola.core import Face as _Face

def importOBJMesh(filename):
    """Loads a Wavefront OBJ file. """
    mesh=_Mesh()
    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'v':
            v = map(float, values[1:4])
            mesh.vertices.append(_Vertex(v[0],v[1],v[2]))
        elif values[0] == 'f':
            face = _Face([])
            for v in values[1:]:
                w = v.split('/')
                vertex=mesh.vertices[int(w[0])-1]
                face.vertices.append(vertex)
                mesh.faces.append(face)
    return mesh

def importOBJFaces(filename):
    """Loads a Wavefront OBJ file. """
    return importOBJMesh(fileName).faces

def exportOBJMeshWithColors(mesh,fileNameOBJ,fileNameMTL):
    exportOBJFacesWithColors(mesh.faces,fileNameOBJ,fileNameMTL)

def exportOBJFacesWithColors(faces,fileNameOBJ,fileNameMTL):
    exportMtl=True
    weldVertices=True

    """
    Exports the faces as an Alias wavefront obj file.

    Arguments:
    ----------
    faces : list of mola.core.Face
        The face to be measured
    fileNameOBJ : String
        The path and filename for the *.obj mesh file
    fileNameMTL : String
        The path and filename for the *.mtl material file
    """

    file = open(fileNameOBJ, "w")
    if exportMtl:
        file.write("mtllib ./"+fileNameMTL+"\n");
        fileMTL = open(fileNameMTL, "w")
        materials=set()

    vertexCount=0
    vertices={}
    for face in faces:
        if exportMtl:
            materials.add(face.color)
            file.write("usemtl material"+str(face.color)+"\n")
        faceString="f"
        for p in face.vertices:
            #ptuple=(p[0],p[1],p[2])
            ptuple=(p.x,p.y,p.z)
            if ptuple in vertices:
                faceString+=" "+str(vertices[ptuple])
            else:
                vertexCount+=1
                faceString+=" "+str(vertexCount)
                vertices[ptuple]=vertexCount
                file.write("v "+str(p.x)+" "+str(p.y)+" "+str(p.z)+"\n")
        faceString+="\n"
        file.write(faceString)
    file.close()

    if exportMtl:
        for mat in materials:
            fileMTL.write("newmtl material"+str(mat)+"\n");
            fileMTL.write("Kd "+str(mat[0])+" "+" "+str(mat[1])+" "+str(mat[2])+"\n");
            fileMTL.close()

def exportOBJFaces(faces,fileNameOBJ):
    """
    Exports the faces as an Alias wavefront obj file.

    Arguments:
    ----------
    faces : list of mola.core.Face
        The face to be measured
    fileNameOBJ : String
        The path and filename for the *.obj mesh file
    """
    file = open(fileNameOBJ, "w")
    vertexCount=0
    vertices={}
    for face in faces:
        faceString="f"
        for p in face.vertices:
            ptuple=(p.x,p.y,p.z)
            if ptuple in vertices:
                faceString+=" "+str(vertices[ptuple])
            else:
                vertexCount+=1
                faceString+=" "+str(vertexCount)
                vertices[ptuple]=vertexCount
                file.write("v "+str(p.x)+" "+str(p.y)+" "+str(p.z)+"\n")
        faceString+="\n"
        file.write(faceString)
    file.close()
