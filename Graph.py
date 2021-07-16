class Vertex:
    def __init__(self, V):
        self.val = V
        self.adj_vertices = []
        self.visited = False
    
    
class Edge:
    def __init__(self, u, v, fk):
        self.src = u
        self.tgt = v
        self.on = fk


class Graph:
    def __init__(self, vertices=[]):
        self.vertex_count = len(vertices)
        self.vertices = vertices
        self.visited = {v:False for v in vertices}
    
    def DFSUtil(self, temp, v):
        v.visited = True
        temp.append(v)
        for i in v.adj_vertices:
            if i[0].visited == False:
                temp = self.DFSUtil(temp, i[0])
        return temp
    
    def addVertex(self, vertex):
        vertex = Vertex(vertex)
        if vertex not in self.vertices:
            self.vertices.append(vertex)
            self.vertex_count += 1
            self.visited[vertex] = False
        return vertex

    def addEdge(self, v, w, fk):
        edge = Edge(v, w, fk)
        v.adj_vertices.append((w, edge))
        w.adj_vertices.append((v, edge))
        
        
    def connectedComponents(self):
        # visited = [False for i in range(self.vertex_count)]
        cc = []
        for v in self.vertices:
            if v.visited == False:
                temp = []
                cc.append(self.DFSUtil(temp, v))
        return cc
    
    def createAllSubgraphs(self, v):
        from itertools import chain, combinations
        g = [n for n in self.vertices if (n not in v)]
        sublist = list(chain.from_iterable(combinations(g, r) for r in range(len(g)+1)))
        subGraphs = [Graph(list(s)+v) for s in sublist]
        return subGraphs
    
    # DFS function
    def dfs(self, x, temp):
        self.visited[x[0]] = True
        temp.append(x)
        for i in x[0].adj_vertices:
            if i[0] in self.vertices and not self.visited[i[0]]:
                temp = self.dfs(i, temp)
        return temp

    def Is_Connected(self) :
        # Call for correct direction
        if self.vertex_count<0:
            return False
        self.dfs((self.vertices[0], None),[])
        for i in self.visited :
            if (not self.visited[i[0]]) :
                return False
        return True   
    
    def getSpaning(self):
        if self.vertex_count<0:
            return []
        spanning = self.dfs((self.vertices[0], None), [])
        for i in self.visited :
            if (not self.visited[i]) :
                return []
        return spanning

# Driver code
if __name__ == "__main__" :
    g = Graph()
    n1 = g.addVertex(1)
    n2 = g.addVertex(2)
    n3 = g.addVertex(3)
    n4 = g.addVertex(4)
    n0 = g.addVertex(0)
    g.addEdge(n1, n0)
    g.addEdge(n2, n3)
    g.addEdge(n3, n4)
    cc = g.connectedComponents()
    cc2 = [[v.val for v in c] for c in cc]
    print("Following are connected components")
    print(cc2, '--------')
    for c in cc:
        g = Graph(c)
        joinVertices = c[0:len(c)//2]
        subgraphs = g.createAllSubgraphs(joinVertices)
        ret = set()
        for sg in subgraphs:
            joinChain = sg.getSpaning()
            if len(joinChain) > 0:
                ret.add(tuple(joinChain))
        for r in ret:
            print(r[0].val, r[1].on)
        # print(list(map(list, ret)))

