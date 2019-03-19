import math as _math
import mola.vec as _vec

# def areaTriangle(v0,v1,v2):
#     d1 = distance(v0, v1)
#     d2 = distance(v1, v2)
#     d3 = distance(v2, v0)
#     s = (d1+d2+d3)/2.0
#     a = _math.sqrt(s*(s-d1)*(s-d2)*(s-d3))
#     return a
def area(face):
	"""
	Returns the area of a face, for quads that of two triangles.

	Arguments:
	----------
	face : mola.core.Face
			The face to be measured
	"""
	if(len(face.vertices) == 3):
		return areaTriangle3D(face.vertices[0],face.vertices[1],face.vertices[2])
	else:
		return areaTriangle3D(face.vertices[0],face.vertices[1],face.vertices[2]) + __getTriangleArea3D(face.vertices[2],face.vertices[3],face.vertices[0])

def areaFromVertices(vertices):
    if len(vertices) == 3:
        return areaTriangle(vertices[0],vertices[1],vertices[2])
    elif len(vertices) == 4:
        a1 = areaTriangle3D(vertices[0],vertices[1],vertices[2])
        a2 = areaTriangle3D(vertices[2],vertices[3],vertices[0])
        return a1+a2

def areaTriangle3D(a,b,c):
	return areaTriangle3DCoords(a.x,a.y,a.z,b.x,b.y,b.z,c.x,c.y,c.z)

def areaTriangle3DCoords(xa,ya,za,xb,yb,zb,xc,yc,zc):
	return 0.5 * _math.sqrt(_math.pow(__determinant(xa, xb, xc, ya, yb, yc, 1, 1, 1), 2) + _math.pow(__determinant(ya, yb, yc, za, zb, zc, 1, 1, 1), 2) + _math.pow(__determinant(za, zb, zc, xa, xb, xc, 1, 1, 1), 2))

def __determinant(a,b,c,d,e,f,g,h,i):
	return (a * e * i - a * f * h - b * d * i + b * f * g + c * d * h - c * e * g)

def compactness(face):
	"""
	Returns the compactness of a face as the ratio between area and perimeter.

	Arguments:
	----------
	face : mola.core.Face
			The face to be measured
	"""
	return area(face)/perimeter(face)


def perimeter(face):
	"""
	Returns the perimeter of a face as the sum of all the edges' lengths.

	Arguments:
	----------
	face : mola.core.Face
			The face to be measured
	"""
	sum = 0
	for i in range(len(face.vertices)):
		v1 = face.vertices[i]
		v2 = face.vertices[(i+1)%len(face.vertices)]
		sum += _vec.distance(v1,v2)
	return sum

def angleOnXYPlane(face):
	"""
	Returns the verticality of a face as the angle between ??.

	Arguments:
	----------
	face : mola.core.Face
			The face to be measured
	"""
	normal = _vec.normalFromVertices(face.vertices)
	return _math.atan2(normal.y,normal.x )

def angleToXYPlane(f):
	"""
	Returns angle between normal from face and normal from face projected to XY Plane

	Arguments:
	----------
	face : mola.core.Face
			The face to be measured
	"""
    n = _vec.normalFromVertices(f.vertices)
    nXY = Vertex(n.x, n.y, 0.0)
    return _vec.angle(n, nXY)

def curvature(face):
	normal=_vec.normalFromVertices(face.vertices)
	sumD=0
	vPrev=face.vertices[-1]
	num_faces = 0
	for v in face.vertices:
		edge=v.getEdgeAdjacentToVertex(vPrev)
		if edge is None:
			return 0
		nbFace=edge.face1
		if (edge.face1==face):
			nbFace=edge.face2
			if nbFace is None:
				return 0
		num_faces += 1
		nbNormal = _vec.normalFromVertices(nbFace.vertices)
		sumD+=_vec.distance(nbNormal,normal)
		vPrev=v
	num_faces = max(1,num_faces)
	return sumD / num_faces

def center(vertices):
    # return the average of all boundarypoints
    n = len(vertices)
    cx = sum([v.x for v in vertices])/n
    cy = sum([v.y for v in vertices])/n
    cz = sum([v.z for v in vertices])/n
    return _Vertex(cx,cy,cz)

def centerFromLine(v1,v2):
    return _Vertex((v1.x+v2.x)/2,(v1.y+v2.y)/2,(v1.z+v2.z)/2)

def normal(face):
	return _vec.normal(face.vertices[0],face.vertices[1],face.vertices[2])

def normalFromVertices(vertices):
    return _vec.normal(vertices[0],vertices[1],vertices[2])
    # if len(vertices)==3:
    #     return VectorNormal(vertices[0],vertices[1],vertices[2])
    # elif len(vertices)==4:
    #     n1 = VectorNormal(vertices[0],vertices[1],vertices[2])
    #     n2 = VectorNormal(vertices[2],vertices[3],vertices[0])
    # there there is an error. planar surfaces will have identical normals. angle calculation fails?
    #     angle = VectorAngle(n1,n2)
    #     if(angle>_math.pi-0.01):
    #         n2 = VectorScale(n2,-1)
    #         sum = VectorAdd(n1,n2)
    #         sum = VectorScale(sum, 0.5)
    #         sum = VectorUnitize(sum)
    #         return sum
