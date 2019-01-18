import numpy as np
import matplotlib.pyplot as plt
from visualize import *


if __name__=="__main__":
    small_example = False
    big_example = True
    if small_example:
        turbine_x = np.array([0.,0.,0.,500.,500.,500.,1000.,1000.,1000.]) - 500.
        turbine_y = np.array([0.,500.,1000.,0.,500.,1000.,0.,500.,1000.]) - 500.
        nTurbines = len(turbine_x)
        turbine_z = np.zeros(nTurbines)
        hub_height = np.array([120.,80.,120.,80.,120.,80.,120.,80.,120.])
        rotor_diameter = np.array([120.,80.,120.,80.,120.,80.,120.,80.,120.])
        wind_direction = 181.0
        wind_speed = 10.
        nBlades = np.array([3,3,3,3,3,3,3,3,3], dtype=int)
        yaw = np.array([30.,30.,30.,0.,0.,0.,0.,0.,0.])

    if big_example:
        turbine_x = np.array([  909.98349606,  1005.0174903 ,   900.40238835,  -479.57607866,
             937.92551703,   461.20472344,   123.06165965, -1073.3529325 ,
            -698.76200523, -1083.53094471,  1365.9338773 ,   204.10557045,
             306.99725222,  -585.35767689,    10.9706543 ,   543.54927959,
             -20.50212678, -1313.07762466, -1327.00852816,   137.06316521,
            1378.99410072,  -645.66250771,  -535.7876181 ,  -100.66538419,
           -1331.29278587])
        turbine_y = np.array([  500.59889721,  -974.65186327,    76.51586507,  1315.29789208,
            1039.37304649, -1321.85187113,  -300.57817461,  -765.82650713,
           -1213.14956771,   886.54973742,  -306.96866239,   194.51410928,
             735.69027357,    81.95252777,  -892.14222889,  -930.41798152,
             970.9117144 ,   398.75277565,    -3.52236011,  1393.27798468,
             241.61586052,  -791.92492366,   919.26560593, -1396.37638078,
            -433.19849727])
        turbine_z = np.array([ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.])
        hub_height = np.array([ 100.,  100.,  100.,  100.,  100.,  100.,  100.,  100.,  100.,
            100.,  100.,  100.,  100.,  100.,  100.,  100.,  100.,  100.,
            100.,  100.,  100.,  100.,  100.,  100.,  100.])
        rotor_diameter = np.array([ 100.,  100.,  100.,  100.,  100.,  100.,  100.,  100.,  100.,
            100.,  100.,  100.,  100.,  100.,  100.,  100.,  100.,  100.,
            100.,  100.,  100.,  100.,  100.,  100.,  100.])
        wind_direction = 228.0
        wind_direction = 240.
        # wind_direction = 65.
        wind_speed = 9.6279135339051418
        nBlades = np.array([3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
           3, 3], dtype=int)
        yaw = np.array([ 30.,  30.,  30.,  30.,  30.,  30.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.])
        yaw = np.ones(len(turbine_z))*30.

    nPoints = 179
    boundary_points = boundary_points_function2(nPoints)
    # print boundary_points

    call_julia_visualize(turbine_x,turbine_y,turbine_z,rotor_diameter,hub_height,nBlades,wind_direction,wind_speed,
                                yaw,boundary_points,wake_model='gaussian',args=False)

    """2D layout plot"""
    # nTurbines = len(turbine_x)
    # farm_radius = 1500.
    # for i in range(nTurbines):
    #     turb = plt.Circle((turbine_x[i],turbine_y[i]),rotor_diameter[i]/2.,fc='blue',ec='none',alpha=0.25)
    #     plt.gca().add_patch(turb)
    # boundary = plt.Circle((0.,0.),farm_radius,fc='none',ec='black',linestyle='dashed')
    # plt.gca().add_patch(boundary)
    #
    # plt.ylim(-farm_radius-2.*rotor_diameter[0],farm_radius+2.*rotor_diameter[0])
    # plt.axis('equal')
    #
    # plt.show()
