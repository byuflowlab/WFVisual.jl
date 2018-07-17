import numpy as np
from openmdao.api import Group, Component, IndepVarComp, pyOptSparseDriver
import matplotlib.pyplot as plt
from wakeexchange.GeneralWindFarmComponents import *
from wakeexchange.GeneralWindFarmGroups import *
from wakeexchange.gauss import *
# from generalFunctions import *
from FLORISSE3D.setupOptimization import amaliaRose
from visualize import *

if __name__=="__main__":

    windDirections, windFrequencies, windSpeeds = amaliaRose(30)
    nDirections = len(windDirections)

    rotor_diameter = 100.
    farm_radius = 1500.
    hub_height = 100.
    rated_power = 3500.

    nTurbines = 25
    turbineX = np.array([  909.98349606,  1005.0174903 ,   900.40238835,  -479.57607866,
             937.92551703,   461.20472344,   123.06165965, -1073.3529325 ,
            -698.76200523, -1083.53094471,  1365.9338773 ,   204.10557045,
             306.99725222,  -585.35767689,    10.9706543 ,   543.54927959,
             -20.50212678, -1313.07762466, -1327.00852816,   137.06316521,
            1378.99410072,  -645.66250771,  -535.7876181 ,  -100.66538419,
           -1331.29278587])
    turbineY = np.array([  500.59889721,  -974.65186327,    76.51586507,  1315.29789208,
            1039.37304649, -1321.85187113,  -300.57817461,  -765.82650713,
           -1213.14956771,   886.54973742,  -306.96866239,   194.51410928,
             735.69027357,    81.95252777,  -892.14222889,  -930.41798152,
             970.9117144 ,   398.75277565,    -3.52236011,  1393.27798468,
             241.61586052,  -791.92492366,   919.26560593, -1396.37638078,
            -433.19849727])

    turbineZ = np.ones(nTurbines)*hub_height
    rotorDiameter = np.ones(nTurbines)*rotor_diameter
    axialInduction = np.ones(nTurbines)*1./3.
    generatorEfficiency = np.ones(nTurbines)
    air_density = 1.225
    rated_power = np.ones(nTurbines)*rated_power
    Ct_in = np.ones(nTurbines)*8./9.
    Cp_in = np.ones(nTurbines)*0.45

    differentiable = True

    expansion_factors = np.array([3, 2.75, 2.5, 2.25, 2.0, 1.75, 1.5, 1.25, 1.0])
    wake_combination_method = 1
    ti_calculation_method = 4
    ti_opt_method = 0
    if ti_calculation_method == 0:
        calc_k_star_calc = False
    else:
        calc_k_star_calc = True
    if ti_opt_method == 0:
        calc_k_star_opt = False
    else:
        calc_k_star_opt = True
    nRotorPoints = 1
    TI = 0.10817009629252423
    k_calc = 0.3837 * TI + 0.003678
    shear_exp = 0.30665565
    air_density = 1.1716
    wake_model_options = {'nSamples': 0,
                          'nRotorPoints': nRotorPoints,
                          'use_ct_curve': False,
                          # 'ct_curve': ct_curve,
                          'interp_type': 1,
                          'differentiable': differentiable}

    prob = Problem()
    prob.root = Group()

    prob.root.add('AEP', AEPGroup(nTurbines=nTurbines, nDirections=nDirections,nSamples=0,
                                              differentiable=differentiable,
                                              use_rotor_components=False,
                                              wake_model=gauss_wrapper,
                                              params_IdepVar_func=add_gauss_params_IndepVarComps,
                                              params_IndepVar_args={'nRotorPoints': nRotorPoints},
                                              wake_model_options=wake_model_options,
                                              rec_func_calls=True),promotes=['*'])

    prob.root.add('Boundary', BoundaryComp(nTurbines,1), promotes=['*'])
    prob.root.add('Spacing', SpacingComp(nTurbines), promotes=['*'])

    prob.setup()

    prob['windDirections'] = windDirections
    prob['windSpeeds'] = windSpeeds
    prob['windFrequencies'] = windFrequencies

    prob['turbineY'] = turbineY
    prob['turbineX'] = turbineX
    prob['hubHeight'] = turbineZ

    prob['rotorDiameter'] = rotorDiameter
    prob['axialInduction'] = axialInduction
    prob['generatorEfficiency'] = generatorEfficiency
    prob['air_density'] = air_density
    prob['rated_power'] = rated_power
    prob['Ct_in'] = Ct_in
    prob['Cp_in'] = Cp_in

    prob['boundary_radius'] = farm_radius
    prob['boundary_center'] = (0.,0.)

    prob['model_params:wake_combination_method'] = wake_combination_method
    prob['model_params:ti_calculation_method'] = ti_calculation_method
    prob['model_params:wake_model_version'] = 2016
    prob['model_params:opt_exp_fac'] = 1.0
    prob['model_params:calc_k_star'] = calc_k_star_calc
    prob['model_params:sort'] = True
    prob['model_params:z_ref'] = hub_height
    prob['model_params:z_0'] = 0.
    prob['model_params:ky'] = k_calc
    prob['model_params:kz'] = k_calc
    prob['model_params:print_ti'] = False
    prob['model_params:shear_exp'] = shear_exp
    prob['model_params:I'] = TI

    prob.run()
    print 'AEP: ', prob['AEP']

    turbine_x = prob['turbineX']
    turbine_y = prob['turbineY']
    turbine_z = np.zeros(nTurbines)
    hub_height = prob['hubHeight']
    rotor_diameter = prob['rotorDiameter']
    wind_direction = prob['windDirections'][np.argmax(prob['windFrequencies'])]
    wind_speed = prob['windSpeeds'][np.argmax(prob['windFrequencies'])]
    nBlades = np.ones(nTurbines,dtype=int)*3
    yaw = prob['yaw%s'%(np.argmax(prob['windFrequencies']))]
    boundary_points = boundary_points_function(25,boundary_radius=farm_radius)
    # wake_function

    # print 'turbine_x = np.', repr(turbine_x)
    # print 'turbine_y = np.', repr(turbine_y)
    # print 'turbine_z = np.', repr(turbine_z)
    # print 'hub_height = np.', repr(hub_height)
    # print 'rotor_diameter = np.', repr(rotor_diameter)
    # print 'wind_direction =', repr(wind_direction)
    # print 'nBlades = np.', repr(nBlades)
    # print 'yaw = np.', repr(yaw)
    # print 'boundary_points = np.', repr(boundary_points)
    # print 'boundary_x = np.', repr(boundary_x)
    # print 'boundary_y = np.', repr(boundary_y)
    # print 'boundary_z = np.', repr(boundary_z)

    call_julia_visualize(turbine_x,turbine_y,turbine_z,rotor_diameter,hub_height,nBlades,wind_direction,wind_speed,
                                yaw,boundary_points,wake_model='gaussian',args=False)


    # for i in range(nTurbines):
    #     turb = plt.Circle((turbine_x[i],turbine_y[i]),rotor_diameter[i]/2.,fc='blue',ec='none',alpha=0.25)
    #     plt.gca().add_patch(turb)
    # boundary = plt.Circle((0.,0.),farm_radius,fc='none',ec='black',linestyle='dashed')
    # plt.gca().add_patch(boundary)
    #
    # # plt.xlim(-farm_radius-2.*rotor_diameter[0],farm_radius+2.*rotor_diameter[0])
    # plt.ylim(-farm_radius-2.*rotor_diameter[0],farm_radius+2.*rotor_diameter[0])
    # plt.axis('equal')
    #
    # plt.show()
