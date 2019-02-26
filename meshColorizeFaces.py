import colorsys as _colorsys
import mola.meshAnalysis as _analysis

def __getColorRgb(hue):
	col = _colorsys.hsv_to_rgb(hue,1,1)
	return (col[0],col[1],col[2],1)

def mapValuesToColor(values):
	valueMin = min(values)
	valueMax = max(values)
	colors=[]
	for v in values:
		h = __map(v,valueMin,valueMax,0.0,1.0)
		colors.append(__getColorRgb(h))
	return colors

def colorFacesByArea(faces):
	values = []
	for face in faces:
		values.append(_analysis.getFaceArea(face))
	valueMin = min(values)
	valueMax = max(values)
	for i, face in enumerate(faces):
		h = __map(values[i],valueMin,valueMax,0.0,1.0)
		face.color = __getColorRgb(h)

def colorFacesByPerimeter(faces):
	values = []
	for face in faces:
		values.append(_analysis.getFacePerimeter(face))
	valueMin = min(values)
	valueMax = max(values)
	for i , face in enumerate(faces):
		h = __map(values[i],valueMin,valueMax,0.0,1.0)
		face.color = __getColorRgb(h)

def colorFacesByVerticality(faces):
	values = []
	for face in faces:
		values.append(_analysis.getFaceVerticality(face))
	valueMin = min(values)
	valueMax = max(values)
	for i , face in enumerate(faces):
		h = __map(values[i],valueMin,valueMax,0.0,1.0)
		face.color = __getColorRgb(h)

def __map(value, fromMin, fromMax, toMin, toMax):
	return toMin + ((toMax - toMin) / (fromMax - fromMin)) * (value - fromMin)


