def Vertex:
    def __init__(x=0,y=0,z=0):
        self.x=x
        self.y=y
        self.z=z

def Face:
    def __init__(self,vertices=[]):
        self.vertices = vertices
        self.color=(1,1,1,1)

def Edge:
    def __init__(v1,v2):
        self.v1=v1
        self.v2=v2

def Mesh:
    def __init__(vertices=[],faces=[],edges=[]):
        self.vertices=vertices
        self.faces=faces
        self.edges=edges
