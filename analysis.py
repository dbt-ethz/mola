import math as _math
import mola.vec as _vec

def __determinant(a,b,c,d,e,f,g,h,i):
	return (a * e * i - a * f * h - b * d * i + b * f * g + c * d * h - c * e * g)

def __getTriangleArea3D(a,b,c):
	return __getTriangleArea3DCoords(a.x,a.y,a.z,b.x,b.y,b.z,c.x,c.y,c.z)

def __getTriangleArea3DCoords(xa,ya,za,xb,yb,zb,xc,yc,zc):
	return 0.5 * _math.sqrt(_math.pow(__determinant(xa, xb, xc, ya, yb, yc, 1, 1, 1), 2) + _math.pow(__determinant(ya, yb, yc, za, zb, zc, 1, 1, 1), 2) + _math.pow(__determinant(za, zb, zc, xa, xb, xc, 1, 1, 1), 2))

def getFaceCompactness(face):
	return analysis.getFaceArea(face)/analysis.getFacePerimeter(face)

def getFaceArea(face):
    """
    Returns the area of a face, for quads that of two triangles.

    Arguments:
    ----------
    face : mola.core.Face
        The face to be measured
    """
	if(len(face.vertices) == 3):
		return __getTriangleArea3D(face.vertices[0],face.vertices[1],face.vertices[2])
	else:
		return __getTriangleArea3D(face.vertices[0],face.vertices[1],face.vertices[2]) + __getTriangleArea3D(face.vertices[2],face.vertices[3],face.vertices[0])

def getFacePerimeter(face):
    """
    Returns the perimeter of a face as the sum of all the edges' lengths.

    Arguments:
    ----------
    face : mola.core.Face
        The face to be measured
    """
	sum = 0;
	for i in range(len(face.vertices)):
		v1 = face.vertices[i]
		v2 = face.vertices[(i+1)%len(face.vertices)]
		sum += _vec.VectorDistance(v1,v2)
	return sum

def getFaceVerticality(face):
    """
    Returns the verticality of a face as the angle between ??.

    Arguments:
    ----------
    face : mola.core.Face
        The face to be measured
    """
	normal = _vec.VectorNormalFromVertices(face.vertices)
	return _math.atan2(normal.y * normal.y, normal.x * normal.x)
	#return _math.atan2(normal[1] * normal[1], normal[0] * normal[0])

def getFaceCurvature(face):
	normal=_vec.VectorCenter(face.vertices)
	sumD=0
	vPrev=face.vertices[-1]
	for v in face.vertices:
		edge=v.getEdgeAdjacentToVertex(vPrev)
		nbFace=edge.face1
		if (edge.face1==face):
			nbFace=edge.face2
		nbNormal = _vec.VectorCenter(nbFace.vertices)
		sumD+=_vec.VectorDistance(nbNormal,normal)
		vPrev=v
	return sumD / len(face.vertices)
