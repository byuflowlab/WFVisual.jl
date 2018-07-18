import numpy as np
from _porteagel_fortran import porteagel_visualize as porteagel_visualize_fortran

def boundary_points_function(nPoints,boundary_type='circle',boundary_radius=1500.,boundary_center=(0.,0.)):
    if nPoints%2==1:
        nPoints+=1

    if boundary_type=='circle':
        centerX = boundary_center[0]
        centerY = boundary_center[1]
        theta = np.linspace(0.,2.*np.pi,nPoints)
        xpoints = boundary_radius*np.cos(theta) + centerX
        ypoints = boundary_radius*np.sin(theta) + centerY
        zpoints = np.zeros(nPoints)
        boundaryPoints = np.zeros((nPoints,3))
        for i in range(nPoints):
            boundaryPoints[i][0] = xpoints[i]
            boundaryPoints[i][1] = ypoints[i]
            boundaryPoints[i][2] = zpoints[i]
        return boundaryPoints



def WindFrame(wind_direction, turbineX, turbineY):
    """ Calculates the locations of each turbine in the wind direction reference frame """
    windDirectionDeg = wind_direction
    # adjust directions
    windDirectionDeg = 270. - windDirectionDeg
    if windDirectionDeg < 0.:
        windDirectionDeg += 360.
    windDirectionRad = np.pi*windDirectionDeg/180.0    # inflow wind direction in radians

    # convert to downwind(x)-crosswind(y) coordinates
    turbineXw = turbineX*np.cos(-windDirectionRad)-turbineY*np.sin(-windDirectionRad)
    turbineYw = turbineX*np.sin(-windDirectionRad)+turbineY*np.cos(-windDirectionRad)

    return turbineXw, turbineYw



def call_julia_visualize(turbineX,turbineY,turbineZ,rotorDiameter,hubHeight,nBlades,wind_direction,wind_speed,
                            yaw,boundaryPoints,wake_model='gaussian',args=False):
    nTurbines = len(turbineX)
    globalYaw = yaw-wind_direction
    turbineXw,turbineYw = WindFrame(wind_direction,turbineX,turbineY)
    sorted_x_idx = np.argsort(turbineXw, kind='heapsort')
    if wake_model=='gaussian':
        if args:
            Ct,ky,kz,alpha,beta,I,RotorPointsY,RotorPointsZ,z_ref,z_0,shear_exp,wake_combination_method,\
                        ti_calculation_method,calc_k_star,opt_exp_fac,wake_model_version,interp_type,use_ct_curve,ct_curve_wind_speed,ct_curve_ct = args
        else:
            Ct = np.ones(nTurbines)*8./9.
            ky = 0.0451828659474
            kz = 0.0451828659474
            alpha = 2.32
            beta = 0.154
            I = 0.108170096293
            RotorPointsY = [ 0.]
            RotorPointsZ = [ 0.]
            z_ref = 100.0
            z_0 = 0.0
            shear_exp = 0.30665565
            wake_combination_method = 1
            ti_calculation_method = 4
            calc_k_star = True
            opt_exp_fac = 1.0
            wake_model_version = 2016
            interp_type = 1
            use_ct_curve = False
            ct_curve_wind_speed = np.ones(nTurbines)*wind_speed
            ct_curve_ct = np.ones(nTurbines)*8./9.

        def wrapped_wake_model(loc):
            velX,velY = WindFrame(wind_direction, loc[0], loc[1])
            velZ = loc[2]
            ws_array = porteagel_visualize_fortran(turbineXw, sorted_x_idx, turbineYw,
                                                           hubHeight, rotorDiameter, Ct,
                                                           wind_speed, np.copy(yaw),
                                                           ky, kz, alpha, beta, I, RotorPointsY, RotorPointsZ,
                                                           z_ref, z_0, shear_exp, velX, velY, velZ, wake_combination_method,
                                                           ti_calculation_method, calc_k_star, opt_exp_fac, wake_model_version,
                                                           interp_type, use_ct_curve, ct_curve_wind_speed, ct_curve_ct)
            return ws_array

        # x = 280.
        # y = 230.
        # z = 100.
        # resolution = 100
        # x = np.linspace(-2000.,2000.,resolution)
        # y = np.linspace(-2000.,2000.,resolution)
        # xx, yy = np.meshgrid(x, y)
        # xx = xx.flatten()
        # yy = yy.flatten()
        # n = len(xx)
        # zz = np.ones(n)*z
        # velocities = np.zeros(n)
        #
        # for i in range(n):
        #     loc = np.array([xx[i],yy[i],zz[i]])
        #     # print loc
        #     velocities[i] = wrapped_wake_model(loc)
        #
        # import matplotlib.pyplot as plt
        # fig = plt.figure(frameon=False)
        # ax = fig.add_subplot(111)
        # vel = velocities.flatten()
        # vmin = min(vel)
        # vmax = wind_speed
        # vel = vel.reshape(len(y), len(x))
        # im = plt.pcolormesh(x, y, vel, cmap='Blues_r', vmin=vmin, vmax=vmax)
        # ax.set_aspect('equal')
        # ax.autoscale(tight=True)
        # cbar = plt.colorbar(im,fraction=0.046, pad=0.04, orientation = 'horizontal', ticks=[vmin,(vmin+vmax)/2,vmax])
        # cbar.set_label('wind speed (m/s)')
        # ax.get_xaxis().set_visible(False)
        # ax.get_yaxis().set_visible(False)
        # for i in range(25):
        #     turbine = plt.Circle((turbineX[i],turbineY[i]), 50.,facecolor='blue',edgecolor=None,alpha=0.25)
        #     plt.gca().add_patch(turbine)
        # # farm_boundary = plt.Circle((0,0), 1500., linestyle='dashed',facecolor='none')
        # # plt.gca().add_patch(farm_boundary)
        # plt.axis('equal')
        # plt.xlim(-1700.,1700.)
        # plt.ylim(-1700.,1700.)
        # plt.draw()
        # plt.pause(0.001)
        #
        # plt.tight_layout()
        # plt.show()
