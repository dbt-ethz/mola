import colorsys as _colorsys
import mola.meshAnalysis as _analysis

__grayscale = False;

def __getColorRgb(hue):
	if __grayscale:
		return (hue,hue,hue,1)
	else:
		col = _colorsys.hsv_to_rgb(hue,1,1)
		return (col[0],col[1],col[2],1)

def mapValuesToColor(values):
	valueMin = min(values)
	valueMax = max(values)
	colors=[]
	for v in values:
		h = __map(v,valueMin,valueMax,0.0,0.8)
		colors.append(__getColorRgb(h))
	return colors

def colorFacesByArea(faces):
	"""
	Assigns a color to all the faces by area,
	from smallest (red) to biggest (purple).
	"""
	values = []
	for face in faces:
		values.append(_analysis.getFaceArea(face))
	valueMin = min(values)
	valueMax = max(values)
	for i, face in enumerate(faces):
		h = __map(values[i],valueMin,valueMax,0.0,0.8)
		face.color = __getColorRgb(h)

def colorFacesByPerimeter(faces):
	"""
	Assigns a color to all the faces by perimeter,
	from smallest (red) to biggest (purple).
	"""
	values = []
	for face in faces:
		values.append(_analysis.getFacePerimeter(face))
	valueMin = min(values)
	valueMax = max(values)
	for i , face in enumerate(faces):
		h = __map(values[i],valueMin,valueMax,0.0,0.8)
		face.color = __getColorRgb(h)

def colorFacesByCompactness(faces):
	"""
	Assigns a color to all the faces by compactness (area/perimeter),
	from smallest (red) to biggest (purple).
	"""
	values = []
	for face in faces:
		a = _analysis.getFaceArea(face)
		p = _analysis.getFacePerimeter(face)
		values.append(a/p)
	valueMin = min(values)
	valueMax = max(values)
	for i , face in enumerate(faces):
		h = __map(values[i],valueMin,valueMax,0.0,0.8)
		face.color = __getColorRgb(h)

def colorFacesByVerticality(faces):
	"""
	Assigns a color to all the faces by verticality,
	from smallest (red) to biggest (purple).
	"""
	values = []
	for face in faces:
		values.append(_analysis.getFaceVerticality(face))
	valueMin = min(values)
	valueMax = max(values)
	for i , face in enumerate(faces):
		h = __map(values[i],valueMin,valueMax,0.0,0.8)
		face.color = __getColorRgb(h)

def __map(value, fromMin, fromMax, toMin, toMax):
	return toMin + ((toMax - toMin) / (fromMax - fromMin)) * (value - fromMin)

def grayscale(boolean):
	global __grayscale
	__grayscale = boolean
