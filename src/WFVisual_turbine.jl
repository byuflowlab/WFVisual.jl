#=##############################################################################
# DESCRIPTION
    Methods for generating a wind turbine geometry.
# AUTHORSHIP
  * Author    : Eduardo J Alvarez
  * Email     : Edo.AlvarezR@gmail.com
  * Created   : Jul 2018
  * License   : MIT License
=###############################################################################

################################################################################
# WIND TURBINE
################################################################################
"""
`generate_windturbine(Rtip::Float64, h::Float64, blade_name::String,
                              hub_name::String, tower_name::String;
                              nblades::Int64=3, data_path::String=def_data_path,
                              save_path=nothing, file_name="windturbine",
                              paraview=true)`

  Generates and returns a WindTurbine object scaled by `Rtip` with a tower of
height `h`, where the blade will be read from the `blade_name.jld` in
`data_path` containing the TriangularGrid geometry of the blade, samething for
`hub_name` and `tower_name`.

See the notebook under `docs/geometry_processing` for an example on how to
generate these files.
"""
function generate_windturbine(Rtip::Float64, h::Float64, blade_name::String,
                              hub_name::String, tower_name::String;
                              nblades::Int64=3, data_path::String=def_data_path,
                              save_path=nothing, file_name="windturbine",
                              paraview=true,
                              rot=nothing, random_rot::Bool=true, pitch=70)

  # Read gridded geometries
  blade_grid = JLD.load(joinpath(data_path, blade_name*".jld"), "blade_grid")
  hub_grid, Rhub, Thub = JLD.load(joinpath(data_path, hub_name*".jld"),
                                                    "hub_grid", "Rhub", "Thub")
  tower_grid = JLD.load(joinpath(data_path, tower_name*".jld"), "tower_grid")
  # Scales dimensions by Rtip
  blade_grid.orggrid.nodes .*= Rtip
  hub_grid.orggrid.nodes .*= Rtip
  for i in 1:size(tower_grid.orggrid.nodes, 2)
    # println([Rtip, h, Rtip])
    tower_grid.orggrid.nodes[:, i] .*= [Rtip, h, Rtip]
      # println(tower_grid.orggrid.nodes[:, i])
  end
  Rhub *= Rtip
  Thub *= Rtip


  # Rotor center
  C = [Thub*5/12, 0, h+Rhub/2]

  # Initiates rotor multigrid
  rotor = gt.MultiGrid(3)

  # Aligns and add hub to rotor
  gt.lintransform!(hub_grid, gt.rotation_matrix(0, 90, 0), zeros(3))
  gt.addgrid(rotor, "hub", hub_grid)

  # Pitches the blade
  gt.lintransform!(blade_grid, gt.rotation_matrix(0, -pitch, 0), zeros(3))

  # Rotates the rotor
  if rot != nothing
    gt.lintransform!(blade_grid, gt.rotation_matrix(0, 0, rot), zeros(3))
  elseif random_rot
    gt.lintransform!(blade_grid, gt.rotation_matrix(0, 0, rand()*360), zeros(3))
  end

  # Creates every blade and adds them to the rotor
  gt.lintransform!(blade_grid, gt.rotation_matrix(0, 0, -90), zeros(3))
  rotM = gt.rotation_matrix(0, 0, 360/nblades)
  for i in 1:nblades
    this_blade = deepcopy(blade_grid)
    gt.lintransform!(this_blade, eye(3), [-Thub*5/6, 0, 0])
    gt.addgrid(rotor, "blade$i", this_blade)

    gt.lintransform!(blade_grid, rotM, zeros(3))
  end

  # Starts multigrid of the wind turbine
  windturbine = gt.MultiGrid(3)

  # Aligns and adds tower
  gt.lintransform!(tower_grid, gt.rotation_matrix(0, 0, -90), zeros(3))
  gt.addgrid(windturbine, "tower", tower_grid)

  # Translates and adds rotor
  # gt.lintransform!(rotor, eye(3), C-*[Thub/2, 0, 0])
  gt.lintransform!(rotor, eye(3), C)
  gt.addgrid(windturbine, "rotor", rotor)

  if save_path!=nothing
    gt.save(windturbine, file_name; path=save_path)

    if paraview
      strn = ""
      strn *= file_name*"_tower.vtk;"
      strn *= file_name*"_rotor_hub.vtk;"
      for i in 1:nblades
        strn *= file_name*"_rotor_blade$i.vtk;"
      end

      run(`paraview --data=$save_path/$strn`)
    end

  end

  return windturbine::gt.MultiGrid
