import os
import glob
import numpy as np

from vertex import Vertex

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
        for root, dirs, files in os.walk(data_dir):
            driver_id = root.split('/')[-1]
            for fn in files:
                trip_id = fn.split('.')[0]
                vertex = extract_trips(driver_id, trip_id)
                self.vertices.append(vertex)

                # apply the rules
