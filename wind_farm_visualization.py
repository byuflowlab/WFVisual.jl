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




def plot_turbine_locations(turbineX,turbineY,rotorDiameter,color='blue',alpha=0.25,title=False,titlesize=20,titlefont='serif',\
                           starting=False,startingX=False,startingY=False,starting_color='red',staring_alpha=0.25,lines=False,linecolor='black',linestyle='solid',\
                           circle_boundary=False,farm_radius=False,farm_center=(0.,0.),\
                           custom_boundary=False,boundaryX=False,boundaryY=False,
                           boundary_color='black',boundary_line='dashed',boundary_width=1,farm_bounds=False):

    """plot wind farm layouts.
    must save figure outside of this function
    must call plt.show() if you want the figure to remain shown when the program ends

    INPUTS
    ______________________________________________________________________________
    turbineX: numpy array of x locations
    turbineY: numpy array of y locations
    rotorDiameter: numpy array of turbine rotor diameters

    color: color of turbines, default pyplot colors (string) or custom RBG values (float)
    alpha: transparancy of the turbines as a float as a float
    title: plot title as a string. This must be active for the other title options to work
    titlesize: title font size as a float
    titlefont: title font family
    starting: True if you want to compare the starting locations to final locations
    startingX: numpy array of starting x locations
    startingY: numpy array of starting y locations
    starting_color: color of starting turbines, default pyplot colors (string) or custom RBG values (float)
    staring_alpha: transparancy of the starting turbines as a float as a float
    lines: True if you want lines connecting each starting turbine to its final location
    linecolor: color or lines connecting turibnes
    linestyle: style of lines connecting turbines
    circle_boundary: True if you want to display a circular wind farm boundary
    farm_radius: circular wind farm boundary radius (float)
    farm_center: circular wind farm boundary center (x,y)
    custom_boundary: True if you want to define a custom wind farm boundary
    boundaryX: numpy array of x values for a custom wind farm boundary
    boundaryY: numpy array of y values for a custom wind farm boundary
    boundary_color: color of the wind farm boundary
    boundary_line: line style of the wind farm boundary
    boundary_width: line width of the wind farm boundary
    farm_bounds: custom axis bounds on the plot (xmin,xmax,ymin,ymax)
    """


    nTurbines = len(turbineX)
    for i in range(nTurbines):
        if starting:
            opt_turbine = plt.Circle((startingX[i],startingY[i]),rotorDiameter[i]/2.,fc=starting_color,alpha=staring_alpha,lw=0.)
            plt.gca().add_patch(opt_turbine)
            if lines:
                plt.plot(np.array([startingX[i],turbineX[i]]),np.array([startingY[i],turbineY[i]]),color=linecolor,linestyle=linestyle)

        turbine = plt.Circle((turbineX[i],turbineY[i]),rotorDiameter[i]/2.,fc=color,alpha=alpha,lw=0.)
        plt.gca().add_patch(turbine)

    if circle_boundary:
        farm_boundary = plt.Circle(farm_center,farm_radius,linestyle=boundary_line,fc='none',edgecolor=boundary_color,linewidth=boundary_width)
        plt.gca().add_patch(farm_boundary)
    elif custom_boundary:
        plt.plot(boundaryX,boundaryY,color=boundary_color,linestyle=boundary_line,linewidth=boundary_width)


    """limits on the axes"""
    plt.axis('equal')
    if farm_bounds:
        plt.axis(farm_bounds)
    elif circle_boundary:
        plt.xlim(farm_center[0]-farm_radius-2.*rotorDiameter[0],farm_center[0]+farm_radius+2.*rotorDiameter[0])
        plt.ylim(farm_center[1]-farm_radius-2.*rotorDiameter[0],farm_center[1]+farm_radius+2.*rotorDiameter[0])
    else:
        plt.xlim(min(turbineX)-2.*rotorDiameter[0],max(turbineX)+2.*rotorDiameter[0])
        plt.ylim(min(turbineY)-2.*rotorDiameter[0],max(turbineY)+2.*rotorDiameter[0])

    if title:
        plt.title(title,fontsize=titlesize,family=titlefont)

    plt.axis('off')
    plt.tight_layout()
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


    """test layout plot"""
    turbineX = np.array([0.,0.,0.,500.,500.,500.,1000.,1000.,1000.])
    turbineY = np.array([0.,500.,1000.,0.,500.,1200.,0.,500.,1000.])
    startingX = np.array([0.,0.,0.,500.,500.,500.,1000.,1000.,1000.])+np.random.rand(len(turbineX))*100.
    startingY = np.array([0.,500.,1000.,0.,500.,1200.,0.,500.,1000.])+np.random.rand(len(turbineX))*100.
    rotorDiameter = np.ones(len(turbineX))*100.
    plot_turbine_locations(turbineX,turbineY,rotorDiameter,starting=True,startingX=startingX,startingY=startingY,color='blue',lines=True,circle_boundary=True,farm_radius=1000.*np.sqrt(2))
    plt.show()
    plot_turbine_locations(turbineX,turbineY,rotorDiameter)
    plt.show()
