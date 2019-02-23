def displayLines2D(lines):
    code=beginDraw2D()
    for line in lines:
        code+="line("+str(line.v1.x)+","+str(line.v1.y)+str(line.v2.x)+","+str(line.v2.y)+");"
    code+=endDraw2D()
    return code

def displayFaces2D(faces):
    code=beginDraw2D()
    for face in faces:
        code+="beginShape();"
        for v in face.vertices:
            code+="vertex("+str(v.x)+","+str(v.y)+");"
        code+="endShape();"
    code+=endDraw2D()
    return code

def beginDraw2D():
    return '''
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/0.6.0/p5.js"></script>
<script>
new p5();
createCanvas(1024, 768);
'''

def endDraw2D():
    return '''
    </script>
    '''
