#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']


try:
    from Queue import PriorityQueue
except ImportError:
    from queue import PriorityQueue
from mola.core_grid import GridManager


class Graph:
    ''' basic graph class. edge-weighted graphs should implement different weightFunction'''
    def __init__(self, neighbours, gm=None):
        self.neighbours = neighbours
        self.weight_function = lambda a, b : 1

    def get_neighbours(self, u):
        return self.neighbours[u]

    def size(self):
        return len(self.neighbours)

    def weight(self, index1, index2):
        return self.weight_function(index1, index2)

    @classmethod
    def from_grid_2d(cls, nx, ny, nbs8=False, continuous=False):
        gm = GridManager(nx,ny)
        neighbours = [0] * gm.length
        for i in range(gm.length):
            neighbours[i] = gm.get_neighbors_2d(i, nbs8, continuous)
        return cls(neighbours)

    @classmethod
    def from_hex_grid_2d(cls, nx, ny,continuous=False):
        gm = GridManager(nx, ny)
        neighbours = [0] * gm.length
        for i in range(gm.length):
            neighbours[i] = gm.get_neighbors_hex_2d(i, continuous)
        return cls(neighbours)

    @classmethod
    def from_grid_3d(cls, nx, ny, nz, mode=3, continuous=False):
        gm = GridManager(nx, ny, nz)
        neighbours = [0] * gm.length
        for i in range(gm.length):
            neighbours[i] = gm.get_neighbors_3d(i, mode, continuous)
        return cls(neighbours)

    @classmethod
    def from_mesh_faces(cls, mesh):
        faceIds = {}
        neighbours = [0] * len(mesh.faces)
        for index, face in enumerate(mesh.faces):
            faceIds[face] = index
        for index, face in enumerate(mesh.faces):
            nbs = []
            v0 = face.vertices[-1]
            for v1 in face.vertices:
                nbFace = mesh.getFaceAdjacentToVertices(v1, v0)
                nbs.append(faceIds[nbFace])
                v0 = v1
            neighbours[index] = nbs
        return cls(neighbours)

    def from_mesh_edges(self,mesh):
        pass

    def from_mesh_vertices(self,mesh):
        pass

#http://www.iti.fh-flensburg.de/lang/algorithmen/graph/dijkstra.htm
#http://www.iti.fh-flensburg.de/lang/algorithmen/graph/shortest-paths.htm
#http://en.wikipedia.org/wiki/Dijkstra_algorithm
class GraphAnalyser:
    """
    works with graphs which provide 3 methods: size(), getNeighbours(), and weight()
    this class stores all distances in order to allow a fast calculation of path to predefined starting points
    usage: construct a Graphanalyser
    1. compute distance to a list of starting points
    2. getShortest Path from end point to those starting point
    """
    def __init__(self,graph):
        self.n = graph.size()
        self.graph = graph
        self.dist = [1000000] * self.n
        self.pred = [-1] * self.n

    def compute_distance_to_nodes(self,startIndexes):
        pq = PriorityQueue()
        for i in startIndexes:
            self.dist[i] = 0
            pq.put((0,i))
        while not pq.empty():
            u = pq.get()[1]
            nbs = self.graph.get_neighbours(u)
            for v in nbs:
                d = self.dist[u] + self.graph.weight(u,v)
                if d < self.dist[v]:
                    self.dist[v] = d
                    self.pred[v] = u
                    pq.put((d, v))

    def shortest_path(self,v):
        p = []
        while v != -1:
            p.append(v)
            v = self.pred[v]
        return p

    def compute_traffic_and_centrality(self,nodes):
        n = self.n
        self.traffic = [0] * n
        self.centrality = [0] * n
        for i in range(len(nodes) - 1):
            startI = nodes[i]
            self.dist = [100000] * n
            self.pred = [-1] * n
            self.compute_distance_to_nodes([startI])
            for j in range(i,len(nodes)):
                endI = nodes[j]
                if endI != startI:
                    self.centrality[startI] += self.dist[endI]
                    self.centrality[endI] += self.dist[endI]
                    path = self.shortest_path(endI)
                    for ii in path:
                        cI = path[ii]
                        self.traffic[cI] += 1
