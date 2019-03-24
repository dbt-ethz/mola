from mola.core import *
import mola.vec as vec
import math

def subdivideCatmull2D(pts):
    newNodes=[]
    for i in range(len(pts)):
        a=pts[i]
        newNodes.append(Vertex(a.x,a.y,a.z))
        b=pts[(i+1)%len(pts)]
        center=vec.add(a, b)
        newNodes.append(vec.scale(center,0.5))
    newNodes2=[]
    for i in range(len(newNodes)):
        iPrev=i-1
        if iPrev<0:
            iPrev=len(newNodes)-1
        iNext=i+1
        if iNext>=len(newNodes):
            iNext=0
        a=newNodes[iPrev]
        b=newNodes[i]
        c=newNodes[iNext]
        average=Vertex(0,0,0)
        average=vec.add(average,a)
        average=vec.add(average,b)
        average=vec.add(average,b)
        average=vec.add(average,c)
        average=vec.divide(average,4.0)
        newNodes2.append(average)
    return newNodes2

def normalEdge2DNonUnified(vprev,v):
    vec1=vec.subtract(v,vprev)
    return vec.rot2D90(vec1)

def normalEdge2D(vprev,v):
    vec1=vec.subtract(v,vprev)
    vec1=vec.unitize(vec1)
    return vec.rot2D90(vec1)

def normalVertex2D(vprev,v,vnext):
    vec1=vec.subtract(v,vprev)
    vec1=vec.unitize(vec1)
    vec2=vec.subtract(vnext,v)
    vec2=vec.unitize(vec1)
    n=vec.add(vec1,vec2)
    n=vec.scale(n,0.5)
    t=n.x
    n.x=-n.y
    n.y=t
    return n

def constructCircle(radius,segments,z=0):
    vertices=[]
    deltaAngle=math.pi*2.0/segments
    for i in range(segments):
        cAngle=i*deltaAngle
        vertices.append(Vertex(math.cos(cAngle)*radius,math.sin(cAngle)*radius,z))
    return vertices
