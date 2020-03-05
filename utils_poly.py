from mola.core_vertex import Vertex
from mola import utils_vertex
import math

def subdivide_catmull_2d(vertices):
    newNodes = []
    for i in range(len(vertices)):
        a = vertices[i]
        newNodes.append(Vertex(a.x,a.y,a.z))
        b = vertices[(i + 1) % len(vertices)]
        center = utils_vertex.vertex_add(a, b)
        newNodes.append(utils_vertex.vertex_scale(center,0.5))
    newNodes2 = []
    for i in range(len(newNodes)):
        iPrev = i - 1
        if iPrev < 0:
            iPrev = len(newNodes) - 1
        iNext = i + 1
        if iNext >= len(newNodes):
            iNext = 0
        a = newNodes[iPrev]
        b = newNodes[i]
        c = newNodes[iNext]
        average = Vertex()
        # [average.add(v) for v in [a,b,b,c]]
        average.add(a)
        average.add(b)
        average.add(b)
        average.add(c)
        average.divide(4.0)
        # average = utils_vertex.vertex_add(average,a)
        # average = utils_vertex.vertex_add(average,b)
        # average = utils_vertex.vertex_add(average,b)
        # average = utils_vertex.vertex_add(average,c)
        # average /= 4
        # average = utils_vertex.vertex_divide(average,4.0)
        newNodes2.append(average)
    return newNodes2

def normal_edge_2d_non_unified(vprev, v):
    vec1 = utils_vertex.vertex_subtract(v, vprev)
    return utils_vertex.vertex_rotate_2D_90(vec1)

def normal_edge_2d(vprev, v):
    vec1 = utils_vertex.vertex_subtract(v, vprev)
    vec1 = utils_vertex.vertex_unitize(vec1)
    return utils_vertex.vertex_rotate_2D_90(vec1)

def normal_vertex_2d(vprev, v, vnext):
    vec1 = utils_vertex.vertex_subtract(v, vprev)
    vec1 = utils_vertex.vertex_unitize(vec1)
    vec2 = utils_vertex.vertex_subtract(vnext, v)
    vec2 = utils_vertex.vertex_unitize(vec2)
    n = utils_vertex.vertex_add(vec1, vec2)
    n = utils_vertex.vertex_scale(n, 0.5)
    n = utils_vertex.vertex_rotate_2D_90(n)
    #t=n.x
    #n.x=-n.y
    #n.y=t
    return n

def construct_circle(radius, segments, z=0):
    vertices = []
    deltaAngle = math.pi * 2.0 / segments
    for i in range(segments):
        cAngle = i * deltaAngle
        vertices.append(Vertex(math.cos(cAngle) * radius, math.sin(cAngle) * radius, z))
    return vertices
