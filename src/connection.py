
'''

    A class to represent a connection in an adjacency list representation of a
    weighted undirected graph. Each node X in the graph has a list of connections,
    where the node Y of the connection is connected to node X with weight (or distance)
    given by the distance of this connection.

'''

class Connection:

    def __init__(self, node, distance):

        self._node = node
        self._distance = distance

    @property
    def node(self):
        return self._node
    
    @property
    def distance(self):
        return self._distance

    def hash_code(self):

        prime = 31
        result = 1
        result = prime * result + distance
        result = prime * result + node
        return result
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return "< Node: %d, Distance: %d >"%(self._node, self._distance)

    def __repr__(self):
        return "< Node: %d, Distance: %d >"%(self._node, self._distance)

