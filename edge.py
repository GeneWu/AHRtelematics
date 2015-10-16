from vertex import *

class Edge(object):
    """
        hyper edge
        vertices : set of the vertices that belongs to this type of edge
        id : name + "_" + value
        name : attribute name
        value : attribute value
    """
    def __init__(self, name, value):
        self.vertices = set()
        self.id = name + "_" + value
        self.name = name
        self.value = value

    def add_vertex(vertex):
        self.vertices.add(vertex)

