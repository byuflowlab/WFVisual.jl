module_path = splitdir(@__FILE__)[1]            # Path to this file

# NOTE: In Julia v0.7, JLD throws the error "Cannot `convert` an object of type
# getfield(JLD, Symbol("##JLD.AssociativeWrapper" unless, imported outside of
# WFVisual through the following line. I'm not sure, but I think it's because
# JLD must be imported before GeometricTools to be able to read Grid JLDs.
# Also, notice that `generate_windfarm(...)` takes an abnormal long time to run
# in v0.7.
import JLD

# Load WFVisual module
import WFVisual
wfv=WFVisual

# Load GeometricTools: https://github.com/byuflowlab/GeometricTools.jl
import GeometricTools
gt=GeometricTools

# Data path with geometry JLDs
if Int(VERSION.major)==0 && Int(VERSION.minor)==6   # Case of Julia v0.6
    data_path = joinpath(module_path, "../data/")
else                                                # Case of Julia v0.7
    data_path = joinpath(module_path, "../datav07/")
end

# Create save path where to store vtks
save_path = "temps/windfarm06/"         # Save path of this example
gt.create_path(save_path, true)



# --------------------- WIND FARM LAYOUT ---------------------------------------
turbine_x = [  909.98349606,  1005.0174903 ,   900.40238835,  -479.57607866,
                 937.92551703,   461.20472344,   123.06165965, -1073.3529325 ,
                -698.76200523, -1083.53094471,  1365.9338773 ,   204.10557045,
                 306.99725222,  -585.35767689,    10.9706543 ,   543.54927959,
                 -20.50212678, -1313.07762466, -1327.00852816,   137.06316521,
                1378.99410072,  -645.66250771,  -535.7876181 ,  -100.66538419,
               -1331.29278587]

turbine_y = [  500.59889721,  -974.65186327,    76.51586507,  1315.29789208,
                1039.37304649, -1321.85187113,  -300.57817461,  -765.82650713,
               -1213.14956771,   886.54973742,  -306.96866239,   194.51410928,
                 735.69027357,    81.95252777,  -892.14222889,  -930.41798152,
                 970.9117144 ,   398.75277565,    -3.52236011,  1393.27798468,
                 241.61586052,  -791.92492366,   919.26560593, -1396.37638078,
                -433.19849727]
turbine_z = [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
                0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]

hub_height = [ 100.,  100.,  100.,  100.,  100.,  100.,  100.,  100.,  100.,
                100.,  100.,  100.,  100.,  100.,  100.,  100.,  100.,  100.,
                100.,  100.,  100.,  100.,  100.,  100.,  100.]

rotor_diameter = [ 100.,  100.,  100.,  100.,  100.,  100.,  100.,  100.,  100.,
                100.,  100.,  100.,  100.,  100.,  100.,  100.,  100.,  100.,
                100.,  100.,  100.,  100.,  100.,  100.,  100.]

nBlades = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
               3, 3]

wind_direction = 228.0

yaw = [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
        0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.] - wind_direction


# --------------------- PERIMETER AND FLUID DOMAIN -----------------------------
NDIVSx = 70              # Cells in the parametric x-direction
NDIVSy = 70              # Cells in the parametric y-direction
NDIVSz = 70              # Cells in the geometric z-direction

# Dummy perimeter
Rper = norm(maximum.([turbine_x, turbine_y]) - minimum.([turbine_x, turbine_y]))/2*3/4
perimeter_points = Rper*[ [cos(a), sin(a), 0] for a in linspace(0, 2*pi, 179)]

# Dummy wake function
wake(X) = 1.0*[cos(wind_direction*pi/180), sin(wind_direction*pi/180), 0]


# --------------------- GENERATE WIND FARM -------------------------------------

wfv.generate_windfarm(rotor_diameter, hub_height, nBlades,
                                turbine_x, turbine_y, turbine_z,
                                yaw,
                                perimeter_points, wake;
                                NDIVSx=NDIVSx, NDIVSy=NDIVSy, NDIVSz=NDIVSz,
                                save_path=save_path, spl_s=0.01,
                                data_path=data_path);

nothing