end


"""
`generate_loft(bscale::Real, b_low::Real, b_up::Real, b_NDIVS::Int64,
                        chords::Array{T,2}, twists::Array{T,2},
                        LE_x::Array{T,2}, LE_z::Array{T,2},
                        airfoils::Array{Tuple{T,Array{T,2}}, 1};
                        # MORE GEOMETRIC OPTIONS
                        tilt_z=nothing,
                        # SPLINE OPTIONS
                        spline_k::Int64=5, spline_bc::String="extrapolate",
                        spline_s::Real=0.001, verify_spline::Bool=true,
                        # OUTPUT OPTIONS
                        save_path=nothing, paraview::Bool=true,
                        file_name::String="myloft"
                       ) where{T<:Real}`

  Generates a lofted geometry.

  **Arguments**
  * `bscale::Float64`         : Semi-span scale.
  * `b_low::Float64`          : Scaled low bound of the span.
  * `b_up::Float64`           : Scaled upper bound of the span. To generate
                                a symmetric wing, give it b_low=-1, b_up=1; for
                                a semi-span, give it b_low=0, b_up=1. All
                                y/bscale value in the following arguments must
                                go from 0 to 1.
  * `b_NDIVS::Int64`          : Number of division along span.
  * `chords::Array{Float64,2}`: Chord distribution along the span in the form
                                [(y/bscale, c/bscale)].
  * `twists::Array{Float64,2}`: Twist distribution along the span in the form
                                [(y/bscale, deg)].
  * `LE_x::Array{Float64,2}`  : x-position (chordwise) of leading edge along the
                                span in the form [(y/bscale, x/bscale)].
  * `LE_z::Array{Float64,2}`  : z-position (dihedral-wise) of leading edge along
                                the span in the form [(y/bscale, z/bscale)].
  * `airfoils`                : Airfoil cross sections along the span in the
                                form [(y/bscale, airfoil_contour)], where
                                `airfoil_contour` is a matrix that contains
                                all points of the airfoil contour indexed by row.

  **Optional Arguments**
  * `tilt_z::{Array{Float64,2}}`            : Tilting about the z-axis of
                                              every span cross section in the
                                              form [(y/bscale, deg)].
  * `spline_k`, `spline_bc`, `spline_s`     : Spline parameters.

"""
function generate_loft(bscale::Real, b_low::Real, b_up::Real, b_NDIVS::Int64,
                        chords::Array{T,2}, twists::Array{T,2},
                        LE_x::Array{T,2}, LE_z::Array{T,2},
                        airfoils::Array{Tuple{T,Array{T,2}}, 1};
                        # MORE GEOMETRIC OPTIONS
                        tilt_z=nothing,
                        # SPLINE OPTIONS
                        spline_k::Int64=5, spline_bc::String="extrapolate",
                        spline_s::Real=0.001, verify_spline::Bool=true,
                        # OUTPUT OPTIONS
                        save_path=nothing, paraview::Bool=true,
                        file_name::String="myloft"
                       ) where{T<:Real}

  rfl_NDIVS = size(airfoils[1][2], 1)-1
  for (pos, rfl) in airfoils
    if rfl_NDIVS!=size(rfl,1)-1
      error("All airfoil sections must have the same number of points.")
    end
  end

  # ----------------- PARAMETRIC GRID ------------------------------------------
  P_min = [0, b_low, 0]            # Lower boundary arclength, span, dummy
  P_max = [1, b_up, 0 ]            # Upper boundary arclength, span, dummy
  loop_dim = 1                     # Loops the arclength dimension

  # Adds dummy division
  NDIVS = [rfl_NDIVS, b_NDIVS, 0]

  # Generates parametric grid
  grid = gt.Grid(P_min, P_max, NDIVS, loop_dim)


  # ----------------- GEOMETRY SPLINES -----------------------------------------
  # Splines all distributions for a smooth geometry
  _spl_chord = Dierckx.Spline1D(chords[:, 1], chords[:, 2];
                      k= size(chords,1)>=spline_k ? spline_k : size(chords,1)-1,
                                s=spline_s, bc=spline_bc)
  _spl_twist = Dierckx.Spline1D(twists[:, 1], twists[:, 2];
                      k= size(twists,1)>=spline_k ? spline_k : size(twists,1)-1,
                                s=spline_s, bc=spline_bc)
  _spl_LE_x = Dierckx.Spline1D(LE_x[:, 1], LE_x[:, 2];
                      k= size(LE_x,1)>=spline_k ? spline_k : size(LE_x,1)-1,
                                s=spline_s, bc=spline_bc)
  _spl_LE_z = Dierckx.Spline1D(LE_z[:, 1], LE_z[:, 2];
                      k= size(LE_z,1)>=spline_k ? spline_k : size(LE_z,1)-1,
                                s=spline_s, bc=spline_bc)
  if tilt_z!=nothing
    _spl_tlt_z = Dierckx.Spline1D(tilt_z[:, 1], tilt_z[:, 2];
                      k= size(tilt_z,1)>=spline_k ? spline_k : size(tilt_z,1)-1,
                                s=spline_s, bc=spline_bc)
  end

  # ----------------- SPLINE VERIFICATION --------------------------------------
  if verify_spline
    nnodesspan = gt.get_ndivsnodes(grid)[2]    # Number of nodes along span
    y_poss = [gt.get_node(grid, [1,i])[2] for i in 1:nnodesspan]  # Span positions

    fig = plt.figure("spl_verif", figsize=(7*2,5*1))

    plt.subplot(121)
    plt.plot(LE_x[:,1], LE_x[:,2], "og", label="Org LE x", alpha=0.5)
    plt.plot(LE_z[:,1], LE_z[:,2], "ob", label="Org LE z", alpha=0.5)
    plt.plot(y_poss, [_spl_LE_x(y) for y in y_poss], "--g", label="Spline LE x")
    plt.plot(y_poss, [_spl_LE_z(y) for y in y_poss], "--b", label="Spline LE z")
    plt.xlabel(plt.L"y/b_{scale}")
    plt.ylabel(plt.L"x/b_{scale}, z/b_{scale}")
    plt.grid(true, color="0.8", linestyle="--")
    plt.legend(loc="best")

    plt.subplot(122)
    p1 = plt.plot(twists[:,1], twists[:,2], "og", label="Org Twist", alpha=0.5)
    p2 = plt.plot(y_poss, [_spl_twist(y) for y in y_poss], "--g",
                                                          label="Spline twist")
    pextra = []
    if tilt_z!=nothing
      pextra1 = plt.plot(tilt_z[:,1], tilt_z[:,2], "or", label="Org tilt z",
                                                                      alpha=0.5)
      pextra2 = plt.plot(y_poss, [_spl_tlt_z(y) for y in y_poss], "--r",
                                                          label="Spline tilt z")
      pextra = vcat(pextra, [pextra1[1], pextra2[1]])
    end
    plt.ylabel("Twist (deg)")

    plt.grid(true, color="0.8", linestyle="--")
    plt.xlabel(plt.L"y/b_{scale}")

    plt.twinx()
    p3 = plt.plot(chords[:,1], chords[:,2], "ob", label="Org Chord", alpha=0.5)
    p4 = plt.plot(y_poss, [_spl_chord(y) for y in y_poss], "--b",
                                                          label="Spline chord")
    plt.ylabel(plt.L"c/b_{scale}")

    ps = vcat([p1[1], p2[1], p3[1], p4[1]], pextra)
    plt.legend(ps, [p[:get_label]() for p in ps], loc="best")
  end

  # ----------------- SURFACE GRID ---------------------------------------------
  # Auxiliary function for weighting values across span
  function calc_vals(span, array)

    # Finds bounding airfoil position
    val_in, val_out = nothing, array[1]
    for val in array[2:end]
        val_in = val_out
        val_out = val
        if val[1]>=abs(span); break; end
    end
    pos_in = val_in[1]
    val_in = val_in[2]
    pos_out = val_out[1]
    val_out = val_out[2]

    weight = (abs(span)-pos_in)/(pos_out-pos_in)

    return weight, val_in, val_out
  end

  # Space transformation function
  function my_space_transform(X, inds)
    span = X[2]                     # y/bscale span position
    chord = _spl_chord(abs(span))   # c/bscale chord length
    twist = _spl_twist(abs(span))   # twist
    le_x = _spl_LE_x(abs(span))     # x/bscale LE position
    le_z = _spl_LE_z(abs(span))     # z/bscale LE position

    # Merges airfoil contours at this span position
    weight, rfl_in, rfl_out = calc_vals(span, airfoils)

    # Point over airfoil contour
    point = weight*rfl_out[inds[1], :]+(1-weight)*rfl_in[inds[1], :]
    point = vcat(point, 0)

    # Scales the airfoil contour by the normalized chord length
    point = chord*point

    # Applies twist to the airfoil point
    tlt_z = tilt_z!=nothing ?  _spl_tlt_z(abs(span)) : 0.0
    point = gt.rotation_matrix(-twist, -tlt_z, 0)*point

    # Places the point relative to LE and scales by span scale
    point = [point[1]+le_x, span+point[3], point[2]+le_z]*bscale


    return point
  end

  # Transforms the quasi-two dimensional parametric grid into the wing surface
  gt.transform3!(grid, my_space_transform)

  # Splits the quadrialateral panels into triangles
  dimsplit = 2              # Dimension along which to split
  triang_grid = gt.GridTriangleSurface(grid, dimsplit)

  if save_path!=nothing
    # Outputs a vtk file
    gt.save(triang_grid, file_name; path=save_path)

    # Outputs a jld file
    JLD.save(joinpath(save_path, "$file_name.jld"), "triang_grid", triang_grid)

    if paraview
      # Calls paraview
      run(`paraview --data=$save_path$file_name.vtk`)
    end
  end

  return triang_grid
