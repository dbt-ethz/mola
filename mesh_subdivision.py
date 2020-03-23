from __future__ import division

#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

from mola.core_mesh import Mesh
from mola.core_vertex import Vertex
from mola.core_face import Face
from mola import utils_face
from mola import utils_vertex
import copy
import math

def _collect_new_faces(mesh):
    newMesh=Mesh()
    for face in mesh.faces:
        v1 = face.vertices[-2]
        v2 = face.vertices[-1]
        for v3 in face.vertices:
            edge1 = mesh.edge_adjacent_to_vertices(v1,v2)
            edge2 = mesh.edge_adjacent_to_vertices(v2,v3)
            if (edge1 != None) and (edge2!= None):
                newFace = Face([edge1.vertex, v2.vertex, edge2.vertex, face.vertex])
                newFace.color = face.color
                newFace.group = face.group
                newMesh.faces.append(newFace)
            v1 = v2
            v2 = v3
    newMesh.update_topology()
    return newMesh

def offset(mesh,offset=1,doclose=True):
    newMesh=Mesh()
    # calculate vertex normals
    for vertex in mesh.vertices:
        vertex.vertex = Vertex(0,0,0)
        vertex.nfaces = 0
    for face in mesh.faces:
        normal = utils_face.face_normal(face)
        for vertex in face.vertices:
            vertex.vertex.add(normal)
            vertex.nfaces += 1
    for vertex in mesh.vertices:
        vertex.vertex.scale(offset / vertex.nfaces)
        vertex.vertex.add(vertex)
    # create faces
    for face in mesh.faces:
        offsetVertices = []
        for vertex in face.vertices:
            offsetVertices.append(vertex.vertex)
        offsetVertices.reverse()
        newFace = Face(offsetVertices)
        newMesh.faces.append(newFace)
        newMesh.faces.append(face)
    # create sides
    if doclose:
        for edge in mesh.edges:
            if edge.face1 == None or edge.face2 == None:
                offsetVertices = [edge.v1, edge.v2, edge.v2.vertex, edge.v1.vertex]
                if edge.face2 == None:
                    offsetVertices.reverse()
                newFace = Face(offsetVertices)
                newMesh.faces.append(newFace)
    newMesh.update_topology()
    return newMesh

def subdivide_mesh(mesh,values=[]):
    for face in mesh.faces:
        face.vertex=utils_face.center(face)
    for edge in mesh.edges:
        edge.vertex = edge.center()
    for vertex in mesh.vertices:
        vertex.vertex = Vertex(vertex.x,vertex.y,vertex.z)
    if len(values)>0:
        _translate_face_vertices(mesh,values)
    return _collect_new_faces(mesh)

def _catmullVertices(mesh):
    for face in mesh.faces:
        face.vertex = face.center()

    for edge in mesh.edges:
        if edge.face1 == None or edge.face2 == None:
            edge.v1.fix = True
            edge.v2.fix = True
            edge.vertex = edge.center()
        else:
            vsum = Vertex()
            nElements = 2
            vsum = utils_vertex.vertex_add(vsum, edge.v1)
            vsum = utils_vertex.vertex_add(vsum, edge.v2)
            if edge.face1 != None:
                vsum = utils_vertex.vertex_add(vsum, edge.face1.vertex)
                nElements += 1
            if edge.face2 != None:
                vsum = utils_vertex.vertex_add(vsum, edge.face2.vertex)
                nElements += 1
            vsum = utils_vertex.vertex_divide(vsum, nElements)
            edge.vertex = vsum
        if edge.v1.fix and edge.v2.fix:
            edge.vertex.fix = True

    for vertex in mesh.vertices:
        if vertex.fix:
            vertex.vertex = copy.copy(vertex)
        else:
            averageFaces = Vertex()
            averageEdges = Vertex()
            nEdges = len(vertex.edges)

            for edge in vertex.edges:
                face = edge.face1
                if edge.v2 is vertex:
                    face = edge.face2
                if face != None:
                    averageFaces = utils_vertex.vertex_add(averageFaces, face.vertex)
                averageEdges=utils_vertex.vertex_add(averageEdges,edge.center())
            averageEdges = utils_vertex.vertex_scale(averageEdges, 2.0/nEdges)
            averageFaces = utils_vertex.vertex_scale(averageFaces, 1.0/nEdges)

            v = Vertex(vertex.x, vertex.y, vertex.z)
            v = utils_vertex.vertex_scale(v,nEdges-3)
            v = utils_vertex.vertex_add(v,averageFaces)
            v = utils_vertex.vertex_add(v,averageEdges)
            v = utils_vertex.vertex_scale(v,1.0/nEdges)
            vertex.vertex = v

