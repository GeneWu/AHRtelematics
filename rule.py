import numpy as np
from edge import Edge

class Rule(object):
    """
        abstract class for all the rules
        every (name, output) pair of the rule define a type of edge,
        create all the edges as instance variables and update the edge based on the output of the classify method

        to create new rule:
        1. create a class and inherit the Rule class
        2. define the rule name and instanitate the edge variables
        3. overwrite the classify method, which return name + "_" + output

    """
    def __init__(self):
        self.name = ""

    def classify(self, vertex):
        pass

    def edges(self):
        pass


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
            self.long_edge.add_vertex(vertex)
            return self.long_edge.id

        if distance <= 100:
            self.short_edge.add_vertex(vertex)
            return self.short_edge.id

    def edges(self):
        return [self.long_edge, self.short_edge]

class MedianSpeed(Rule):
    """
        classify the trip as high / low median speed
        output : high , low
    """
    def __init__(self):
        self.name = "MedianSpeed"
        self.high_edge = Edge(self.name, "high")
        self.low_edge = Edge(self.name, "low")

    def classify(self, vertex):
        median_speed = vertex.speed[5]
        # high median speed
        if median_speed > 25.0:
            self.high_edge.add_vertex(vertex)
            return self.high_edge.id
        if median_speed < 8:
            self.low_edge.add_vertex(vertex)
            return self.low_edge.id

    def edges(self):
        return [self.high_edge, self.low_edge]

class MedianSpeedyTurning(Rule):
    """
        classify the trip as high speedy turning based on median
        output: high
    """
    def __init__(self):
        self.name = "MedianSpeedyTurning"
        self.high_edge = Edge(self.name, "high")

    def classify(self, vertex):
        median_speedy_angle = vertex.turning[16]
        if median_speedy_angle > 1.0:
            self.high_edge.add_vertex(vertex)
            return self.high_edge.id

    def edges(self):
        return [self.high_edge]

class PostStopAcc(Rule):
    """classify the trip as high based on maximum of post_stop_acc"""
    def __init__(self):
        self.name = "PostStopAcc"
        self.high_edge = Edge(self.name, "high")

    def classify(self, vertex):
        max_post_stop_acc = vertex.stop_points[5]
        if max_post_stop_acc > 2.0:
            self.high_edge.add_vertex(vertex)
            return self.high_edge.id

    def edges(self):
        return [self.high_edge]

class PreStopAcc(Rule):
    """classify the trip as high based on the minimum of pre_stop_acc, which is the maximum of deceleration"""
    def __init__(self):
        self.name = "PreStopAcc"
        self.high_edge = Edge(self.name, "high")

    def classify(self, vertex):
        min_pre_stop_acc = vertex.stop_points[2]
        if min_pre_stop_acc < -3.0:
            self.high_edge.add_vertex(vertex)
            return self.high_edge.id

    def edges(self):
        return [self.high_edge]


