#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

from mola.core_mesh import Mesh
from mola.core_vertex import Vertex
from mola.core_face import Face
import ntpath

def __strColor(color,decimals=1):
    colorRound = (round(color[0],decimals),round(color[1],decimals),round(color[2],decimals),round(color[3],decimals))
    return str(colorRound)

def import_obj(filename):
    """Loads a Wavefront OBJ file. """
    mesh = Mesh()
    group = ""
    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'g':
            group=values[1]
        elif values[0] == 'v':
            v = [float(c) for c in values[1 : 4]]
            #v = map(float, values[1:4])
            mesh.vertices.append(Vertex(v[0],v[1],v[2]))
        elif values[0] == 'f':
            face = Face([])
            face.group = group
            for v in values[1:]:
                w = v.split('/')
                vertex = mesh.vertices[int(w[0]) - 1]
                face.vertices.append(vertex)
            mesh.faces.append(face)
    return mesh

def import_obj_faces(filename):
    """Loads a Wavefront OBJ file. """
    return import_obj(filename).faces

def export_obj(mesh,fileNameOBJ,exportColors=True,exportGroups=True,weldVertices=True):
    export_obj_faces(mesh.faces,fileNameOBJ,exportColors,exportGroups,weldVertices)

def export_obj_faces(faces,fileNameOBJ,exportColors=True,exportGroups=True,weldVertices=True):
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
    if exportColors:
        fileNameMTL = ntpath.basename(fileNameOBJ) + ".mtl"
        file.write("mtllib ./" + fileNameMTL + "\n")
        fileMTL = open(fileNameOBJ + ".mtl", "w")
        materials = {}

    if exportGroups:
        faces.sort(key = lambda x: x.group)

    vertexCount = 0
    vertices = {}
    currentGroup = None

    for face in faces:
        if exportGroups and face.group != currentGroup:
            file.write("g " + str(face.group) + "\n")
            currentGroup = face.group
        if exportColors:
            materials[__strColor(face.color)] = face.color
            file.write("usemtl material" + __strColor(face.color) + "\n")
        faceString = "f"

        if weldVertices:
            for p in face.vertices:
                ptuple = (p.x,p.y,p.z)
                if ptuple in vertices:
                    faceString += " " + str(vertices[ptuple])
                else:
                    vertexCount += 1
                    faceString += " "+str(vertexCount)
                    vertices[ptuple] = vertexCount
                    file.write("v " + str(p.x) + " " + str(p.y) + " " + str(p.z) + "\n")
        else:
            for p in face.vertices:
                vertexCount += 1
                faceString += " " + str(vertexCount)
                file.write("v " + str(p.x) + " " + str(p.y) + " " + str(p.z) + "\n")

        faceString += "\n"
        file.write(faceString)
    file.close()

    if exportColors:
        for mat in materials.values():
            fileMTL.write("newmtl material" + __strColor(mat) + "\n")
            fileMTL.write("Kd " + str(mat[0]) + " " + str(mat[1]) + " " + str(mat[2]) + "\n")
        fileMTL.close()