def _translate_face_vertices(mesh,values):
    for face,value in zip(mesh.faces, values):
        normal=utils_face.face_normal(face)
        normal.scale(value)
        face.vertex.add(normal)

def subdivide_mesh_catmull(mesh, values=[]):
    _catmullVertices(mesh)
    if len(values)>0:
        _translate_face_vertices(mesh,values)
    return _collect_new_faces(mesh)

def subdivide_face_split_grid(face,nU,nV):
    """
    splits a triangle, quad or a rectangle into a regular grid
    """
    if len(face.vertices) > 4:
        print('too many vertices')
        return face

    if len(face.vertices) == 4:
        vsU1 = _vertices_between(face.vertices[0], face.vertices[1], nU)
        vsU2 = _vertices_between(face.vertices[3], face.vertices[2], nU)
        gridVertices = []
        for u in range(len(vsU1)):
            gridVertices.append(_vertices_between(vsU1[u], vsU2[u], nV))
        faces = []
        for u in range(len(vsU1) - 1):
            vs1 = gridVertices[u]
            vs2 = gridVertices[u + 1]
            for v in range(len(vs1) - 1):
                #f = Face([vs1[v], vs1[v + 1], vs2[v + 1], vs2[v]])
                f = Face([vs1[v], vs2[v], vs2[v + 1], vs1[v + 1]])
                utils_face.face_copy_properties(face, f)
                faces.append(f)
        return faces

    if len(face.vertices) == 3:
        vsU1 = _vertices_between(face.vertices[0], face.vertices[1], nU)
        vsU2 = _vertices_between(face.vertices[0], face.vertices[2], nU)
        gridVertices = []
        for u in range(1, len(vsU1)):
            gridVertices.append(_vertices_between(vsU1[u], vsU2[u], nV))
        faces = []
        # triangles
        v0 = face.vertices[0]
        vs1 = gridVertices[0]
        for v in range(len(vs1) - 1):
            f = Face([v0,vs1[v],vs1[v + 1]])
            utils_face.face_copy_properties(face, f)
            faces.append(f)
        for u in range(len(gridVertices) - 1):
            vs1 = gridVertices[u]
            vs2 = gridVertices[u + 1]
            for v in range(len(vs1) - 1):
                f = Face([vs1[v],vs1[v + 1], vs2[v + 1], vs2[v]])
                utils_face.face_copy_properties(face, f)
                faces.append(f)
        return faces

def _vertices_between(v1,v2,n):
    row = []
    deltaV = utils_vertex.vertex_subtract(v2, v1)
    deltaV = utils_vertex.vertex_divide(deltaV, n)
    for i in range(n):
        addV = utils_vertex.vertex_scale(deltaV, i)
        row.append(utils_vertex.vertex_add(addV, v1))
    row.append(v2)
    return row

def subdivide_face_split_rel_free_quad(face, indexEdge,  split1,  split2):
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

    indexEdge1 = (indexEdge + 1) % len(face.vertices)
    indexEdge2 = (indexEdge + 2) % len(face.vertices)
    indexEdge3 = (indexEdge + 3) % len(face.vertices)
    p1 = utils_vertex.vertex_between_rel(face.vertices[indexEdge], face.vertices[indexEdge1], split1)
    p2 = utils_vertex.vertex_between_rel(face.vertices[indexEdge2 ], face.vertices[indexEdge3], split2)
    faces = []
    if indexEdge == 0:
        f1 = Face([face.vertices[0], p1, p2, face.vertices[3]])
        f2 = Face([p1, face.vertices[1], face.vertices[2], p2])
        utils_face.face_copy_properties(face, f1)
        utils_face.face_copy_properties(face, f2)
        faces.extend([f1, f2])
    elif indexEdge == 1:
        f1 = Face([face.vertices[0], face.vertices[1], p1, p2])
        f2 = Face([p2, p1, face.vertices[2], face.vertices[3]])
        utils_face.face_copy_properties(face,f1)
        utils_face.face_copy_properties(face,f2)
        faces.extend([f1, f2])
    return faces

