#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import math
from mola.core_mesh import Mesh
from mola.core_vertex import Vertex
from mola.core_face import Face

class GridManager:
    """
    A `GridManager` is taking care of getting and setting values and
    retrieving neighbors in an orthogonal grid of either 2 or 3 dimension.

    Attributes
    ----------
    nx, ny, nz : int
        The number of elements in x,y and z direction.
    """
    def __init__(self, nx, ny, nz=1):
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.length = nx * ny * nz
        self.nyz = ny * nz

    def get_index(self, x, y, z=0):
        """
        returns the value at position x,y,z
        """
        return x * self.nyz + y * self.nz + z

    def get_x(self,index):
        """
        returns the X coordinate of a specific index
        """
        return index // self.nyz

    def get_y(self,index):
        """
        returns the Y coordinate of a specific index
        """
        return (index // self.nz) % self.ny

    def get_z(self,index):
        """
        returns the Z coordinate of a specific index
        """
        return index % self.nz

    def get_neighbors_hex_2d(self,index,continuous=False):
        """
        returns the 6 neighbor indices of a cell in a hexagonal grid
        set `continuous` to `True` to get torus topology (left edge stitched to right and top to bottom)
        """
        nbs = []
        x = self.get_x(index)
        y = self.get_y(index)
        if not continuous:
            if x < self.nx - 1:
                nbs.append(self.get_index(x + 1, y))
            if x > 0:
                nbs.append(self.get_index(x - 1, y))
            if y > 0:
                nbs.append(self.get_index(x, y - 1))
            if y < self.ny - 1:
                nbs.append(self.get_index(x, y + 1))
            if y % 2 == 0:
                if x < self.nx - 1 and y < self.ny - 1:
                    nbs.append(self.get_index(x + 1, y + 1))
                if x < self.nx - 1 and y > 0:
                    nbs.append(self.get_index(x + 1, y - 1))
            else:
                if x > 0 and y < self.ny - 1:
                    nbs.append(self.get_index(x - 1, y + 1))
                if x > 0 and y > 0:
                    nbs.append(self.get_index(x - 1, y - 1))
        else:
            xNext = x + 1 if x < self.nx - 1 else 0
            xPrev = x - 1 if x > 0 else self.nx - 1
            yNext = y + 1 if y < self.ny - 1 else 0
            yPrev = y - 1 if y > 0 else self.ny - 1
            nbs.append(self.get_index(xNext, y))
            nbs.append(self.get_index(xPrev, y))
            nbs.append(self.get_index(x, yPrev))
            nbs.append(self.get_index(x, yNext))
            if y % 2 == 0:
                nbs.append(self.get_index(xNext, yNext))
                nbs.append(self.get_index(xNext, yPrev))
            else:
                nbs.append(self.get_index(xPrev, yNext))
                nbs.append(self.get_index(xPrev, yPrev))
        return nbs

    def get_neighbors_2d(self,index,nbs8=False,continuous=False):
        """
        returns the neighbor indices of a cell in an orthogonal grid
        set `nbs8` to `True` to get 8 neighbors, default is 4
        set `continuous` to `True` to get torus topology (left edge stitched to right and top to bottom)
        """
        nbs = []
        x = self.get_x(index)
        y = self.get_y(index)
        if not continuous:
            if x < self.nx - 1:
                nbs.append(self.get_index(x + 1, y))
            if nbs8:
                if x < self.nx - 1 and y < self.ny - 1:
                    nbs.append(self.get_index(x + 1, y + 1))
            if y < self.ny - 1:
                nbs.append(self.get_index(x, y + 1))
            if nbs8:
                if x > 0 and y < self.ny - 1:
                    nbs.append(self.get_index(x - 1, y + 1))
            if x > 0:
                nbs.append(self.get_index(x - 1, y))
            if nbs8:
                if x > 0 and y > 0:
                    nbs.append(self.get_index(x - 1, y - 1))
            if y > 0:
                nbs.append(self.get_index(x, y - 1))
            if nbs8:
                if x < self.nx - 1 and y > 0:
                    nbs.append(self.get_index(x + 1, y - 1))
        else:
            xPrev = x - 1 if x > 0 else self.nx - 1
            xNext = x + 1 if x < self.nx - 1 else 0
            yPrev = y - 1 if y > 0 else self.ny - 1
            yNext = y + 1 if y < self.ny - 1 else 0
            nbs.append(self.get_index(xNext, y))
            if nbs8:
                nbs.append(self.get_index(xNext, yNext))
            nbs.append(self.get_index(x, yNext))
            if nbs8:
                nbs.append(self.get_index(xPrev, yNext))
            nbs.append(self.get_index(xPrev, y))
            if nbs8:
                nbs.append(self.get_index(xPrev, yPrev))
            nbs.append(self.get_index(x, yPrev))
            if nbs8:
                nbs.append(self.get_index(xNext, yPrev))
        return nbs

    def get_neighbors_3d(self, index, mode=3, continuous=False):
        nbs = []
        x = self.get_x(index)
        y = self.get_y(index)
        z = self.get_z(index)

        # mode: neighbourhood type
        # 1 :  6 nbs, shared face
        # 2 : 18 nbs, shared face or edge
        # 3 : 26 nbs, shared face, edge or vertex
        if not mode:
            mode==3
        if mode<1:
            mode==1
        if mode>3:
            mode==3

        # precalculate distances
        # dists = [1, math.sqrt(2), math.sqrt(3)]

        # create a list of directions with x,y and z offsets
        directions = []
        for i in range(-1,2):
            for j in range(-1,2):
                for k in range(-1,2):
                    l = [i,j,k]
                    s = sum([abs(v) for v in l])
                    # check for neighbourhood type
                    if s > 0 and s <= mode:
                        directions.append(l)

        for d in directions:
            ex = x + d[0]
            ey = y + d[1]
            ez = z + d[2]
            if continuous:
                ex = ex % self.nx
                ey = ey % self.ny
                ez = ez % self.nz
            if 0 <= ex < self.nx and 0 <= ey < self.ny and 0 <= ez < self.nz:
                nbs.append(self.get_index(ex,ey,ez))

        return nbs

class Grid(GridManager):
    def __init__(self, nx, ny, nz=1, values=None, scale_to_canvas=False):
        super().__init__(nx, ny, nz)
        # self.nx = nx
        # self.ny = ny
        # self.nz = nz
        # self.nyz = ny * nz
        self.scale_to_canvas = scale_to_canvas;
        if values is None:
            self.values = [0] * nx * ny * nz
        else:
            self.values = values

    def set_value_at_xyz(self, value, x, y, z=0):
        self.values[self.get_index(x, y, z)] = value

    def get_value_at_xyz(self, x, y, z=0):
        return self.values[self.get_index(x, y, z)]

    def set_value_at_index(self, value, index):
        self.values[index] = value

    def get_value_at_index(self, index):
        return self.values[index]

    def shortest_path(self, startindex, endindex, obstaclevalue):
        # TODO
        return []

    def quad_mesh(self, functionIn, functionOut):
        faces = []
        for x in range(self.nx):
            for y in range(self.ny):
                for z in range(self.nz):
                    index=self.get_index(x,y,z)
                    if functionIn(self.values[index]):
                        # (x,y) (x1,y) (x1,y1) (x,y1)
                        if x == self.nx - 1 or functionOut(self.get_value_at_xyz(x + 1, y, z)):
                            v1 = Vertex(x + 1, y, z)
                            v2 = Vertex(x + 1, y + 1, z)
                            v3 = Vertex(x + 1, y + 1, z + 1)
                            v4 = Vertex(x + 1, y, z + 1)
                            faces.append(Face([v1, v2, v3, v4]))
                        if x == 0 or functionOut(self.get_value_at_xyz(x-1,y,z)):
                            v1 = Vertex(x, y + 1, z)
                            v2 = Vertex(x, y, z)
                            v3 = Vertex(x, y, z + 1)
                            v4 = Vertex(x, y + 1, z + 1)
                            faces.append(Face([v1, v2, v3, v4]))
                        if y == self.ny - 1 or functionOut(self.get_value_at_xyz(x, y + 1, z)):
                            v1 = Vertex(x + 1, y + 1, z)
                            v2 = Vertex(x, y + 1, z)
                            v3 = Vertex(x, y + 1, z + 1)
                            v4 = Vertex(x + 1, y + 1, z + 1)
                            faces.append(Face([v1, v2, v3, v4]))
                        if y == 0 or functionOut(self.get_value_at_xyz(x, y - 1, z)):
                            v1 = Vertex(x, y, z)
                            v2 = Vertex(x + 1, y, z)
                            v3 = Vertex(x + 1, y, z + 1)
                            v4 = Vertex(x, y, z + 1)
                            faces.append(Face([v1, v2, v3, v4]))
                        if z==self.nz-1 or functionOut(self.get_value_at_xyz(x, y, z + 1)):
                            v1 = Vertex(x, y, z + 1)
                            v2 = Vertex(x + 1, y, z + 1)
                            v3 = Vertex(x + 1, y + 1, z + 1)
                            v4 = Vertex(x, y + 1, z + 1)
                            faces.append(Face([v1, v2, v3, v4]))
                        if z == 0 or functionOut(self.get_value_at_xyz(x, y, z - 1)):
                            v1 = Vertex(x, y + 1, z)
                            v2 = Vertex(x + 1, y + 1, z)
                            v3 = Vertex(x + 1, y, z)
                            v4 = Vertex(x, y, z)
                            faces.append(Face([v1, v2, v3, v4]))
        mesh = Mesh()
        mesh.faces = faces
        mesh.update_topology()
        if (self.scale_to_canvas):
            mesh.translate(-self.nx/2.0,-self.ny/2.0,-self.nz/2.0)
            sc = 20.0/max(self.nx,self.ny)
            mesh.scale(sc,sc,sc)
        return mesh

class HexGrid(Grid):
    def __init__(self, nx, ny, nz=1, values=None):
        super().__init__(nx, ny, nz, values)
        # self.ny = nx
        # self.ny = ny
        # self.nz = nz
        # self.nyz = ny * nz
        # if values == None:
        #     self.values = [0] * nx * ny * nz
        self.dimy = math.sqrt(3) * 0.5

    def get_position(self, x, y, z=0):
        return [x + (y % 2) * 0.5, y * self.dimy, z]
