# import queue
import heapq
from src import Connection

class GraphException(Exception):
    def __init___(self, d_error_arguments):
        Exception.__init__(self, "Graph Exception was raised with arguments {0}".format(d_error_arguments))
        self._d_error_arguments = d_error_arguments





class Graph:

    def __init__(self, connections = None):
        '''
            Create a graph from an array of edges. Each edge is itself an array of 3 integers,
            the source node, the destination node and the distance between them. Nodes have to be
            sequential (eg. a node called 7 should not be present in graph unless there are nodes 0 to 6 already in it)
            
            Each edge in the input array will be added using 'addEdge(node1,node2,distance)}'
            implying that the reverse of each edge is also added and should NOT be explicitly in
            the input array.
            
            @param connections      the array of edges to add. (passing None: It is okay to create an empty graph, as we can add edges to it later)
            @raises GraphException  if there are not exactly 3 integers in each edge array

        '''  

        self._graph = {}

        if connections is not None:

            for connection in connections:
                if len(connection) != 3:
                    raise GraphException("Connections in Graphs must have 3 integers: node 1, node 2 and the distance between them. This connection did not: " + str(connection)) 
                self.add_edge(connection[0], connection[1], connection[2])



    def add_edge(self, node1, node2, distance):
        '''
            Add an edge to the graph
        
            This graph is UNDIRECTED, so any time we add an edge we must add the reverse edge as well.
        
            param node1             The source node
            param node2             The destination node
            param distance          The distance or weight on the edge

            raises GraphException   if the distance is negative

        '''
        
        if distance < 0:
            raise GraphException("All distances must be greater than or equal to 0: attempted to add node %d to node %d with distance %d"%(node1, node2, distance))

        if node1 not in self._graph:
            self._graph[node1] = []

        self._graph[node1].append(Connection(node2, distance))

        # ----- also add the reverse connection
        if node2 not in self._graph:
            self._graph[node2] = []

        self._graph[node2].append(Connection(node1, distance))


    def get_connections(self):
        '''
            Get an array of edges in the same form as the array of edges Graph constructor, except that
            this method returns ALL the individual edges, thus one for the forward and one for the reverse direction of each true edge.

            @return the array of edges in the graph

        '''
        connections = []
        for node in self._graph:
            for edge in self._graph[node]:
                connections.append([node, edge.node, edge.distance])

        return connections

    def contract_node_with_two_edges(self, node):

        '''
            Contract a node that has exactly two connecting edges

            This is the simplest case of contracting nodes. If node X is connected to node A with
            distance a and node B with distance b, then this will remove both the X-A and the X-B
            edge (essentially removing X from the graph), and add a new edge (A-B) with distance a+b

            Pre-existing edge between A and B are not be changed
            or removed.

            @param node             the node to be contracted
            @raises GraphException  if the node to be contracted does not exist in the graph or
                                        does not have precisely two edges
            
        '''
        if node not in self._graph:
            raise GraphException("Graph does not have the given node: %d"%node)

        if len(self._graph[node]) != 2:
            raise GraphException("The number of connections for the node '%d' has to be 2. It was %d"%(node,len(self._graph[node])))

        connections = self._graph[node]

        # ----- remove node from graph
        del(self._graph[node])

        for connection in connections:
            for inv_connection in self._graph[connection.node]:
                if inv_connection.node == node:
                    self._graph[connection.node].remove(inv_connection)

        # ----- add new edge bypassing the current given node using its previous connections
        self.add_edge(connections[0].node, connections[1].node, connections[0].distance+connections[1].distance)


    def dijkstra_version_1(self, node1, node2):

        '''
            Apply Dijkstra's algorithm to find the distance between 2 nodes in the graph. Implemented according to John Bullinaria's lecture notes.
    
            
            @param node1            the start node in the pair between which the distance is to be found
            @param node2            the final node in the pair between which the distance is to be found

            @return                 the distance between the pair of nodes

            @raises GraphException  if either of the nodes are not in the graph or there is no path
                                        between them
            
        '''

        if node1 not in self._graph:
            raise GraphException("Node 1 '%d' does not exist in graph"%node1)

        if node2 not in self._graph:
            raise GraphException("Node 2 '%d' does not exist in graph"%node2)


        # ----- set the distance of node1 to itself zero, and the distance of node1 to the other nodes infinite
        D = [float('inf')] * len(self._graph)
        D[node1] = 0 

        # ----- We use an auxiliary array ‘tight’ indexed by the vertices, that records for which nodes the shortest path estimates are ‘‘known’’ to be tight by the algorithm.
        tight = [False]*len(self._graph)

        # ----- the actual algorithm
        for i in range(len(tight)):
            tight[i] = True
            for connection in self._graph[i]:
                if D[i] + connection.distance < D[connection.node]:
                    D[connection.node] = D[i] + connection.distance

        return D[node2]


    def dijkstra_version_2(self, node1, node2):

        '''
            Apply Dijkstra's algorithm to find the distance between 2 nodes in the graph. Implemented according to John Bullinaria's lecture notes.
            Uses priority queues to speed up.
            
            @param node1            the start node in the pair between which the distance is to be found
            @param node2            the final node in the pair between which the distance is to be found

            @return                 the distance between the pair of nodes

            @raises GraphException  if either of the nodes are not in the graph or there is no path
                                        between them
            
        '''

        # if node1 not in self._graph:
        #     raise GraphException("Node 1 '%d' does not exist in graph"%node1)

        # if node2 not in self._graph:
        #     raise GraphException("Node 2 '%d' does not exist in graph"%node2)


        # # ----- set the distance of node1 to itself zero, and the distance of node1 to the other nodes infinite
        # D = [float('inf')] * len(self._graph)
        # D[node1] = 0 

        # # ----- Create a priority queue containing all the vertices of the graph, with the entries of D as the priorities
        # pq = heapq.heapify(list(zip(D,[i for i in range(len(D))])))

        # # print (pq)
        # # input()
        # # pq = queue.PriorityQueue() 
        # # for i in range(len(D)):
        # #     pq.put((D[i], i))

        # for i in range(len(pq)):
        #     u = pq[i][1]
        #     for connection in self._graph[u]:
        #         if D[u] + connection.distance < D[connection.node]:
        #             D[connection.node] = D[u] + connection.distance
        #             # ----- change priority of the node in the priority queue... HOWW???

        # return D[node2]
        raise NotImplementedError("Have to change priority of a node in the priority queue... How..?")

    def dijkstra(self, node1, node2):
        return self.dijkstra_version_2(node1, node2)


    def __str__(self):
        return str(self._graph)


        


if __name__ == '__main__':
    
    edges = [[ 0, 1, 4 ],
            [ 0, 3, 2 ],
            [ 1, 2, 5 ],
            [ 1, 3, 1 ],
            [ 2, 3, 8 ],
            [ 2, 4, 1 ],
            [ 2, 5, 6 ],
            [ 3, 4, 9 ],
            [ 4, 5, 3 ]]

    g = Graph(edges)
    # g.add_edge(1,2,3)
    # g.add_edge(1,3,4)
    # g.add_edge(2,3,5)

    # print (g.get_connections())
    # print(g)
    # g.contract_node_with_two_edges(1)

    # print(g)

    print (g.dijkstra_version_1(2,3))
    print (g.dijkstra(2,3))