def subdivide_face_extrude(face, height=0.0, capBottom=False, capTop=True):
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
    normal=utils_face.face_normal(face)
    normal=utils_vertex.vertex_scale(normal,height)
    # calculate vertices
    new_vertices=[]
    for i in range(len(face.vertices)):
        new_vertices.append(utils_vertex.vertex_add(face.vertices[i], normal))
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
        new_faces.append(Face([v0,v1,v2,v3]))
    if capTop:
        new_faces.append(Face(new_vertices))
    for new_face in new_faces:
        utils_face.face_copy_properties(face,new_face)
    return new_faces

def subdivide_mesh_extrude_tapered(mesh,heights,fractions,doCaps):
    new_mesh = Mesh()
    for face,height,fraction,doCap in zip(mesh.faces,heights,fractions,doCaps):
        new_mesh.faces.extend(subdivide_face_extrude_tapered(face,height,fraction,doCap))
    new_mesh.update_topology()
    return new_mesh

def subdivide_face_extrude_tapered(face, height=0.0, fraction=0.5,doCap=True):
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
    center_vertex = utils_face.face_center(face)
    normal = utils_face.face_normal(face)
    scaled_normal = utils_vertex.vertex_scale(normal, height)

    # calculate new vertex positions
    new_vertices = []
    for i in range(len(face.vertices)):
        n1 = face.vertices[i]
        betw = utils_vertex.vertex_subtract(center_vertex, n1)
        betw = utils_vertex.vertex_scale(betw, fraction)
        nn = utils_vertex.vertex_add(n1, betw)
        nn = utils_vertex.vertex_add(nn, scaled_normal)
        new_vertices.append(nn)

    new_faces = []
    # create the quads along the edges
    num = len(face.vertices)
    for i in range(num):
        n1 = face.vertices[i]
        n2 = face.vertices[(i + 1) % num]
        n3 = new_vertices[(i + 1) % num]
        n4 = new_vertices[i]
        new_face = Face([n1,n2,n3,n4])
        new_faces.append(new_face)

    # create the closing cap face
    if doCap:
        cap_face = Face(new_vertices)
        new_faces.append(cap_face)

    for new_face in new_faces:
        utils_face.face_copy_properties(face,new_face)
    return new_faces

