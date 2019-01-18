import numpy as np
import matplotlib.pyplot as plt
from math import cos,sin,radians


def plot_wind_turbine(hub_height,rotor_diameter,tower_diameter,rotor_color='black',rotor_width=2,rotor_linestyle='dashed',
                      tower_color='blue',tower_width=2,blade_color='blue',blade_width=1,blade_angle=False):

    """plot a single wind turbine.
    must save figure outside of this function
    must call plt.show() if you want the figure to remain shown when the program ends
    this code may need to be added to or modified for your individual use

    INPUTS
    ______________________________________________________________________________
    hub_height: hub height of the turbine (float)
    rotor_diameter: rotor diameter of the turbine (float)
    tower_diameter: parameterized tower diameter at bottom, middle, top (np array)

    rotor_color: color of the rotor circle
    rotor_width: line width of the rotor circle
    rotor_linestyle: linstyle of the rotor circle
    tower_color: color of the tower
    tower_width: line width of the tower


    """
    #add the tower
    t = hub_height
    m = hub_height/2.
    b = 0.
    tr = tower_diameter[2]/2.
    tl = -tower_diameter[2]/2.
    mr = tower_diameter[1]/2.
    ml = -tower_diameter[1]/2.
    br = tower_diameter[0]/2.
    bl = -tower_diameter[0]/2.
    xt = np.array([bl,ml,tl,tr,mr,br,bl])
    yt = np.array([b,m,t,t,m,b,b])
    plt.plot(xt,yt,color=tower_color,lw=tower_width)

    #add the rotor circle
    rotor = plt.Circle((0.,hub_height),rotor_diameter/2.,fc='none',ec=rotor_color,lw=rotor_width,linestyle=rotor_linestyle)
    plt.gca().add_patch(rotor)

    #add the turbine blades
    bladeX = np.array([3.,7.,10.,15.,20.,25.,30.,35.,30.,25.,20.,15.,10.,5.,3.,3.])
    bladeY = np.array([0.,0.,0.8,1.5,1.7,1.9,2.1,2.3,2.4,2.4,2.4,2.4,2.4,2.4,2.4,0.])-1.5

    c = rotor_diameter/70.

    if blade_angle:
        angle=blade_angle
    else:
        angle = np.random.rand(1)*60.-55.

    blade1X = bladeX*cos(radians(angle))-bladeY*sin(radians(angle))
    blade1Y = bladeX*sin(radians(angle))+bladeY*cos(radians(angle))

    blade2X = bladeX*cos(radians(angle+120.))-bladeY*sin(radians(angle+120.))
    blade2Y = bladeX*sin(radians(angle+120.))+bladeY*cos(radians(angle+120.))

    blade3X = bladeX*cos(radians(angle+240.))-bladeY*sin(radians(angle+240.))
    blade3Y = bladeX*sin(radians(angle+240.))+bladeY*cos(radians(angle+240.))

    plt.plot(blade1X*c, blade1Y*c+hub_height, linewidth=blade_width, color=blade_color)
    plt.plot(blade2X*c, blade2Y*c+hub_height, linewidth=blade_width, color=blade_color)
    plt.plot(blade3X*c, blade3Y*c+hub_height, linewidth=blade_width, color=blade_color)

    # if title:
        # plt.title(title,fontsize=titlesize,family=titlefont)
    # plt.xlim(-rotor_diameter/2.-10.,rotor_diameter/2.+10.)
    plt.ylim(0.,rotor_diameter/2.+10.)
    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()
    plt.draw()
    plt.pause(0.001)


if __name__=="__main__":

    """test turbine plot"""
    h = 100.
    D = 100.
    d = np.array([6.,4.,3.])

    plot_wind_turbine(h,D,d,blade_angle=75.)
    plt.show()
