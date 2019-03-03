def displayLines(lines):
  for l in lines:
    line(l.v1.x,l.v1.y,l.v2.x,l.v2.y)
    
def displayMesh(mesh):
    return display(mesh.faces)
    
def display(faces):
  for f in faces:
    beginShape()
    for v in f.vertices:
      vertex(v.x,v.y,v.z)
    endShape(CLOSE)

def display2D(faces):
  for f in faces:
    beginShape()
    for v in f.vertices:
      vertex(v.x,v.y)
    endShape(CLOSE)