def subdivide_custom_triface_extrude_tapered_nonU(face, height=0.0, fraction=0.5,doCap=True):
    """
    Extrudes a triangular face tapered like a window by creating an
    offset face and quads between every original edge and the
    corresponding new edge. The vertices of the new edge which corresponds 
    to the shortest edge of the triangle are moved closer to the later,
    while preserving the offset from its other edges 

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

    center_vertex = utils_face.face_center(face)
    normal = utils_face.face_normal(face)
    scaled_normal = utils_vertex.vertex_scale(normal, height)

    minD = 9999999999999999
    for i in range(len(face.vertices)-1):
        n1 = face.vertices[i]
        for j in range(i+1,len(face.vertices)):

            n2 = face.vertices[j]
            d = (n2.x-n1.x)**2.0 + (n2.y - n1.y)**2.0 + (n2.z - n1.z)**2.0
            if d<minD:
                minD = d
                shortF_st = i
                shortF_end = j

    other = 3 - shortF_st - shortF_end
    n_other = face.vertices[other]
    betw_other = utils_vertex.vertex_subtract(center_vertex, n_other)
    betw_other = utils_vertex.vertex_scale(betw_other, fraction)
    nn_other = utils_vertex.vertex_add(n_other, betw_other)
    nn_other = utils_vertex.vertex_add(nn_other, scaled_normal)

    # calculate new vertex positions
    new_vertices = []
    for i in range(len(face.vertices)):
        n1 = face.vertices[i]
        betw = utils_vertex.vertex_subtract(center_vertex, n1)
        betw = utils_vertex.vertex_scale(betw, fraction)
        nn = utils_vertex.vertex_add(n1, betw)
        nn = utils_vertex.vertex_add(nn, scaled_normal) 

        if i==shortF_st or i==shortF_end:
            vec = utils_vertex.vertex_subtract(n1, nn_other)
            vec = utils_vertex.vertex_scale(vec, 0.25)
            nn = utils_vertex.vertex_add(nn, vec)

        new_vertices.append(nn)

    new_faces = []
    # create the quads along the edges
    num = len(face.vertices)
    for i in range(num):
        n1 = face.vertices[i]
        n2 = face.vertices[(i + 1) % num]
        n3 = new_vertices[(i + 1) % num]
        n4 = new_vertices[i]
        new_face = Face([n1,n2,n3,n4])
        new_faces.append(new_face)

    # create the closing cap face
    if doCap:
        cap_face = Face(new_vertices)
        new_faces.append(cap_face)

    for new_face in new_faces:
        utils_face.face_copy_properties(face,new_face)

    return new_faces

def subdivide_face_split_roof(face, height):
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
    normal = utils_face.face_normal(face)
    normal = utils_vertex.vertex_scale(normal,height)
    if len(face.vertices) == 4:
        ev1 = utils_vertex.vertex_center(face.vertices[0], face.vertices[1])
        ev1 = utils_vertex.vertex_add(ev1, normal)
        ev2 = utils_vertex.vertex_center(face.vertices[2], face.vertices[3])
        ev2 = utils_vertex.vertex_add(ev2, normal)

        faces.append(Face([face.vertices[0], face.vertices[1], ev1]))
        faces.append(Face([face.vertices[1], face.vertices[2], ev2, ev1]))
        faces.append(Face([face.vertices[2], face.vertices[3], ev2]))
        faces.append(Face([face.vertices[3], face.vertices[0], ev1, ev2]))

        for f in faces:
            utils_face.face_copy_properties(face,f)
        return faces

    elif len(face.vertices) == 3:
        ev1 = utils_vertex.vertex_center(face.vertices[0], face.vertices[1])
        ev1 = utils_vertex.vertex_add(ev1, normal)
        ev2 = utils_vertex.vertex_center(face.vertices[1], face.vertices[2])
        ev2 = utils_vertex.vertex_add(ev2, normal)

        faces.append(Face([face.vertices[0], face.vertices[1], ev1]))
        faces.append(Face([face.vertices[1], ev2, ev1]))
        faces.append(Face([face.vertices[1], face.vertices[2], ev2]))
        faces.append(Face([face.vertices[2], face.vertices[0], ev1, ev2]))

        for f in faces:
            utils_face.face_copy_properties(face, f)
        return faces
    return [face]

def subdivide_face_extrude_to_point(face, point):
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
        v2 = face.vertices[(i + 1) % numV]
        f = Face([v1, v2, point])
        utils_face.face_copy_properties(face, f)
        faces.append(f)
    return faces

def subdivide_face_extrude_to_point_center(face, height=0.0):
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
    normal = utils_face.face_normal(face)
    normal = utils_vertex.vertex_scale(normal,height)
    center = utils_face.face_center(face)
    center = utils_vertex.vertex_add(center,normal)
    return subdivide_face_extrude_to_point(face,center)

def subdivide_mesh_extrude_to_point_center(mesh,heights,doExtrudes):
    new_mesh = Mesh()
    for face,height,doExtrude in zip(mesh.faces,heights,doExtrudes):
        if doExtrude:
            new_mesh.faces.extend(subdivide_face_extrude_to_point_center(face,height))
        else:
            new_mesh.faces.append(face)
    new_mesh.update_topology()
    return new_mesh

def subdivide_face_offset_planar(face,offsets):
    newPts = []
    for i in range(len(face.vertices)):
        iP = i - 1
        if(iP < 0):
            iP = len(face.vertices)-1
        iN = (i + 1) % len(face.vertices)
        v0 = face.vertices[iP]
        v1 = face.vertices[i]
        v2 = face.vertices[iN]
        newPts.append(utils_vertex.vertex_offset_point(v0, v1, v2, offsets[iP], offsets[i]))
    f = Face(newPts)
    utils_face.face_copy_properties(face, f)
    return f

def subdivide_face_split_offset(face,offset):
    offsets = [offset] * len(face.vertices)
    return subdivide_face_split_offsets(face, offsets)

def subdivide_face_split_offsets(face,offsets):
    offsetFace = subdivide_face_offset_planar(face,offsets)
    nOffsetFaces = 0
    for o in offsets:
        if(abs(o) > 0):
            nOffsetFaces += 1
    faces = []
    for i in range(len(face.vertices)):
        if(abs(offsets[i]) > 0):
            i2 = (i + 1) % len(face.vertices)
            f = Face([face.vertices[i], face.vertices[i2], offsetFace.vertices[i2], offsetFace.vertices[i]])
            utils_face.face_copy_properties(face, f)
            faces.append(f)
    faces.append(offsetFace)
    for f in faces:
        if(utils_face.face_area(f) < 0):
            f.vertices.reverse()
    return faces

def subdivide_face_split_rel_multiple(face, direction, splits):
    sA = []
    sA.append(face.vertices[direction])
    lA = face.vertices[direction + 1]
    sB = []
    sB.append(face.vertices[direction + 3])
    lB = face.vertices[(direction + 2) % len(face.vertices)]

    for i in range(len(splits)):
        sA.append(utils_vertex.vertex_between_rel(sA[0], lA,splits[i]))
        sB.append(utils_vertex.vertex_between_rel(sB[0], lB,splits[i]))
    sA.append(lA)
    sB.append(lB)

    result = []
    for i in range(len(splits) + 1):
        if(dir == 1):
            f = Face([sB[i], sA[i], sA[i+1], sB[i+1]])
            utils_face.face_copy_properties(face, f)
            result.append(f)
        else:
            f = Face([sB[i], sB[i+1], sA[i+1], sA[i]])
            utils_face.face_copy_properties(face, f)
            result.append(f)
    return result

def subdivide_face_split_rel(face, direction, split):
    """
    Splits face in given direction.

    Arguments:
    ----------
    face : mola.core.Face
        The face to be split
    direction : integer (-1 or 0)
    split : float
        Position of the split relative to initial face points (0 to 1)
    """
    return subdivide_face_split_rel_multiple(face, direction, [split])

def subdivide_face_split_frame(face, w):
    """
    Creates an offset frame with quad corners. Works only with convex shapes.

    Arguments:
    ----------
    face : mola.core.Face
        The face to be split
    w : float
        The width of the offset frame
    """
    faces = []
    innerVertices = []
    for i in range(len(face.vertices)):
      if(i == 0):
        vp = face.vertices[len(face.vertices)-1]
      else:
        vp = face.vertices[i - 1]
      v = face.vertices[i]
      vn = face.vertices[(i + 1) % len(face.vertices)]
      vnn = face.vertices[(i + 2) % len(face.vertices)]

      th1 = utils_vertex.vertex_angle_triangle(vp,v,vn)
      th2 = utils_vertex.vertex_angle_triangle(v,vn,vnn)

      w1 = w / math.sin(th1)
      w2 = w / math.sin(th2)

      vs1 = _vertices_frame(v, vn, w1, w2)
      vs2 = _vertices_frame(_vertices_frame(vp, v, w1, w1)[2], _vertices_frame(vn, vnn, w2, w2)[1], w1, w2)
      innerVertices.append(vs2[1])
      f1 = Face([vs1[0], vs2[0], vs2[1], vs1[1]])
      utils_face.face_copy_properties(face, f1)
      f2 = Face([vs1[1], vs2[1], vs2[2], vs1[2]])
      utils_face.face_copy_properties(face, f2)
      faces.extend([f1, f2])
    fInner = Face(innerVertices)
    utils_face.face_copy_properties(face, fInner)
    faces.append(fInner)
    return faces

def _vertices_frame(v1,v2,w1,w2):
    p1 = utils_vertex.vertex_between_abs(v1, v2, w1)
    p2 = utils_vertex.vertex_between_abs(v2, v1, w2)
    return [v1, p1, p2, v2]
