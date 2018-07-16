import numpy as np
import matplotlib.pyplot as plt
import math


def plot_wind_rose(dirs,yval,color='blue',alpha=0.25,title=False,titlesize=20,titlefont='serif',\
                    tics=False,ticangle=-45.,ticlabels=False,ticlabelsize=18,ticlabelfont='serif',\
                    dirsize=20,dirfont='serif'):

    """create wind rose plot.
    must save figure outside of this function
    must call plt.show() if you want the figure to remain shown


    INPUTS
    ______________________________________________________________________________
    dirs: wind directions in degrees as an numpy array
    yval: wind value (frequency or wind speed) as a numpy array

    color: color of the wind rose, default pyplot colors (string) or custom RBG values (float)
    alpha: transparancy of the wind rose as a float as a float
    title: plot title as a string. This must be active for the other title options to work
    titlesize: title font size as a float
    titlefont: title font family
    tics: locations of custom tics as a tuple. This must be active for the other tic options to work
    ticangle: angle of the tic labels
    ticlabels: custom tic labels as a tuple. This must be active for the other ticlabel options to work
    ticlabelsize: font size of the tic labels
    ticlabelfont: font family of the tic labels
    dirsize: font size of the directions
    dirfont: font size of the directions
    """

    nDirections = len(dirs)
    dirs += 270.
    for i in range(nDirections):
        dirs[i] = np.radians(dirs[i])*-1.
    width = (2*np.pi) / nDirections
    dirs = dirs-width/2.
    max_height = np.max(yval)
    ax = plt.subplot(111, polar=True)
    bars = ax.bar(dirs, yval, width=width, bottom=0., color=color,alpha=alpha)
    ax.set_xticklabels(['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE'],fontsize=dirsize,family=dirfont)

    if tics:
        ax.set_rgrids(tics, angle=ticangle)
    else:
        max_tic = float(format(max(yval), '.1g'))
        ax.set_rgrids([max_tic/3.,2.*max_tic/3.,max_tic], angle=ticangle)

    if ticlabels:
        ax.set_yticklabels(ticlabels,fontsize=ticlabelsize,family=ticlabelfont)
    if title:
        plt.title(title, y=1.09,fontsize=titlesize,family=titlefont)
    plt.tight_layout()
    plt.draw()
    plt.pause(0.001)




def plot_turbine_locations(turbineX,turbineY,rotorDiameter,\
                           facecolor='blue',alpha=0.25,\
                           farm_radius=False,farm_bounds=False):
    """plot the turbine layouts"""

    nTurbines = len(turbineX)
    for i in range(nTurbines):
        turbine = plt.Circle((turbineX[i],turbineY[i]),rotorDiameter[i]/2.,fc=facecolor,alpha=alpha,lw=0.)
        plt.gca().add_patch(turbine)
    if farm_radius:
        farm_boundary = plt.Circle((0,0),farm_radius,linestyle='dashed',facecolor='none')
        plt.gca().add_patch(farm_boundary)
    plt.axis('equal')

    if farm_bounds:
        plt.axis(farm_bounds)
    elif farm_radius:
        plt.xlim(-farm_radius-2.*rotorDiameter[0],farm_radius+2.*rotorDiameter[0])
        plt.ylim(-farm_radius-2.*rotorDiameter[0],farm_radius+2.*rotorDiameter[0])
    else:
        plt.xlim(min(turbineX)-2.*rotorDiameter[0],max(turbineX)+2.*rotorDiameter[0])
        plt.ylim(min(turbineY)-2.*rotorDiameter[0],max(turbineY)+2.*rotorDiameter[0])
    plt.draw()
    plt.pause(0.001)


if __name__=="__main__":

    """test wind rose"""
    # wf = np.array([1.17812570e-02, 1.09958570e-02, 9.60626600e-03, 1.21236860e-02,
    #                            1.04722450e-02, 1.00695140e-02, 9.68687400e-03, 1.00090550e-02,
    #                            1.03715390e-02, 1.12172280e-02, 1.52249700e-02, 1.56279300e-02,
    #                            1.57488780e-02, 1.70577560e-02, 1.93535770e-02, 1.41980570e-02,
    #                            1.20632100e-02, 1.20229000e-02, 1.32111160e-02, 1.74605400e-02,
    #                            1.72994400e-02, 1.43993790e-02, 7.87436000e-03, 0.00000000e+00,
    #                            2.01390000e-05, 0.00000000e+00, 3.42360000e-04, 3.56458900e-03,
    #                            7.18957000e-03, 8.80068000e-03, 1.13583200e-02, 1.41576700e-02,
    #                            1.66951900e-02, 1.63125500e-02, 1.31709000e-02, 1.09153300e-02,
    #                            9.48553000e-03, 1.01097900e-02, 1.18819700e-02, 1.26069900e-02,
    #                            1.58895900e-02, 1.77021600e-02, 2.04208100e-02, 2.27972500e-02,
    #                            2.95438600e-02, 3.02891700e-02, 2.69861000e-02, 2.21527500e-02,
    #                            2.12465500e-02, 1.82861400e-02, 1.66147400e-02, 1.90111800e-02,
    #                            1.90514500e-02, 1.63932050e-02, 1.76215200e-02, 1.65341460e-02,
    #                            1.44597600e-02, 1.40370300e-02, 1.65745000e-02, 1.56278200e-02,
    #                            1.53459200e-02, 1.75210100e-02, 1.59702700e-02, 1.51041500e-02,
    #                            1.45201100e-02, 1.34527800e-02, 1.47819600e-02, 1.33923300e-02,
    #                            1.10562900e-02, 1.04521380e-02, 1.16201970e-02, 1.10562700e-02])
    # nDirections = len(wf)
    # dirs = np.linspace(0,360-360/nDirections, nDirections)
    # color = 'red'
    # alpha = 0.25
    # title = 'Amalia Wind Rose'
    # titlesize = 20
    # titlefont = 'serif'
    # tics = [0.01,0.02,0.03]
    # ticlabels = ['1%','2%','3%']
    # ticangle= -45.
    # plot_wind_rose(dirs,wf)
    # # plot_wind_rose(dirs,wf,color=color,alpha=alpha,title=title,titlesize=titlesize,titlefont=titlefont,\
    #                     # tics=tics,ticangle=ticangle,ticlabels=ticlabels,ticsize=18,ticfont='serif',dirsize=20,dirfont='serif')
    #
    # plt.show()

    turbineX = np.array([0.,0.,0.,500.,500.,500.,1000.,1000.,1000.])
    turbineY = np.array([0.,500.,1000.,0.,500.,1000.,0.,500.,1000.])
    rotorDiameter = np.ones(len(turbineX))*100.
    edgecolor='black'
    plot_turbine_locations(turbineX,turbineY,rotorDiameter,facecolor='red',farm_radius=1000.*np.sqrt(2))
    plt.show()
