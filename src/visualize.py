import numpy as np
from _porteagel_fortran import porteagel_visualize as porteagel_visualize_fortran
import _floris
import julia
# import WFVisual as wfv


def boundary_points_function(nPoints,boundary_type='circle',boundary_radius=1500.,boundary_center=(0.,0.),boundary_edge=1200.):

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

    if boundary_type=='square':
        centerX = boundary_center[0]
        centerY = boundary_center[1]
        half_edge = boundary_edge/2.
        n = nPoints/4
        d = boundary_edge/float(n)
        xpoints = np.zeros(4*n)
        ypoints = np.zeros(4*n)
        zpoints = np.zeros(4*n)

        xpoints[0:n] = centerX - half_edge
        ypoints[0:n] = np.linspace(centerY-half_edge,centerY+half_edge-d,n)
        xpoints[n:2*n] = np.linspace(centerX-half_edge,centerX+half_edge-d,n)
        ypoints[n:2*n] = centerY + half_edge
        xpoints[2*n:3*n] = centerX + half_edge
        ypoints[2*n:3*n] = np.linspace(centerY+half_edge,centerY-half_edge+d,n)
        xpoints[3*n:4*n] = np.linspace(centerX+half_edge,centerX-half_edge+d,n)
        ypoints[3*n:4*n] = centerY - half_edge

        boundaryPoints = np.zeros((nPoints+1,3))
        for i in range(nPoints):
            boundaryPoints[i][0] = xpoints[i]
            boundaryPoints[i][1] = ypoints[i]
            boundaryPoints[i][2] = zpoints[i]
        boundaryPoints[-1][:] = boundaryPoints[0][:]
        return boundaryPoints


# def boundary_square(nPoints)


