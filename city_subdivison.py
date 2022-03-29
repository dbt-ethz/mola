from __future__ import division
from ast import Raise
from asyncio import proactor_events
from logging import raiseExceptions
import re
import string
import sys
import os
import random
from tokenize import group
from webbrowser import get
from .core_mesh import Mesh
from .utils_face import face_normal
import mola

class Engine:
    def __init__(self, mesh):
        self._mesh = None
        self.mesh = mesh
        self.rules = []
        self.color = {
            "block": (),
            "block_s": (),
            "block_ss": (),
            "plot": (),
            "road": (),
            "construct_up": (1, 0, 0, 1),
            "construct_side": (0, 1, 0, 1),
            "construct_down": (0, 0, 0, 1),
            "wall": (0, 1, 0, 1),
            "panel": (),
            "roof": (1, 0, 0, 1),
            "glass": (0.1, 0.1, 0.1, 0),
            "road": (0, 0, 0, 1),
            "others": (0, 0, 0, 1)
        }
        self.groups = [
            0, "block", "block_s", "block_ss", "block_sss", "plaza", "plot", "road", "construct_up", 
            "construct_side", "construct_down", "roof", "roof_s", "roof_f", "wall", "panel", "facade",
            "frame", "glass", "brick"
        ]
        self.groups_block = {
            "block", "block_s", "block_ss", "block_sss"
        }
        self.groups_building = {
            "plot", "road", "construct_up", "construct_side", "construct_down",
        }
        self.groups_facade = {
            "roof", "wall", "panel", "facade", "frame", "glass", "brick", "roof_s"
        }
        self.parent_children_rule = {
            "block":{
                "group_children": "group_by_default",
                "group_children_into": ["block_s"],
                "undivided": "plaza"
            },
            "block_s":{
                "group_children": "group_by_default",
                "group_children_into": ["block_ss"],
                "undivided": "plaza"
            },
            "block_ss":{
                "group_children": "group_by_default",
                "group_children_into": ["block_sss"],
                "undivided": "plaza"
            },
            "block_sss":{
                "group_children": "group_by_default",
                "group_children_into": ["plot"],
                "undivided": "plaza"
            },
            "plot":{
                "group_children": "group_by_index",
                "group_children_into": ["road", "construct_up"],
                "undivided": "plaza"
            },
            "construct_up":{
                "group_children": "group_by_orientation",
                "group_children_into": ["construct_up", "construct_down", "construct_side"],
                "undivided": "roof"
            },
            "construct_side":{
                "group_children": "group_by_orientation",
                "group_children_into": ["construct_up", "construct_down", "construct_side"],
                "undivided": "wall"
            },
            "wall":{
                "group_children": "group_by_default",
                "group_children_into": ["panel"],
                "undivided": "facade"
            },
            "panel":{
                "group_children": "group_by_index",
                "group_children_into": ["frame", "glass"],
                "undivided": "brick"
            },
            "roof":{
                "group_children": "group_by_default",
                "group_children_into": ["roof_s"],
                "undivided": "roof_f"
            },
            "roof_s":{
                "group_children": "group_by_default",
                "group_children_into": ["roof_f"],
                "undivided": "roof_f"
            }
        }

    @property
    def mesh(self):
        return self._mesh
    
    @mesh.setter
    def mesh(self, value):
        if type(value) != Mesh:
            raise Exception("input is not a mola mesh!!")

        self._mesh = value
        # for f in self._mesh.faces:
        #     f.group = "block"

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

    def subidivide_by_group(self, parentgroup, faces, ratio, method, *args):
        group_children = self.parent_children_rule[parentgroup]["group_children"]
        group_children = getattr(self, group_children)
        group_args = self.parent_children_rule[parentgroup]["group_children_into"]
        subdivide_method = getattr(mola, "subdivide_" + method)
        undivide_group = self.parent_children_rule[parentgroup]["undivided"]

        new_faces = []

        if method[:4] == "mesh":  # mesh subidivision
            new_mesh = mola.Mesh()
            for f in faces:
                if random.random() <= ratio:
                    new_mesh.faces.append(f)
                else:
                    f.group = undivide_group
                    new_faces.append(f)
            new_mesh.update_topology()
            new_mesh = subdivide_method(new_mesh, *args)
            group_children(new_mesh.faces, *group_args)
            new_faces.extend(new_mesh.faces)
        
        elif method[:4] == "face":  # face subdivision
            for f in faces:
                if random.random() <= ratio:
                    subdivided_faces = subdivide_method(f, *args)
                    group_children(subdivided_faces, *group_args)
                    new_faces.extend(subdivided_faces)
                else:
                    f.group = undivide_group
                    new_faces.append(f)
        else:
            raise Exception("subdivision method couldnt found!!")

        return new_faces

    def subdivide(self, rules):
        new_mesh = mola.Mesh()
        remaining_faces = self.mesh.faces
        for rule in rules:
            select = rule[0]["select"]
            ratio = rule[0]["ratio"]
            subd = rule[1]["subd"]
            arg = rule[1]["arg"]

            selected_faces = []
            unseleted_faces = []
            for f in remaining_faces:
                if f.group == select:
                    selected_faces.append(f)
                else:
                    unseleted_faces.append(f)

            new_faces = self.subidivide_by_group(select, selected_faces, ratio , subd, *arg)
            new_mesh.faces.extend(new_faces)
            remaining_faces = unseleted_faces
        new_mesh.faces.extend(unseleted_faces)
        self._mesh = new_mesh

        self.color_by_group()
        return self._mesh

    def subdivide_block(self, iter=1):
        for f in self._mesh.faces:
            if f.group == 0:
                f.group = "block"
        rules_block = []
        for rule in self.rules:
            if rule[0]["select"] in self.groups_block:
                rules_block.append(rule)
        
        for _ in range(iter):
            self.subdivide(rules_block)

    def subdivide_building(self, iter=1):
        for f in self._mesh.faces:
            if f.group[:5] == "block": 
                f.group = "plot"
        rules_building = []
        for rule in self.rules:
            if rule[0]["select"] in self.groups_building:
                rules_building.append(rule)
        
        for _ in range(iter):
            self.subdivide(rules_building)

    def subdivide_facade(self, iter=1):
        for f in self._mesh.faces:
            if f.group == "construct_side":
                f.group = "wall"
            elif f.group =="construct_up":
                f.group = "roof"
        rules_facade = []
        for rule in self.rules:
            if rule[0]["select"] in self.groups_facade:
                rules_facade.append(rule)
        
        for _ in range(iter):
            self.subdivide(rules_facade)

    def color_by_group(self):
        # for f in self._mesh.faces:
        #     f.color = self.color[f.group]
        values = [self.groups.index(f.group) for f in self._mesh.faces]
        mola.color_faces_by_values(self._mesh.faces, values)