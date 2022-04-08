from __future__ import division
from ast import Raise
from asyncio import proactor_events
from hashlib import new
from logging import raiseExceptions
import re
import string
import sys
import os
import random
import operator
from tokenize import group
from webbrowser import get
from .core_mesh import Mesh
from .utils_face import face_normal
import mola


def filter(attr, relate, arg):
    ops = {'>': operator.gt,
           '<': operator.lt,
           '>=': operator.ge,
           '<=': operator.le,
           '==': operator.eq}

    return lambda f: ops[relate](getattr(f, attr), arg)


def selector(faces, filter, ratio):
    selected = []
    unselected_by_ratio = []
    unselected_by_filer = []
    for f in faces:
        if filter(f):
            if random.random() < ratio:
                selected.append(f)
            else:
                unselected_by_ratio.append(f)
        else:
            unselected_by_filer.append(f)
    
    return selected, unselected_by_ratio, unselected_by_filer


class Engine(Mesh):
    """
    """
    def __init__(self):
        super(Engine, self).__init__()
        self.groups = [
            0, "block", "block_s", "block_ss", "block_sss", "plaza", "plot", "road", "construct_up", 
            "construct_side", "construct_down", "roof", "roof_s", "roof_f", "wall", "panel", "facade",
            "frame", "glass", "brick"
        ]
        self.successor_rules = {
            "block":{
                "divide_to": ["block"],
                "undivided": "plaza",
                "group_children": "group_by_default",
            },
            "plot":{
                "divide_to": ["road", "construct_up"],
                "undivided": "plaza",
                "group_children": "group_by_index",
            },
            "construct_up":{
                "divide_to": ["construct_up", "construct_down", "construct_side"],
                "undivided": "roof",
                "group_children": "group_by_orientation",
            },
            "construct_side":{
                "divide_to": ["construct_up", "construct_down", "construct_side"],
                "undivided": "wall",
                "group_children": "group_by_orientation",
            },
            "wall":{
                "divide_to": ["panel"],
                "undivided": "facade",
                "group_children": "group_by_default",
            },
            "panel":{
                "divide_to": ["frame", "glass"],
                "undivided": "brick",
                "group_children": "group_by_index",
            },
            "roof":{
                "divide_to": ["roof"],
                "undivided": "roof",
                "group_children": "group_by_default",
            },
        }

    @classmethod
    def from_mesh(cls, mesh):
        "convert a mola Mesh to a mola Engine"
        engine = cls()
        engine.faces = mesh.faces

        return engine

    def color_by_group(self, faces):
        values = [self.groups.index(f.group) for f in faces]
        mola.color_faces_by_values(faces, values)

    def group_by_index(self, faces, child_a, child_b):
        "assign group value child_a and child_b to a set of faces according to their index"
        for f in faces[:-1]:
            f.group = child_a
        faces[-1].group = child_b

    def group_by_orientation(self, faces, up, down, side):
        "assign group value up, side and down to a set of faces according to each face's orientation"
        for f in faces:
            normal_z = mola.face_normal(f).z
            if normal_z > 0.1:
                f.group = up
            elif normal_z < -0.1:
                f.group = down
            else:
                f.group = side

    def group_by_default(self, faces, child):
        for f in faces:
            f.group = child

    def subdivide(self, faces, my_filter, ratio, subd_method, *args, group=False):
        selected_faces =[] 
        unselected_by_ratio = []
        unselected_by_filter = []
        new_faces = []
        for f in faces:
            if my_filter(f):
                if random.random() < ratio:
                    selected_faces.append(f)
                else:
                    unselected_by_ratio.append(f)
            else:   
                unselected_by_filter.append(f)

        if selected_faces != []:
            subdivide_method = getattr(mola, "subdivide_" + subd_method)

            if group:
                parent_group = selected_faces[0].group
                group_children = self.successor_rules[parent_group]["group_children"]
                group_method = getattr(self, group_children)
                group_args = self.successor_rules[parent_group]["divide_to"]
                undivide_group = self.successor_rules[parent_group]["undivided"]
            else:
                group_method = None
                group_args = []
                undivide_group = None

            if subd_method[:4] == "mesh":  # mesh subidivision
                new_mesh = mola.Mesh()
                for f in selected_faces:
                    new_mesh.faces.append(f)

                new_mesh.update_topology()
                new_mesh = subdivide_method(new_mesh, *args)
                if group:
                    group_method(new_mesh.faces, *group_args)
                new_faces.extend(new_mesh.faces)
            
            elif subd_method[:4] == "face":  # face subidivision
                for f in selected_faces:
                    subdivided_faces = subdivide_method(f, *args)
                    if group:
                        group_method(subdivided_faces, *group_args)
                    new_faces.extend(subdivided_faces)
            else:
                raise Exception("subdivision method couldnt be found!!")
        
        # add back unselected faces by ratio and by filter
        if unselected_by_ratio != []:
            for f in unselected_by_ratio:
                if group:
                    f.group = undivide_group
                new_faces.append(f)
            
        new_faces.extend(unselected_by_filter)

        if group:
            self.color_by_group(new_faces)
        return new_faces
    
    def change_face_group(self, faces, group_before, group_after):
        for f in faces:
            if group_before == "all":
                f.group = group_after
            else:
                if f.group == group_before:
                    f.group = group_after