end

"""
  `generate_blade(Rtip, Rhub, r_NDIVS, blade_name; data_path=def_data_path,
    optargs...)`

  Reads the blade geometry in the data path under `blade_name`, and generates
a lofted geometry of the blade. Returns a TriangularGrid object of the geometry.

  **Arguments**
  * `Rtip::Float64`           : Blade radius.
  * `Rhub::Float64`           : Hub radius.
  * `r_NDIVS::Float64`        : Number of divisions along blade.
  * `blade_name::String`      : Blade geometry identifier.

"""
function generate_blade(Rtip::Real, Rhub::Real, r_NDIVS::Int64,
                        blade_name::String; data_path::String=def_data_path,
                        optargs...)

  # Reads all data
  data_airfoil = CSV.read(joinpath(data_path, blade_name*"_airfoilsections.csv"))
  data_chord = CSV.read(joinpath(data_path, blade_name*"_chord.csv"))
  data_twist = CSV.read(joinpath(data_path, blade_name*"_twist.csv"))
  data_lex = CSV.read(joinpath(data_path, blade_name*"_lex.csv"))
  data_lez = CSV.read(joinpath(data_path, blade_name*"_lez.csv"))

  airfoils = Tuple{Float64, Array{Float64, 2}}[]
  for i in 1:size(data_airfoil, 1)
    pos = data_airfoil[1][i]
    file_name = blade_name*"_"*data_airfoil[2][i]

    # rfl_contour = Array(CSV.read(joinpath(data_path, "airfoils/$file_name")))
    rfl_contour = CSV.read(joinpath(data_path, "airfoils/$file_name"))

    # Convert DataFrames to Arrays
    rfl_contour = hcat(rfl_contour[1], rfl_contour[2])
    rfl_contour = [val for val in rfl_contour]

    push!(airfoils, (pos, rfl_contour))
  end

  # Convert DataFrames to Arrays
  data_chord = hcat(data_chord[1], data_chord[2])
  data_twist = hcat(data_twist[1], data_twist[2])
  data_lex = hcat(data_lex[1], data_lex[2])
  data_lez = hcat(data_lez[1], data_lez[2])

  # Get rid of the Missing type
  data_chord = [val for val in data_chord]
  data_twist = [val for val in data_twist]
  data_lex = [val for val in data_lex]
  data_lez = [val for val in data_lez]

  return generate_loft(Rtip, Rhub/Rtip, 1.0, r_NDIVS, data_chord,
                  data_twist, data_lex, data_lez,
                  airfoils; file_name=blade_name, optargs...)
end
# ------------ END OF WIND TURBINE ---------------------------------------------
