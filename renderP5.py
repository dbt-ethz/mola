def displayLines(lines):
    for l in lines:
        line(l.v1.x,l.v1.y,l.v2.x,l.v2.y)

def displayMesh(mesh):
    return display(mesh.faces)

def createLinesShape(lines):
    shape = createShape(LINES)
    for l in lines:
        shape.line(l.v1.x,l.v1.y,l.v2.x,l.v2.y)
    return shape

def createMeshShape(mesh):
    shape = createShape(GROUP)
    trishape = createShape()
    trishape.beginShape(TRIANGLES)
    quadshape = createShape()
    quadshape.beginShape(QUADS)
    for f in faces:
        cShape = trishape
        if len(f.vertices) == 4:
            cShape = quadshape
        cShape.fill(f.color[0]*255,f.color[1]*255,f.color[2]*255)
        for v in f.vertices:
            cShape.vertex(v.x,v.y,v.z)
        trishape.endShape()
        quadshape.endShape()
        shape.addChild(trishape)
        shape.addChild(quadshape)
    return shape

# split between triangles, quads and more..
def display(faces):
    beginShape(QUADS)
    for f in faces:
        if len(f.vertices)==4:
            fill(f.color[0]*255,f.color[1]*255,f.color[2]*255)
            for v in f.vertices:
                vertex(v.x,v.y,v.z)
    endShape()
    beginShape(TRIANGLES)
    for f in faces:
        if len(f.vertices)==3:
            fill(f.color[0]*255,f.color[1]*255,f.color[2]*255)
            for v in f.vertices:
                vertex(v.x,v.y,v.z)
    endShape()
    for f in faces:
        if len(f.vertices)>4:
            fill(f.color[0]*255,f.color[1]*255,f.color[2]*255)
            beginShape()
            for v in f.vertices:
                vertex(v.x,v.y,v.z)
            endShape(CLOSE)

# def display(faces):
#     for f in faces:
#         fill(f.color[0]*255,f.color[1]*255,f.color[2]*255)
#         beginShape()
#         for v in f.vertices:
#             vertex(v.x,v.y,v.z)
#         endShape(CLOSE)

def display2D(faces):
    for f in faces:
        beginShape()
        for v in f.vertices:
            vertex(v.x,v.y)
        endShape(CLOSE)
