#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

p5code=""

def display_lines2D(lines):
    global p5code
    for line in lines:
        p5code += "line(" + str(line.v1.x) + "," + str(line.v1.y) + "," + str(line.v2.x) + "," + str(line.v2.y) + ");"

def display_faces2D(faces):
    global p5code
    for face in faces:
        if face.color != None:
            p5code += "fill("+str(face.color[0])+","+str(face.color[1])+","+str(face.color[2])+");"
        p5code += "beginShape();"
        for v in face.vertices:
            p5code += "vertex("+str(v.x)+","+str(v.y)+");"
        p5code += "endShape();"

def save_canvas(fileName):
    global p5code
    p5code+="saveCanvas(canvas,'"+fileName+"');"

def save_image(fileName):
    global p5code
    p5code+="save("+fileName+");"

def _begin2D(width=1024,height=768):
    return '''<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/0.6.0/p5.js"></script><script>new p5();var canvas = createCanvas('''+str(width)+","+str(height)+''');'''

def _end2D():
    return '''</script>'''

def text_size(size):
    global p5code
    p5code+="textSize("+str(size)+");"

def translate(x,y):
    global p5code
    p5code+="translate("+str(x)+","+str(y)+");"

def scale(x,y):
    global p5code
    p5code+="scale("+str(x)+","+str(y)+");"

def text(text,x,y):
    global p5code
    p5code+="text("+str(text)+","+str(x)+","+str(y)+");"

def no_stroke():
    global p5code
    p5code+="noStroke();"

def no_fill():
    global p5code
    p5code+="noFill();"

def stroke_weight(weight):
    global p5code
    p5code+="strokeWeight("+str(weight)+");"

def color_mode(mode,max):
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

def begin_shape():
    global p5code
    p5code+="beginShape();"

def end_shape():
    global p5code
    p5code+="endShape();"

def vertex(x,y):
    global p5code
    p5code+="vertex("+str(x)+","+str(y)+");"

def background(r,g,b):
    global p5code
    p5code+="background("+str(r)+","+str(g)+","+str(b)+");"

def begin_draw(width=1024,height=768):
    global p5code
    p5code=_begin2D(width,height)
    p5code+="rectMode(CORNERS);"

def end_draw():
    global p5code
    p5code+=_endDraw2D()
    return p5code

# helper function to get a drawing canvas inside the notebook
def whiteboard():
    from IPython.display import IFrame
    return IFrame('https://dbt.arch.ethz.ch/temp/canvas', width=800, height=500)
