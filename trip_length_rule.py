import numpy as np
from rule import Rule
from edge import Edge

class TripLengthRule(Rule):
    """
        classify the trip as long / short based on time and distance
        output: long, short
    """
    def __init__(self):
        self.name = "TripLengthRule"
        self.long_edge = Edge(self.name, "long")
        self.short_edge = Edge(self.name, "short")

    def classify(self, vertex):
        time, distance = vertex.route[0], vertex.route[1]
        #long trip
        if distance > 1000 and time > 600:
            long_edge.add_vertex(vertex)
            return long_edge.id

        if distance <= 100:
            short_edge.add_vertex(vertex)
            return short_edge.id

