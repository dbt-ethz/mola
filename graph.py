#http://www.iti.fh-flensburg.de/lang/algorithmen/graph/dijkstra.htm
#http://www.iti.fh-flensburg.de/lang/algorithmen/graph/shortest-paths.htm
#http://en.wikipedia.org/wiki/Dijkstra_algorithm
from Queue import PriorityQueue

'works with graphs which provide 3 methods: getNumNodes(), getNbs(), and getWeight()'

class Dijkstra:
    def __init__(self, graph):
    	n = graph.getNumNodes()
        self.graph=graph
        self.dist = [1000000]*n
        self.pred = [-1]*n
        self.traffic = [0]*n
    	self.centrality = [0]*n

    def computeAllDistancesFromA(self,startIndexes):
    	pq = PriorityQueue()
        for i in startIndexes:
            self.dist[i] == 0
            pq.put((0, i))
    	while not pq.empty(): #and not tree[end]:
            u = pq.get()(1)
            nbs = self.graph.getNbs(u)
            for v in nbs:
                d = self.dist[u] + graph.getWeight(u, v)
                if d < self.dist[v]:
    				self.dist[v] = d
    				self.pred[v] = u
    				pq.put((d, v))

    def getShortestPath(self,v):
        p=[]
    	while (v != -1):
            p.append(v)
    	    v = self.pred[v]
    	return p

    def computeTrafficAndCentrality(self,nodes):
        self.traffic = [0]*n
    	self.centrality = [0]*n
    	for i in range(len(nodes)-1):
            startI=nodes[i]
            self.dist = [100000]*n
            self.pred = [-1]*n
            computeAllDistancesFromA([startI])
            for j in range(i,len(nodes)):
                endI = nodes[j]
                if endI != startI:
                    self.centrality[startI] += self.dist[endI]
                    self.centrality[endI] += self.dist[endI]
                    path = getShortestPath(endI)
                    for ii in path:
    					cI = path[ii]
    					self.traffic[cI]+=1
