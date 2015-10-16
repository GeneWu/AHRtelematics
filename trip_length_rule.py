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
        pass
