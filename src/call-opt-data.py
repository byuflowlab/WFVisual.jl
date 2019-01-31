import numpy as np
import matplotlib.pyplot as plt
from visualize import *


if __name__=="__main__":

    nTurbs = 32
    nSteps = 50

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

    n = 15
    x = np.zeros((nSteps+n*(nSteps-1),nTurbs))
    y = np.zeros((nSteps+n*(nSteps-1),nTurbs))
    d = np.zeros((nSteps+n*(nSteps-1),nTurbs))
    z = np.zeros((nSteps+n*(nSteps-1),nTurbs))

    x[0] = X[0]
    y[0] = Y[0]
    d[0] = D[0]
    z[0] = Z[0]

    for k in range(nSteps-1):
        x[(k+1)*(n+1)-1] = X[k+1]
        y[(k+1)*(n+1)-1] = Y[k+1]
        d[(k+1)*(n+1)-1] = D[k+1]
        z[(k+1)*(n+1)-1] = Z[k+1]
        for i in range(n):
            for j in range(nTurbs):
                x[k*(n+1)+i][j] = (X[k+1][j]-X[k][j])/float(n+1.)*float(i+1)+X[k][j]
                y[k*(n+1)+i][j] = (Y[k+1][j]-Y[k][j])/float(n+1.)*float(i+1)+Y[k][j]
                d[k*(n+1)+i][j] = (D[k+1][j]-D[k][j])/float(n+1.)*float(i+1)+D[k][j]
                z[k*(n+1)+i][j] = (Z[k+1][j]-Z[k][j])/float(n+1.)*float(i+1)+Z[k][j]


    wind_speed = 10.
    yaw = np.zeros(nTurbs)
    nBlades = np.ones(nTurbs, dtype=int)*3
    wind_direction = 0.
    wind_direction = -30.
    turbine_z = np.zeros(nTurbs)

    nPoints = 179
    boundary_points = boundary_points_function2(nPoints,boundary_radius=659.6969000988257)

    print np.shape(boundary_points)
    print boundary_points

    for i in range(500):
        a = np.deg2rad(30.)
        x_r = np.cos(a)*x[i] - np.sin(a)*y[i]
        y_r = np.sin(a)*x[i] + np.cos(a)*y[i]
        call_julia_visualize(x_r,y_r,turbine_z,d[i],z[i],nBlades,wind_direction,wind_speed,
                                yaw,boundary_points,num=i,wake_model='gaussian',nDIVS=np.array([100,100,25],dtype=int),save_path="/Users/ningrsrch/Dropbox/Projects/wind-farm-utilities/opt")
