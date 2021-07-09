# Python program to print connected
# components; in an undirected graph
class Vertex:
    def __init__(self, V):
        self.val = V
        self.adj_vertices = []
        self.visited = False
    

class Graph:
    def __init__(self):
        self.vertex_count = 0
        self.vertices = []
    
    def DFSUtil(self, temp, v, visited):
        v.visited = True
        temp.append(v)
        for i in v.adj_vertices:
            if i.visited == False:
                temp = self.DFSUtil(temp, i, visited)
        return temp
    
    def addVertex(self, vertex):
        vertex = Vertex(vertex)
        if vertex not in self.vertices:
            self.vertices.append(vertex)
            self.vertex_count += 1
        return vertex
    
    
    def addEdge(self, v, w):
        v.adj_vertices.append(w)
        w.adj_vertices.append(v)
        
        
    def connectedComponents(self):
        visited = [False for i in range(self.vertex_count)]
        cc = []
        for v in self.vertices:
            if v.visited == False:
                temp = []
                cc.append(self.DFSUtil(temp, v, visited))
        return cc


# Driver Code
if __name__ == "__main__":
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
    cc = [[v.val for v in c] for c in cc]
    print("Following are connected components")
    print(cc)

