import os
import glob
import numpy as np

from rule import *
from feature import extract_trips

class Graph(object):
    """
        Attributed hyper Graph
        vertices : a set of vertex object
        edges : a set of hyper edges object
    """
    def __init__(self):
        self.vertices = []
        self.edges = []

    def construct(self, data_dir):
        # create rule set
        rule_list = [rule() for rule in Rule.__subclasses__()]
        for root, dirs, files in os.walk(data_dir):
            for fn in files:
                if fn[-3:] == 'csv':
                    driver_id = root.split('/')[-1]
                    trip_id = fn.split('.')[0]
                    vertex = extract_trips(driver_id, trip_id)
                    self.vertices.append(vertex)

                    # apply the rules
                    for rule in rule_list:
                        output = rule.classify(vertex)
                        if output:
                            vertex.add_rule(output)
        self.edges = [ edge for rule in rule_list for edge in rule.edges()]

if __name__ == "__main__":
    data_dir = "/Users/nickwang/Documents/Programs/python/projects/telematics/drivers"
    g = Graph()
    g.construct(data_dir)
