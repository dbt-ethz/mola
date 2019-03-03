class Vertex:
    def __init__(self,x=0,y=0,z=0):
        self.x=x
        self.y=y
        self.z=z
        self.edges=[]

    def __str__(self):
        return ' '.join([str(v) for v in [self.x,self.y,self.z]])

class Face:
    def __init__(self,vertices=[]):
        self.vertices = vertices
        self.color=(1,1,1,1)

class Edge:
    def __init__(self,v1,v2):
        self.v1=v1
        self.v2=v2
        self.face1=None
        self.face2=None
        
    def getCenter(self):
        return Vertex((self.v2.x+self.v1.x)/2.0,(self.v2.y+self.v1.y)/2.0,(self.v2.z+self.v1.z)/2.0)

class Box:
    
    def __init__(self,x1=-float('inf'),y1=-float('inf'),z1=-float('inf'),x2=float('inf'),y2=float('inf'),z2=float('inf')):
        self.x1=x1
        self.y1=y1
        self.z1=z1
        self.x2=x2
        self.y2=y2
        self.z2=z2
        
    def getDimX(self):
        return self.x2-self.x1
    
    def getDimY(self):
        return self.y2-self.y1
    
    def getDimZ(self):
        return self.z2-self.z1
    
    def getCenterX(self):
        return (self.x2+self.x1)/2
    
    def getCenterY(self):
        return (self.y2-self.y1)/2
    
    def getCenterZ(self):
        return (self.z2-self.z1)/2
    
    def addPoint(self,x,y,z):
        self.x1=min(x,self.x1)
        self.y1=min(y,self.y1)
        self.z1=min(z,self.z1)
        self.x2=max(x,self.x2)
        self.y2=max(y,self.y2)
        self.z2=max(z,self.z2)

class Mesh:
    def __init__(self,_vertices=[],_faces=[],_edges=[]):
        self.vertices=_vertices
        self.faces=_faces
        self.edges=_edges

    def getEdgeAdjacentToVertices(self,v1,v2):
        for edge in v1.edges:
            if edge.v2==v2 or edge.v1==v2:
                return edge
        return None

    def weldVertices(self):
        weldedVertices={}
        self.vertices=[]
        for f in self.faces:
            for i in range(len(f.vertices)):
                v=f.vertices[i]
                vtuple=(v.x,v.y,v.z)
                if vtuple in weldedVertices:
                    f.vertices[i]=weldedVertices[vtuple]
                else:
                    weldedVertices[vtuple]=v
        self.vertices=weldedVertices.values()

    def updateAdjacencies(self):
        self.weldVertices()
        self.edges=[]
        for v in self.vertices:
            v.edges=[]
        for f in self.faces:
            v1=f.vertices[-1]
            for v2 in f.vertices:
                edge=self.getEdgeAdjacentToVertices(v1,v2)
                if edge == None:
                    edge=Edge(v1,v2)
                    v1.edges.append(edge)
                    v2.edges.append(edge)
                    self.edges.append(edge)
                if edge.v1==v1:
                    edge.face1=f
                else:
                    edge.face2=f
                v1=v2

