import colorsys as colorsys
import mola.analysis as analysis

__grayscale = False;

def getColorRGB(hue):
	if __grayscale:
		return (hue,hue,hue,1)
	else:
		hue = __map(hue,0.0,1.0,0.0,0.8) #limit hue red-red to red-magenta
		col = colorsys.hsv_to_rgb(hue,1,1)
		return (col[0],col[1],col[2],1)

def __getColorRgb(hue):
	if __grayscale:
		return (hue,hue,hue,1)
	else:
		hue = __map(hue,0.0,1.0,0.0,0.8) #limit hue red-red to red-magenta
		col = colorsys.hsv_to_rgb(hue,1,1)
		return (col[0],col[1],col[2],1)

def colorFacesByFunction(faces,faceFunction):
	"""
	Assigns a color to all the faces by face-function which has to return a float value for a face as argument,
	from smallest (red) to biggest (purple).
	"""
	values = []
	for face in faces:
		values.append(faceFunction(face))
	valueMin = min(values)
	valueMax = max(values)
	for i, face in enumerate(faces):
		h = __map(values[i],valueMin,valueMax,0.0,1.0)
		face.color = __getColorRgb(h)

def colorFacesByCurvature(faces):
	"""
	Assigns a color to all the faces by curvature (require topological meshinformation),
	from smallest (red) to biggest (purple).
	"""
	colorFacesByFunction(faces,analysis.getFaceCurvature)

def colorFacesByArea(faces):
	"""
	Assigns a color to all the faces by area,
	from smallest (red) to biggest (purple).
	"""
	colorFacesByFunction(faces,analysis.getFaceArea)

def colorFacesByPerimeter(faces):
	"""
	Assigns a color to all the faces by perimeter,
	from smallest (red) to biggest (purple).
	"""
	colorFacesByFunction(faces,analysis.getFacePerimeter)

def colorFacesByCompactness(faces):
	"""
	Assigns a color to all the faces by compactness (area/perimeter),
	from smallest (red) to biggest (purple).
	"""
	colorFacesByFunction(faces,analysis.getFaceCompactness)

def colorFacesByVerticality(faces):
	"""
	Assigns a color to all the faces by verticality,
	from smallest (red) to biggest (purple).
	"""
	colorFacesByFunction(faces,analysis.getFaceVerticality)

def __map(value, fromMin, fromMax, toMin, toMax):
	return toMin + ((toMax - toMin) / (fromMax - fromMin)) * (value - fromMin)

def grayscale(boolean):
	global __grayscale
	__grayscale = boolean
