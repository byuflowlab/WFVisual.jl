import numpy as np
import matplotlib.pyplot as plt
from visualize import *


if __name__=="__main__":

    nTurbs = 32
    nSteps = 1

    file = '../data/opt-data/opt-z.txt'
    opt = open(file)
    optimized = np.loadtxt(opt)
    data = optimized
    Z = np.zeros((nSteps,nTurbs))
    for i in range(nSteps):
        Z[i][:] = data[i*nTurbs:(i+1)*nTurbs]

    file = '../data/opt-data/opt-diameters.txt'
    opt = open(file)
    optimized = np.loadtxt(opt)
    data = optimized
    D = np.zeros((nSteps,nTurbs))
    for i in range(nSteps):
        D[i][:] = data[i*nTurbs:(i+1)*nTurbs]

    file = '../data/opt-data/opt-x.txt'
    opt = open(file)
    optimized = np.loadtxt(opt)
    data = optimized
    X = np.zeros((nSteps,nTurbs))
    for i in range(nSteps):
        X[i][:] = data[i*nTurbs:(i+1)*nTurbs]

    file = '../data/opt-data/opt-y.txt'
    opt = open(file)
    optimized = np.loadtxt(opt)
    data = optimized
    Y = np.zeros((nSteps,nTurbs))
    for i in range(nSteps):
        Y[i][:] = data[i*nTurbs:(i+1)*nTurbs]

    wind_speed = 10.
    yaw = np.zeros(nTurbs)
    nBlades = np.ones(nTurbs, dtype=int)*3
    wind_direction = 0.
    turbine_z = np.zeros(nTurbs)

    nPoints = 15
    boundary_points = boundary_points_function2(nPoints,boundary_radius=659.6969000988257)
    # print np.shape(boundary_points)
    # boundary_points = boundary_points_function(nPoints,boundary_type='square',boundary_edge=659.6969000988257*2.)



    # boundary_points = np.zeros((5,3))
    #
    # R = 659.6969000988257*2.
    # bp = np.zeros((5,3))
    # bp[0][0] = -R
    # bp[1][0] = 0.
    # bp[2][0] = R
    # bp[3][0] = 0.
    # bp[4][0] = -R
    #
    # bp[0][1] = 0.
    # bp[1][1] = R
    # bp[2][1] = 0.
    # bp[3][1] = -R
    # bp[4][1] = 0.
    #
    # boundary_points = bp

    print np.shape(boundary_points)
    print boundary_points

    for i in range(500):
        call_julia_visualize(X[i],Y[i],turbine_z,D[i],Z[i],nBlades,wind_direction,wind_speed,
                                yaw,boundary_points,num=i,wake_model='gaussian',nDIVS=np.array([200,200,50],dtype=int),save_path="/Users/ningrsrch/Dropbox/Projects/wind-farm-utilities/opt1")