def boundary_points_function2(nPoints,boundary_type='circle',boundary_radius=1500.,boundary_center=np.array([0.,0.,0.])):

    return [np.array([boundary_radius*np.cos(a), boundary_radius*np.sin(a), 0])-boundary_center for a in np.linspace(0, 2*np.pi, nPoints)]


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
                            yaw,boundaryPoints,num=0,wake_model='gaussian',args=False,nDIVS=np.array([200,200,25],dtype=int),save_path="/Users/ningrsrch/Dropbox/Projects/wind-farm-utilities/temps"):
    print 'starting call_julia_visualize'
    nTurbines = len(turbineX)
    globalYaw = (-yaw+wind_direction)+90.
    turbineXw,turbineYw = WindFrame(wind_direction,turbineX,turbineY)
    sorted_x_idx = np.argsort(turbineXw, kind='heapsort')

    if wake_model=='floris':
        print 'defining floris wrapped wake model'

        def wrapped_wake_model(loc):
            yaw=False
            Ct=False
            kd=0.15
            bd=-0.01
            initialWakeDisplacement=-4.5
            useWakeAngle=False
            initialWakeAngle=1.5
            ke=0.065
            adjustInitialWakeDiamToYaw=False
            MU=np.array([0.5, 1.0, 5.5])
            useaUbU=True
            aU=5.0
            bU=1.66
            me=np.array([-0.5, 0.22, 1.0])
            cos_spread=1.e+12
            Region2CT=0.888888888889
            axialInduction=False
            keCorrCT=0.0
            keCorrArray=0.0
            axialIndProvided=True
            shearCoefficientAlpha=0.10805
            shearZh=50.

            """wind shear"""
            Uref = wind_speed
            z = hubHeight
            zref = 50.
            z0 = 0.
            shearExp = 0.08

            windSpeeds = np.zeros(nTurbines)+wind_speed

            # for turbine_id in range(nTurbines):
            #     windSpeeds[turbine_id] = Uref*((z[turbine_id]-z0)/(zref-z0))**shearExp

            """floris wake model"""
            velX,velY = WindFrame(wind_direction, loc[0], loc[1])
            velZ = loc[2]

            if yaw == False:
                yaw = np.zeros(nTurbines)
            if axialInduction == False:
                axialInduction = np.ones(nTurbines)*1./3.
            if Ct == False:
                Ct = np.ones(nTurbines)*4.0*1./3.*(1.0-1./3.)

            # yaw wrt wind dir.
            yawDeg = yaw

            # wsPositionXYZw = np.zeros([3, nSamples])
            velX,velY = WindFrame(wind_direction, loc[0], loc[1])
            velZ = loc[2]
            wsPositionXYZw = np.array([velX,velY,velZ])

            # call to fortran code to obtain output values
            _, ws_array, _, _, _, _ = \
                        _floris.floris(turbineXw, turbineYw, hubHeight, yawDeg, rotorDiameter, windSpeeds,
                                                       Ct, axialInduction, ke, kd, me, initialWakeDisplacement, bd,
                                                       MU, aU, bU, initialWakeAngle, cos_spread, keCorrCT,
                                                       Region2CT, keCorrArray, useWakeAngle,
                                                       adjustInitialWakeDiamToYaw, axialIndProvided, useaUbU, wsPositionXYZw,
                                                       shearCoefficientAlpha, shearZh)

            wind_direction_rad = np.deg2rad(270.-wind_direction)
            s = ws_array[0]
            x = s*np.cos(wind_direction_rad)
            y = s*np.sin(wind_direction_rad)
            z = 0.
            return np.array([x,y,z])

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

        print 'defining gaussian wrapped wake model'
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

            wind_direction_rad = np.deg2rad(270.-wind_direction)
            s = ws_array[0]
            x = s*np.cos(wind_direction_rad)
            y = s*np.sin(wind_direction_rad)
            z = 0.
            return np.array([x,y,z])

        def dummy_func(loc):
            return np.array([1.,1.,1.])


    nDIVSx = nDIVS[0]
    nDIVSy = nDIVS[1]
    nDIVSz = nDIVS[2]
    print 'calling pyJulia'
    j = julia.Julia()
    # print 'include WFVisual'
    # generate_windfarm = j.include("WFVisual.jl")
    print 'set path'
    j.eval('include("/Users/ningrsrch/Dropbox/Projects/wind-farm-utilities/src/WFVisual.jl")')
    print 'using'
    j.using("WFVisual")
    # print 'rotorDiameter: ', rotorDiameter
    # print 'hubHeight: ', hubHeight
    # print 'nBlades: ', nBlades
    # print 'turbineX: ', turbineX
    # print 'turbineY: ', turbineY
    # print 'turbineZ: ', turbineZ
    # print 'globalYaw: ', globalYaw
    # print 'boundaryPoints: ', boundaryPoints
    # X = np.array([rotorDiameter, hubHeight, nBlades, turbineX, turbineY, turbineZ,globalYaw, boundaryPoints, dummy_func])
    print 'run function'

    perimeter = [ [p for p in point] for point in boundaryPoints]

    # print 'perimeter: ', perimeter

    # X = [1.0, 180.0, 1.0]
    # Y = [0.2, 0.3, 0.9, 1.9]
    # Xout = j.dummyfun(X,Y)
    # print(Xout)

    # j.dummyfun2(rotorDiameter, hubHeight, nBlades, turbineX, turbineY, turbineZ,globalYaw, perimeter)

    # print X
    # j.generate_windfarm(rotorDiameter, hubHeight, nBlades, turbineX, turbineY, turbineZ,globalYaw, perimeter,save_path=save_path)
    j.generate_windfarm(rotorDiameter, hubHeight, nBlades, turbineX, turbineY, turbineZ,globalYaw, perimeter, wrapped_wake_model, z_max=230., NDIVSx=nDIVSx, NDIVSy=nDIVSy, NDIVSz=nDIVSz,num=num,save_path=save_path)
    # j.generate_windfarm((rotorDiameter), (hubHeight), (nBlades), (turbineX), (turbineY), (turbineZ),(globalYaw), (boundaryPoints), dummy_func)
    # j.eval('import WFVisual')
    # j.eval('WFVisual.generate_windfarm')
    # print 'WFVisual: ', WFVisual
    # j.include("/Users/ningrsrch/Dropbox/Projects/wind-farm-utilities/src/WFVisual.jl")
    # print 'import WFVisual '
    # j.eval("importall WFVisual")
    # generate_windfarm = j.eval("generate_windfarm")

    # print rotorDiameter, hubHeight, nBlades, turbineX, turbineY, turbineZ,\
    #                               globalYaw, boundaryPoints,\
    #                               wrapped_wake_model
    # print 'wrapped_wake_model: ', wrapped_wake_model
    # print 'call generate_windfarm'
    # print generate_windfarm
    # j.eval("generate_windfarm(rotorDiameter, hubHeight, nBlades, turbineX, turbineY, turbineZ,globalYaw, boundaryPoints,dummy_func)")#,
                                 # NDIVSx=NDIVSx, NDIVSy=NDIVSy, NDIVSz=NDIVSz,
                                  #save_path=save_path)


        # loc = np.array([0.,0.,100.])
        # ws = wrapped_wake_model(loc)
        # print 'vectored speed: ', ws
        # print 'speed magnitude: ', np.linalg.norm(ws)

        # """quick visualization of the wakes in 2D"""
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
