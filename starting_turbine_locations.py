import numpy as np
from wind_farm_visualization import *


def random_circular_start(nTurbines,rotor_diameter,farm_radius):
    """This sets up the initial turbine locations randomly in a circular boundary assuming constant rotor diameter

    INPUTS
    ______________________________________________________________________________
    nTurbines: number of wind turbines (int)
    rotor_diameter: assumed constant rotor diameter (float)
    farm_radius: radius of circular wind farm with center 0,0 (float)

    OUTPUTS
    ______________________________________________________________________________
    turbineX: turbine x locations
    turbineY: turbine y locations
    """

    turbineX = np.array([])
    turbineY = np.array([])
    for i in range(nTurbines):
        good=False
        while good==False:
            x = float(np.random.rand(1)*2.*farm_radius-farm_radius)
            y = float(np.random.rand(1)*2.*farm_radius-farm_radius)
            R = np.sqrt(x**2+y**2)
            good_sum = 0
            for j in range(len(turbineX)):
                dist = 0.
                dist = np.sqrt((turbineX[j]-x)**2+(turbineY[j]-y)**2)
                if dist > 3.*rotor_diameter:
                    good_sum += 1
            if good_sum == len(turbineX) and R <= farm_radius:
                turbineX = np.append(turbineX,x)
                turbineY = np.append(turbineY,y)
                good=True

    return turbineX, turbineY


def grid_start(nRows,rotor_diameter,spacing):
    """this sets up initial turbine locations in a grid

    INPUTS
    ______________________________________________________________________________
    nRows: number of rows (int)
    rotor_diameter: rotor diameter for which turbine spacing is defined (float)
    spacing: grid spacing in rotor_diameters (float)

    OUTPUTS
    ______________________________________________________________________________
    turbineX: turbine x locations
    turbineY: turbine y locations

    """

    loc_array = np.arange(nRows)*spacing*rotor_diameter
    loc_array = loc_array - max(loc_array)/2.
    nTurbines = nRows**2
    turbineX = np.zeros(nTurbines)
    turbineY = np.zeros(nTurbines)
    for i in range(nRows):
        turbineX[i*nRows:nRows*(i+1)] = loc_array[i]
        for j in range(nRows):
            turbineY[i*nRows+j] = loc_array[j]

    return turbineX, turbineY


def perturb(x,y,perturbation):
    """randomly perturb some points

    INPUTS
    ______________________________________________________________________________
    x: x points
    y: y points
    perturbation: max perturbation amount

    OUTPUTS
    ______________________________________________________________________________
    newX: randomly perturbed x points
    newY: randomly perturbed y points
    """

    nPoints = len(x)
    perturbX = np.random.rand(nPoints)*2.*perturbation-perturbation
    perturbY = np.random.rand(nPoints)*2.*perturbation-perturbation
    newX = x+perturbX
    newY = y+perturbY

    return newX, newY



if __name__=="__main__":
    nTurbines = 10
    rotor_diameter = 150.
    farm_radius = 1000.
    x,y, = random_circular_start(nTurbines,rotor_diameter,farm_radius)

    plot_turbine_locations(x,y,np.ones(nTurbines)*rotor_diameter,circle_boundary=True,farm_radius=farm_radius)
    plt.show()
