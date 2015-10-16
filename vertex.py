import numpy as np

class Vertex(object):
    """
        attributed vertex for trip
        id : driver_id + '_' + trip_id
        route : [duration, distance]
        speed : [speed_percentile, acc_percentile, jerk_percentile, [std_speed, std_acc, std_jerk, total_energy] ]
        turning : [angle_percentile, speedyangle_percentile]
        stop_points : [n_stop_points, pre_stop_acc_mean, pre_stop_acc_min, pre_stop_acc_std, post_stop_acc_mean, post_stop_acc_max, post_stop_acc_std]
    """
    def __init__(self, idx, attributes):
        self.id = idx
        self.route = attributes['route']
        self.speed = attributes['speed']
        self.turning = attributes['turning']
        self.stop_points = attributes['stop_points']
        self.rule_set = []

    def add_rule(self, rule):
        self.rule_set.append(rule)

