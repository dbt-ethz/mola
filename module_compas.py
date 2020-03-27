#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Conversion tools between mola and COMPAS."""
from compas.datastructures import Mesh as CMesh

import mola

__author__ = ['Benjamin Dillenburger', 'Demetris Shammas', 'Mathias Bernhard']
__copyright__ = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__ = 'MIT License'
__email__ = ['<dbt@arch.ethz.ch>']


def _get_subset_of_attrs(cls, attrs_to_ignore):
    """Get subset of a class' attributes by defining attributes to remove.

    Parameters
    ----------
    cls : :class:`object`
        Class to get subset of attributes from.
    attrs_to_ignore : :class:`list` of :class:`str`
        Attributes to remove from full set of attributes.

    Returns
    -------
    :class:`list` of :class:`str`
    """
    all_attrs = cls().Face().__dir__.keys()

    return [attr for attr in all_attrs if attr not in attrs_to_ignore]


def mesh_from_compas_mesh(cmesh):
    """Convert a compas mesh to a mola mesh.

    Parameters
    ----------
    cmesh : :class:`mola.Mesh`
        Mesh to convert.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
    """
    mesh = mola.Mesh()

    # Get face attributes not derived from mesh geometry
    geo_derived_attrs = ["vertices"]
    face_non_geo_attrs = _get_subset_of_attrs(mola.Face, geo_derived_attrs)

    # Get vertex attributes not derived from mesh geometry
    geo_derived_attrs = ["x", "y", "z", "edges"]
    vertex_non_geo_attrs = _get_subset_of_attrs(mola.Vertex, geo_derived_attrs)

    v_dict = {}

    for vkey in cmesh.vertices():
        x, y, z = cmesh.vertex_coordinates(vkey)

        # get mola compatible attributes if set
        v_attrs = {}
        for attr in vertex_non_geo_attrs:
            try:
                v_attrs.update({attr: cmesh.vertex_attribute(vkey, attr)})
            except KeyError:
                pass

        vert = mola.Vertex(x, y, z)

        # set mola vertex attributes
        for key in v_attrs:
            if v_attrs[key]:
                setattr(vert, key, v_attrs[key])

        mesh.vertices.append(vert)
        v_dict.update({vkey: vert})

    for fkey in cmesh.faces():
        vkeys = cmesh.face_vertices(fkey)

        # get mola face attributes
        f_attrs = {}
        for attr in face_non_geo_attrs:
            try:
                f_attrs.update({attr: cmesh.face_attribute(fkey, attr)})
            except KeyError:
                pass

        face_verts = []
        for vkey in vkeys:
            face_verts.append(v_dict[vkey])

        face = mola.Face(vertices=face_verts)

        # set mola face attributes
        for key in f_attrs:
            if f_attrs[key]:
                setattr(face, key, f_attrs[key])

        mesh.faces.append(face)

    mesh.update_topology()

    return mesh


def mesh_to_compas_mesh(mesh):
    """Convert a mola mesh to a compas mesh.

    Parameters
    ----------
    mesh : :class:`mola.Mesh`
        Mesh to convert.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
    """
    mesh.update_topology()

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
