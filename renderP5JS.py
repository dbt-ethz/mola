p5code=""

def displayLines2D(lines):
    code=_beginDraw2D()
    for line in lines:
        code+="line("+str(line.v1.x)+","+str(line.v1.y)+","+str(line.v2.x)+","+str(line.v2.y)+");"
    code+=_endDraw2D()
    return code

def displayFaces2D(faces):
    code=_beginDraw2D()
    for face in faces:
        if face.color!=None:
            code=="fill("+str(face.color[0])+","+str(face.color[1])+","+str(face.color[2])+");"
        code+="beginShape();"
        for v in face.vertices:
            code+="vertex("+str(v.x)+","+str(v.y)+");"
        code+="endShape();"
    code+=_endDraw2D()
    return code

def _beginDraw2D():
    return '''<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/0.6.0/p5.js"></script><script>new p5();createCanvas(1024, 768);'''

def _endDraw2D():
    return '''</script>'''

def noStroke():
    global p5code
    p5code+="noStroke();"

def noFill():
    global p5code
    p5code+="noFill();"

def strokeWeight(weight):
    global p5code
    p5code+="strokeWeight("+str(weight)+");"

def stroke(r,g,b):
    global p5code
    p5code+="stroke("+str(r)+","+str(g)+","+str(b)+");"

def fill(r,g,b):
    global p5code
    p5code+="fill("+str(r)+","+str(g)+","+str(b)+");"

def line(x1,y1,x2,y2):
    global p5code
    p5code+="line("+str(x1)+","+str(y1)+","+str(x2)+","+str(y2)+");"

def rect(x1,y1,x2,y2):
    global p5code
    p5code+="rect("+str(x1)+","+str(y1)+","+str(x2)+","+str(y2)+");"

def beginShape():
    global p5code
    p5code+="beginShape();"

def endShape():
    global p5code
    p5code+="endShape();"

def vertex(x,y):
    global p5code
    p5code+="vertex("+str(x)+","+str(y)+");"

def beginDraw():
    global p5code
    p5code=_beginDraw2D()

def endDraw():
    global p5code
    p5code+=_endDraw2D()
    return p5code
