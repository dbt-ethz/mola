from __future__ import division
import random
import operator
from .core_mesh import Mesh
from .utils_face import face_normal
import mola


def color_by_group(faces):
    groups = []
    for f in faces:
        if not (f.group in groups):
            groups.append(f.group)

    values = [groups.index(f.group) for f in faces]
    mola.color_faces_by_values(faces, values)



# def filter(attr, relate, arg):
#     ops = {'>': operator.gt,
#            '<': operator.lt,
#            '>=': operator.ge,
#            '<=': operator.le,
#            '==': operator.eq}

#     return lambda f: ops[relate](getattr(f, attr), arg)


# def selector(faces, filter, ratio):
#     selected = []
#     unselected_by_ratio = []
#     unselected_by_filer = []
#     for f in faces:
#         if filter(f):
#             if random.random() < ratio:
#                 selected.append(f)
#             else:
#                 unselected_by_ratio.append(f)
#         else:
#             unselected_by_filer.append(f)
    
#     return selected, unselected_by_ratio, unselected_by_filer


class Engine(Mesh):
    """A mesh class contains severial subdivide, group and color methods.

    Attributes
    ----------
    """
    def __init__(self):
        super(Engine, self).__init__()
        self._rule = None
        self._ratio = 1.0
        self._filter = None
        self._labeling = None
    #     self.successor_rules = {
    #         "block":{
    #             "divide_to": ["block"],
    #             "undivided": "plaza",
    #             "group_children": "group_by_default",
    #         },
    #         "plot":{
    #             "divide_to": ["road", "construct_up"],
    #             "undivided": "plaza",
    #             "group_children": "group_by_index",
    #         },
    #         "construct_up":{
    #             "divide_to": ["construct_up", "construct_down", "construct_side"],
    #             "undivided": "roof",
    #             "group_children": "group_by_orientation",
    #         },
    #         "construct_side":{
    #             "divide_to": ["construct_up", "construct_down", "construct_side"],
    #             "undivided": "wall",
    #             "group_children": "group_by_orientation",
    #         },
    #         "wall":{
    #             "divide_to": ["panel"],
    #             "undivided": "facade",
    #             "group_children": "group_by_default",
    #         },
    #         "panel":{
    #             "divide_to": ["frame", "glass"],
    #             "undivided": "brick",
    #             "group_children": "group_by_index",
    #         },
    #         "roof":{
    #             "divide_to": ["roof"],
    #             "undivided": "roof",
    #             "group_children": "group_by_default",
    #         },
    #     }

    @classmethod
    def from_mesh(cls, mesh):
        "convert a mola Mesh to a mola Engine"
        engine = cls()
        engine.faces = mesh.faces

        return engine

    # @staticmethod
    # def groups():
    #     _groups = [
    #         0, "block", "block_s", "block_ss", "block_sss", "plaza", "plot", "road", "construct_up", 
    #         "construct_side", "construct_down", "roof", "roof_s", "roof_f", "wall", "panel", "facade",
    #         "frame", "glass", "brick"
    #     ]
    #     return _groups
    @property
    def rule(self):
        return self._rule
    @rule.setter
    def rule(self, rule):
        self._rule = rule

    @property
    def filter(self):
        return self._filter
    @filter.setter
    def filter(self, filter):
        self._filter = filter

    @property
    def ratio(self):
        return self._ratio
    @ratio.setter
    def ratio(self, ratio):
        self._ratio = ratio
    
    @property
    def labeling(self):
        return self._labeling
    @labeling.setter
    def labeling(self, labeling):
        self._labeling = labeling

    @staticmethod
    def group_by_index(faces, group_a, group_b):
        "assign group value child_a and child_b to a set of faces according to their index"
        for f in faces[:-1]:
            f.group = group_a
        faces[-1].group = group_b

    @staticmethod
    def group_by_orientation(faces, up, down, side):
        "assign group value up, side and down to a set of faces according to each face's orientation"
        for f in faces:
            normal_z = mola.face_normal(f).z
            if normal_z > 0.1:
                f.group = up
            elif normal_z < -0.1:
                f.group = down
            else:
                f.group = side

    @staticmethod
    def group_by_default(faces, child):
        for f in faces:
            f.group = child


    @staticmethod
    def color_by_group(faces):
        groups = []
        for f in faces:
            if not (f.group in groups):
                groups.append(f.group)

        values = [groups.index(f.group) for f in faces]
        mola.color_faces_by_values(faces, values)

    @staticmethod
    def subdivide(faces, filter, rule, labeling, ratio=1.0):
        """
        Subdivide a group of faces according to customized rules

        Attributes:
        ----------
        faces : list of mola.core.Face
            The faces to be split
        filter : a customized filter, returning faces which fit the condition
        rule :  a customized mola.subdivide_face_xxxx() method with arguments
        labeling: a custmoized funtion to assign values to mola.Face.group for each face
        ratio(opt) : float
            ratio of filtered faces to be subdivided

        Return:
        -------
        faces : list of mola.core.Face 

        Example:
        --------
        >>> from mola import engine_subdivide_face
        >>> ...
        """
        to_be_divided_faces = []
        undivided_faces = []
        unselected_faces = []
        devidied_faces = []

        for f in faces:
            if filter(f):
                if random.random() < ratio:
                    to_be_divided_faces.append(f)
                else:
                    undivided_faces.append(f)
            else:
                unselected_faces.append(f)

        for f in to_be_divided_faces:
            devidied_faces.append(rule(f))

        labeling(devidied_faces, undivided_faces)

        devidied_faces = [face for faces in devidied_faces for face in faces]

        return devidied_faces + undivided_faces + unselected_faces

    def subdivide(self, iteration=1):
        for _ in range(iteration):
            to_be_divided_faces = []
            undivided_faces = []
            unselected_faces = []
            devidied_faces = []

            for f in self.faces:
                if self.filter(f):
                    if random.random() < self.ratio:
                        to_be_divided_faces.append(f)
                    else:
                        undivided_faces.append(f)
                else:
                    unselected_faces.append(f)

            for f in to_be_divided_faces:
                devidied_faces.append(self.rule(f))

            self.labeling(devidied_faces, undivided_faces)

            devidied_faces = [face for faces in devidied_faces for face in faces]

            self.faces = devidied_faces + undivided_faces + unselected_faces
