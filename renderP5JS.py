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

def textSize(size):
    global p5code
    p5code+="textSize("+str(size)+");"

def text(text,x,y):
    global p5code
    p5code+="text("+str(text)+","+str(x)+","+str(y)+");"

def noStroke():
    global p5code
    p5code+="noStroke();"

def noFill():
    global p5code
    p5code+="noFill();"

def strokeWeight(weight):
    global p5code
    p5code+="strokeWeight("+str(weight)+");"

def colorMode(mode,max):
    global p5code
    p5code+="colorMode("+str(mode)+","+str(max)+");"

def stroke(r,g,b):
    global p5code
    p5code+="stroke("+str(r)+","+str(g)+","+str(b)+");"

def fill(r,g=None,b=None):
    global p5code
    if isinstance(r,list) or isinstance(r,tuple):
        p5code+="fill("+str(r[0])+","+str(r[1])+","+str(r[2])+");"
    else:
        p5code+="fill("+str(r)+","+str(g)+","+str(b)+");"

def line(x1,y1,x2,y2):
    global p5code
    p5code+="line("+str(x1)+","+str(y1)+","+str(x2)+","+str(y2)+");"

def ellipse(x,y,w,h):
    global p5code
    p5code+="ellipse("+str(x)+","+str(y)+","+str(w)+","+str(h)+");"

def circle(x,y,radius):
    global p5code
    p5code+="ellipse("+str(x)+","+str(y)+","+str(radius)+","+str(radius)+");"

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

def background(r,g,b):
    global p5code
    p5code+="background("+str(r)+","+str(g)+","+str(b)+");"

def beginDraw():
    global p5code
    p5code=_beginDraw2D()
    p5code+="rectMode(CORNERS);"

def endDraw():
    global p5code
    p5code+=_endDraw2D()
    return p5code
