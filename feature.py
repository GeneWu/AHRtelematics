import os
import numpy as np
import pandas as pd
from collections import defaultdict
from random import random

from vertex import Vertex

DATA_DIR = "/Users/nickwang/Documents/Programs/python/projects/telematics/drivers"

def movingaverage(values,window):
    """
        smooth the list of values
    """
    weigths = np.repeat(1.0, window)/window

    smoothed = np.convolve(values, weigths, 'valid')
    return smoothed

def find_stop_points(speed):
    """
        speed < 0.5 : staypoint
        start point : run from stay point
        stop point : enter stay point
        return start point and end point index
    """
    bounded = np.hstack(([1], speed, [1]))
    staypoints = (bounded < 0.5)*1.0
    diffs = np.diff(staypoints)
    start_point = np.where(diffs < 0)[0]
    stop_point = np.where(diffs > 0)[0]
    return start_point.astype(int), stop_point.astype(int)


def turning_angles(trip):
    """
        compute the angles between velocity vectors
    """
    raw_speed_vec = np.diff(trip,axis=0)
    dx, dy = raw_speed_vec[:,0], raw_speed_vec[:,1]
    dd = np.sum(raw_speed_vec**2,axis=1)**0.5
    #cos<x1,x2> = np.dot(x1,x2)/|x1||x2|
    #angle range from [0,pi]
    angle = np.arccos( (dy[1:]*dy[:-1]+dx[1:]*dx[:-1]) / (dd[:-1]*dd[1:]) )
    not_nan = np.where(np.isfinite(angle))[0]
    angle = angle[not_nan]
    angle_percentile = [np.percentile(angle,per*10) for per in range(0,11)]

    speedyangle = angle * dd[:-1][not_nan]
    speedyangle_percentile = [np.percentile(speedyangle,per*10) for per in range(0,11)]
    return angle_percentile, speedyangle_percentile

def extract_features_from_trip(trip):
    # 1.1 total time of the trip
    duration = len(trip)

    #speed
    speed = np.sum(np.diff(trip,axis=0)**2,axis=1)**0.5

    # 1.2total distance traveled
    distance = np.sum(speed)

    # 2.1smooth the speed
    smooth_speed =  movingaverage(speed,10)
    speed_percentile = [np.percentile(smooth_speed,per*10) for per in range(0,11)]
    std_speed = speed.std()

    # 2.2acceleration
    acc = np.diff(speed)
    #smooth acceleration
    smooth_acc = movingaverage(acc,10)
    acc_percentile = [np.percentile(smooth_acc,per*10) for per in range(0,11)]
    std_acc = acc.std()

    # 2.3jerk (third derivative of speed)
    jerk = np.diff(acc)
    #smooth jerk
    smooth_jerk = movingaverage(jerk,10)
    jerk_percentile = [np.percentile(smooth_jerk,per*10) for per in range(0,11)]
    std_jerk = jerk.std()

    #2.4total energy
    total_energy = np.sum(speed**2)

    #average breaking strengh?

    # 3 turning angles
    angle_percentile, speedyangle_percentile = turning_angles(trip)

    # 4 stop and start points
    start_points, stop_points = find_stop_points(speed)

    # 4.1 number of stop points
    n_stop_points = len(stop_points)

    interval = 5
    # 4.2 average deceleration over 5 seconds before stop, including the stop point
    end_points = stop_points[stop_points-interval+1 >= 0]
    pre_stop_acc = [(speed[idx] - speed[idx - 4]) / 5.0 for idx in end_points]
    pre_stop_acc_mean = np.mean(pre_stop_acc)
    pre_stop_acc_min = np.min(pre_stop_acc)
    pre_stop_acc_std = np.std(pre_stop_acc)

    # 4.3 average acceleration over 5 seconds after start point, including the start point
    begin_points = start_points[start_points + interval - 1 < len(speed)]
    post_stop_acc = [(speed[idx] - speed[idx + 4]) / 5.0 for idx in begin_points]
    post_stop_acc_mean = np.mean(post_stop_acc)
    post_stop_acc_max = np.max(post_stop_acc)
    post_stop_acc_std = np.std(post_stop_acc)

    return {'route' : np.array([duration, distance]),
            'speed' : np.concatenate((speed_percentile, acc_percentile, jerk_percentile, np.array([std_speed, std_acc, std_jerk, total_energy]) )),
            'turning' : np.concatenate((angle_percentile, speedyangle_percentile)),
            'stop_points' : np.concatenate((n_stop_points, pre_stop_acc_mean, pre_stop_acc_min, pre_stop_acc_std, post_stop_acc_mean, post_stop_acc_max, post_stop_acc_std))
            }

def extract_trips(driver_id, trip_id):
    filename = os.path.join(DATA_DIR, str(driver_id) ,'%d.csv' % trip_id)
    res = extract_features_from_trip(np.array(pd.read_csv(filename)))
    vertex_id = "%d_%d" % (driver_id, trip_id)
    return Vertex(vertex_id, res)

if __name__ == "__main__":
    extract_trips(1,1)
