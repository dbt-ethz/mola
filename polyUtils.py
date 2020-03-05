from mola import vecUtils
import math

def subdivideCatmull2D(pts):
    newNodes = []
    for i in range(len(pts)):
        a = pts[i]
        newNodes.append(Vertex(a.x,a.y,a.z))
        b = pts[(i + 1) % len(pts)]
        center = vecUtils.vertex_add(a, b)
        newNodes.append(vecUtils.vertex_scale(center,0.5))
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
        average = Vertex(0,0,0)
        average = vecUtils.vertex_add(average,a)
        average = vecUtils.vertex_add(average,b)
        average = vecUtils.vertex_add(average,b)
        average = vecUtils.vertex_add(average,c)
        average = vecUtils.vertex_divide(average,4.0)
        newNodes2.append(average)
    return newNodes2

def normalEdge2DNonUnified(vprev,v):
    vec1 = vecUtils.vertex_subtract(v, vprev)
    return vecUtils.vertex_rotate_2D_90(vec1)

def normalEdge2D(vprev,v):
    vec1 = vecUtils.vertex_subtract(v, vprev)
    vec1 = vecUtils.vertex_unitize(vec1)
    return vecUtils.vertex_rotate_2D_90(vec1)

def normalVertex2D(vprev,v,vnext):
    vec1 = vecUtils.vertex_subtract(v, vprev)
    vec1 = vecUtils.vertex_unitize(vec1)
    vec2 = vecUtils.vertex_subtract(vnext, v)
    vec2 = vecUtils.vertex_unitize(vec2)
    n = vecUtils.vertex_add(vec1, vec2)
    n = vecUtils.vertex_scale(n, 0.5)
    n = vecUtils.vertex_rotate_2D_90(n)
    #t=n.x
    #n.x=-n.y
    #n.y=t
    return n

def constructCircle(radius,segments,z=0):
    vertices = []
    deltaAngle = math.pi * 2.0 / segments
    for i in range(segments):
        cAngle = i * deltaAngle
        vertices.append(Vertex(math.cos(cAngle) * radius, math.sin(cAngle) * radius, z))
    return vertices
