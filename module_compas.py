#!/usr/bin/env python
# -*- coding: utf-8 -*-
from compas.datastructures import Mesh as CMesh

import mola

__author__ = ['Benjamin Dillenburger', 'Demetris Shammas', 'Mathias Bernhard']
__copyright__ = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__ = 'MIT License'
__email__ = ['<dbt@arch.ethz.ch>']


def mesh_from_compas_mesh(cmesh):
    """Convert a compas mesh to a mola mesh."""
    mesh = mola.Mesh()

    face_attrs = ["color", "groups"]
    vertex_attrs = ["fix, generation"]

    v_dict = {}

    for vkey in cmesh.vertices():
        x, y, z = cmesh.vertex_coordinates(vkey)

        # get mola compatible attributes if set
        v_attrs = {}
        for attr in vertex_attrs:
            try:
                v_attrs.update({attr: cmesh.vertex_attribute(vkey, attr)})
            except KeyError:
                pass

        vert = mola.Vertex(x, y, z)

        # set mola compatible attributes if set
        for key in v_attrs:
            if v_attrs[key]:
                setattr(vert, key, v_attrs[key])

        mesh.vertices.append(vert)
        v_dict.update({vkey: vert})

    for fkey in cmesh.faces():
        vkeys = cmesh.face_vertices(fkey)

        # get mola compatible attributes if set
        f_attrs = {}
        for attr in face_attrs:
            try:
                f_attrs.update({attr: cmesh.face_attribute(fkey, attr)})
            except KeyError:
                pass

        face_verts = []
        for vkey in vkeys:
            face_verts.append(v_dict[vkey])

        face = mola.Face(vertices=face_verts)

        # set mola compatible attributes if set
        for key in f_attrs:
            if f_attrs[key]:
                setattr(face, key, f_attrs[key])

        mesh.faces.append(face)

    for u, v in cmesh.edges():
        mesh.edges.append(mola.Edge(v_dict[u], v_dict[v]))

    return mesh


def mesh_to_compas_mesh(mesh):
    """Convert a mola mesh to a compas mesh."""
    cmesh = CMesh()

    for face in mesh.faces:
        idx = []
        dict_ = face.__dict__
        vertices = dict_.pop("vertices")
        for vertex in vertices:
            dict_ = vertex.__dict__

            x, y, z = dict_.pop("x"), dict_.pop("y"), dict_.pop("z")

            # store v attributes in attr dict
            i = cmesh.add_vertex(x=x, y=y, z=z, attr_dict=dict_)

            idx.append(i)

        # store f attributes in attr dict
        cmesh.add_face(idx, attr_dict=dict_)

    return cmesh
