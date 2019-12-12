import numpy as np
import os

# Load Julia v0.7 kernel
import julia
jl = julia.Julia(compiled_modules=False)

# NOTE: JLD and GeometricTools must be imported in this order, otherwise JLD
# will fail to read the pre-generated geometry saved as GeometricTools.Grid.
jl.eval('import JLD')
jl.eval('import GeometricTools')

# Path to this script
module_path = os.path.dirname(os.path.abspath(__file__))

# Load WFVisual module into Julia kernel
wfvisual_path = os.path.join(module_path, '..', 'src', 'WFVisual.jl')
jl.eval('include(\"'+wfvisual_path+'\")')

# Print Julia version for information
jl.versioninfo()

# Data path with geometry JLDs
data_path = os.path.join(module_path, '..', 'datav07')

# Create save path where to store vtks
save_path = os.path.join(module_path, '..', 'temps', 'pywindfarm00')

if os.path.isdir(save_path):
    os.rmdir(save_path)

os.mkdir(save_path)


# --------------------- WIND FARM LAYOUT ---------------------------------------
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

nBlades = np.array([3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                3, 3, 3, 3, 3])

wind_direction = 228.0

yaw = np.array([ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
        0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]) - wind_direction


# --------------------- PERIMETER AND FLUID DOMAIN -----------------------------
NDIVSx = 70              # Cells in the parametric x-direction
NDIVSy = 70              # Cells in the parametric y-direction
NDIVSz = 70              # Cells in the geometric z-direction

# Dummy perimeter
xlo = np.array([min(turbine_x), min(turbine_y)])
xup = np.array([max(turbine_x), max(turbine_y)])
Rper = np.linalg.norm(xup - xlo)/2.0*3.0/4.0
perimeter_points = [ np.array([Rper*np.cos(a), Rper*np.sin(a), 0.0]) for a in np.linspace(0, 2*np.pi, 179)]

# Dummy wake function
def wake(X):
    return 1.0*np.array([np.cos(wind_direction*np.pi/180), np.sin(wind_direction*np.pi/180), 0.0])

# --------------------- GENERATE WIND FARM -------------------------------------
jl.WFVisual.generate_windfarm(rotor_diameter, hub_height, nBlades,
                                turbine_x, turbine_y, turbine_z,
                                yaw,
                                perimeter_points, wake,
                                NDIVSx=NDIVSx, NDIVSy=NDIVSy, NDIVSz=NDIVSz,
                                save_path=save_path, spl_s=0.01,
                                data_path=data_path)
