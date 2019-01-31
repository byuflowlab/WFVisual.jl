#=##############################################################################
# DESCRIPTION
    Class of wind turbine geometry.
# AUTHORSHIP
  * Author    : Eduardo J Alvarez
  * Email     : Edo.AlvarezR@gmail.com
  * Created   : Jul 2018
  * License   : MIT License
=###############################################################################

################################################################################
# WIND FARM
################################################################################

# import JLD
# import CSV
# import Dierckx
# import PyPlot
# using PyCall
#
# const plt = PyPlot

# ------------ FLOW MODULES ----------------------------------------------------
# https://github.com/byuflowlab/GeometricTools.jl
# import GeometricTools
# const gt = GeometricTools

# include("WFVisual_turbine.jl")

using PyCall

"""
`generate_layout(D::Array{T,1}, H::Array{T,1}, N::Array{Int64,1},
                          x::Array{T,1}, y::Array{T,1}, z::Array{T,1},
                          glob_yaw::Array{T,1};
                          # TURBINE GEOMETRY OPTIONS
                          hub::Array{String,1}=String[],
                          tower::Array{String,1}=String[],
                          blade::Array{String,1}=String[],
                          data_path::String=def_data_path,
                          # FILE OPTIONS
                          save_path=nothing, file_name="windfarm",
                          paraview=true
                         ) where{T<:Real}`

  Generates and returns a wind farm layout consisting of a MultiGrid object
containing every turbine at the indicated position `x,y,z`, and the given
geometry `D,H,N` and orientation `glob_yaw`.

  **Arguments**
  * `D::Array{Float64,1}`         : Rotor diameter of every turbine.
  * `H::Array{Float64,1}`         : Tower height of every turbine.
  * `N::Array{Float64,1}`         : Number of blades of every turbine.
  * `x::Array{Float64,1}`         : x-position of the every turbine base.
  * `y::Array{Float64,1}`         : y-position of the every turbine base.
  * `z::Array{Float64,1}`         : z-position of the every turbine base.
  * `glob_yaw::Array{Float64,1}`  : Angle of the plane of rotation relative to
                                    the x-axis of the global coordinate system
                                    IN DEGREES.

"""
function generate_layout(D::Array{T,1}, H::Array{T,1}, N::Array{Int64,1},
                          x::Array{T,1}, y::Array{T,1}, z::Array{T,1},
                          glob_yaw::Array{T,1};
                          # TURBINE GEOMETRY OPTIONS
                          hub::Array{String,1}=String[],
                          tower::Array{String,1}=String[],
                          blade::Array{String,1}=String[],
                          data_path::String=def_data_path,
                          # FILE OPTIONS
                          save_path=nothing, file_name="windfarm",
                          paraview=true
                         ) where{T<:Real}

  nturbines = size(D, 1)        # Number of turbines

  # Default turbine geometry
  if size(hub,1)==0
    hub = ["hub" for i in 1:nturbines]
  end
  if size(tower,1)==0
    tower = ["tower1" for i in 1:nturbines]
  end
  if size(blade,1)==0
    blade = ["NREL5MW" for i in 1:nturbines]
  end

  # Generates layout
  windfarm = gt.MultiGrid(3)

  for i in 1:nturbines
    # Generate wind turbine geometry
    turbine = generate_windturbine(D[i]/2, H[i], blade[i], hub[i], tower[i];
                                    nblades=N[i], data_path=data_path,
                                    save_path=nothing)

    # Places it at the location and orientation
    Oaxis = gt.rotation_matrix(glob_yaw[i], 0, 0)
    gt.lintransform!(turbine, Oaxis, [x[i], y[i], z[i]])

    # Adds it to the farm
    gt.addgrid(windfarm, "turbine$i", turbine)
  end

  if save_path!=nothing
    gt.save(windfarm, file_name; path=save_path)

    if paraview
      strn = ""
      for i in 1:nturbines
        strn *= file_name*"_turbine$(i)_tower.vtk;"
        strn *= file_name*"_turbine$(i)_rotor_hub.vtk;"
        for j in 1:N[i]
          strn *= file_name*"_turbine$(i)_rotor_blade$(j).vtk;"
        end
      end

      run(`paraview --data=$save_path/$strn`)
    end

  end

  return windfarm::gt.MultiGrid
end

"""
`generate_perimetergrid(perimeter::Array{Array{T, 1}, 1},
                                  NDIVSx, NDIVSy, NDIVSz;
                                  z_min::Real=0, z_max::Real=0,
                                  # SPLINE OPTIONS
                                  verify_spline::Bool=true,
                                  spl_s=0.001, spl_k="automatic",
                                  # FILE OPTIONS
                                  save_path=nothing, file_name="perimeter",
                                  paraview=true
                                )`

  Generates the perimeter grid with `perimeter` the array of points of the
  contour (must be a closed contour), and `NDIVS_` the number of cells in
  each parametric dimension (give it `NDIVSz=0` for a flat surface, otherwise
  it'll generate a volumetric grid between `z_min` and `z_max`).
"""
function generate_perimetergrid(perimeter::Array{Array{T, 1}, 1},
                                  NDIVSx, NDIVSy, NDIVSz;
                                  z_min::Real=0, z_max::Real=0,
                                  # SPLINE OPTIONS
                                  verify_spline::Bool=true,
                                  spl_s=0.001, spl_k="automatic",
                                  # FILE OPTIONS
                                  save_path=nothing, file_name="perimeter",
                                  paraview=true
                                ) where{T<:Real}

  # Error cases
  multidiscrtype = Array{Tuple{Float64,Int64,Float64,Bool},1}
  if typeof(NDIVSx)==Int64
    nz = NDIVSz
  elseif typeof(NDIVSz)==multidiscrtype
    nz = 0
    for sec in NDIVSz
      nz += sec[2]
    end
  else
    error("Expected `NDIVSz` to be type $(Int64) or $MultiDiscrType,"*
            " got $(typeof(NDIVSz)).")
  end

  # --------- REPARAMETERIZES THE PERIMETER ---------------------------
  org_x = [p[1] for p in perimeter]
  org_y = [p[2] for p in perimeter]
  # Separate upper and lower sides to make the contour injective in x
  upper, lower = gt.splitcontour(org_x, org_y)
<<<<<<< HEAD
  #spl_s = 0.1
=======

  # # Parameterize both sides independently
  # fun_upper = gt.parameterize(upper[1], upper[2], zeros(upper[1]); inj_var=1,
  #                                                     s=spl_s, kspl=spl_k)
  # fun_lower = gt.parameterize(lower[1], lower[2], zeros(lower[1]); inj_var=1,
  #                                                     s=spl_s, kspl=spl_k)
  # # Discretizes both sides
  # if NDIVSx==multidiscrtype
  #   new_upper = gt.multidiscretize(fun_upper, 0, 1, NDIVSx)
  #   new_lower = gt.multidiscretize(fun_lower, 0, 1, NDIVSx)
  # else
  #   new_upper = gt.discretize(fun_upper, 0, 1, NDIVSx, 1.0)
  #   new_lower = gt.discretize(fun_lower, 0, 1, NDIVSx, 1.0)
  # end

  splt_up = Int(ceil((size(upper[1],1)/2)))
  splt_low = Int(ceil((size(lower[1],1)/2)))

  # Splits the perimeter into four faces
  upper1 = [[x for x in upper[1][1:splt_up]], [y for y in upper[2][1:splt_up]]]
  upper2 = [[x for x in upper[1][splt_up:end]], [y for y in upper[2][splt_up:end]]]
  lower1 = [[x for x in lower[1][1:splt_low]], [y for y in lower[2][1:splt_low]]]
  lower2 = [[x for x in lower[1][splt_low:end]], [y for y in lower[2][splt_low:end]]]

>>>>>>> 2bb010d26cb11d7eba9f48cd024c93003d2f0d65
  # Parameterize both sides independently
  fun_upper1 = gt.parameterize(upper1[1], upper1[2], zeros(upper1[1]); inj_var=1,
                                                      s=spl_s, kspl=spl_k)
  fun_upper2 = gt.parameterize(upper2[1], upper2[2], zeros(upper2[1]); inj_var=1,
                                                      s=spl_s, kspl=spl_k)
  fun_lower1 = gt.parameterize(lower1[1], lower1[2], zeros(lower1[1]); inj_var=1,
                                                      s=spl_s, kspl=spl_k)
  fun_lower2 = gt.parameterize(lower2[1], lower2[2], zeros(lower2[1]); inj_var=1,
                                                      s=spl_s, kspl=spl_k)
  # Discretizes both sides
  if NDIVSx==multidiscrtype
    new_upper1 = gt.multidiscretize(fun_upper1, 0, 1, NDIVSx)
    new_upper2 = gt.multidiscretize(fun_upper2, 0, 1, NDIVSy)
    new_lower1 = gt.multidiscretize(fun_lower1, 0, 1, NDIVSy)
    new_lower2 = gt.multidiscretize(fun_lower2, 0, 1, NDIVSx)
  else
    new_upper1 = gt.discretize(fun_upper1, 0, 1, NDIVSx, 1.0)
    new_upper2 = gt.discretize(fun_upper2, 0, 1, NDIVSy, 1.0)
    new_lower1 = gt.discretize(fun_lower1, 0, 1, NDIVSy, 1.0)
    new_lower2 = gt.discretize(fun_lower2, 0, 1, NDIVSx, 1.0)
  end

  # ----------------- SPLINE VERIFICATION --------------------------------------

  if verify_spline
  #   new_points = vcat(reverse(new_upper), new_lower)
    # new_x = [p[1] for p in new_points]
    # new_y = [p[2] for p in new_points]
    plt.plot(org_x, org_y, "--^k", label="Original", alpha=0.5)
    # plt.plot(new_x, new_y, ":.b", label="Parameterized")

    plt.plot(upper1[1], upper1[2], "*b", label="upper1", alpha=0.75)
    plt.plot(upper2[1], upper2[2], "^b", label="upper2", alpha=0.75)
    plt.plot(lower1[1], lower1[2], "*r", label="lower1", alpha=0.75)
    plt.plot(lower2[1], lower2[2], "^r", label="lower2", alpha=0.75)

    new_points = vcat(new_upper1, new_upper2)
    new_x = [p[1] for p in new_points]
    new_y = [p[2] for p in new_points]
    plt.plot(new_x, new_y, ":.b", label="Parameterized Upper", alpha=0.75)
    new_points = vcat(new_lower1, new_lower2)
    new_x = [p[1] for p in new_points]
    new_y = [p[2] for p in new_points]
    plt.plot(new_x, new_y, ":.r", label="Parameterized Lower", alpha=0.75)
    plt.xlabel(plt.L"x")
    plt.ylabel(plt.L"y")
    plt.legend(loc="best")
    plt.grid(true, color="0.8", linestyle="--")
  end


  # --------- GRIDS THE INSIDE OF THE PERIMETER ---------------------
  # Parametric grid
  P_min = zeros(3)
  P_max = [1, 1, 1*(nz!=0)]
  param_grid = gt.Grid(P_min, P_max, [NDIVSx, NDIVSy, NDIVSz])

  # function my_space_transform(X, ind)
  #     i = ind[1]                      # Arc length point
  #     w = X[2]                        # Weight
  #     z = z_min + X[3]*(z_max-z_min)  # z-position
  #
  #     Y = new_lower[i] + w*(new_upper[i]-new_lower[i])
  #     Y[3] = z
  #
  #     return Y
  # end

  rev_new_upper1 = reverse(new_upper1)
  rev_new_upper2 = reverse(new_upper2)
  rev_new_lower1 = reverse(new_lower1)
  rev_new_lower2 = reverse(new_lower2)

  function my_space_transform(X, ind)
      z = z_min + X[3]*(z_max-z_min)  # z-position

      xw = X[2]                # x weight
      yw = X[1]                # y weight

      x = new_upper1[ind[1]]*xw + new_lower2[ind[1]]*(1-xw)
      y = rev_new_upper2[ind[2]]*yw + rev_new_lower1[ind[2]]*(1-yw)
      # Y = x + y

      yw = abs(X[1]-0.5)/0.5
      yw = tan(yw*pi/2 - 1e-2)/tan(pi/2 - 1e-2)
      xw = abs(X[2]-0.5)/0.5
      xw = tan(xw*pi/2 - 1e-2)/tan(pi/2 - 1e-2)
      w = ( (1-xw) + yw ) /2
      Y = x*(1-w) + y*w

      Y[3] = z

      return Y
  end

  # Applies the space transformation to the parametric grid
  gt.transform3!(param_grid, my_space_transform)

  if save_path!=nothing
    gt.save(param_grid, file_name; path=save_path)

    if paraview
      strn = file_name*".vtk"
      run(`paraview --data=$save_path/$strn`)
    end

  end

  return param_grid::gt.Grid
end




function generate_windfarm(D::Array{T,1}, H::Array{T,1}, N::Array{Int64,1},
                          x::Array{T,1}, y::Array{T,1}, z::Array{T,1},
                          glob_yaw::Array{T,1}, _perimeter::Array{T, 2},
                          wake;
                          # TURBINE GEOMETRY OPTIONS
                          hub::Array{String,1}=String[],
                          tower::Array{String,1}=String[],
                          blade::Array{String,1}=String[],
                          data_path::String=def_data_path,
                          # PERIMETER AND FLUID DOMAIN OPTIONS
                          NDIVSx=50, NDIVSy=50, NDIVSz=50,
                          z_min="automatic", z_max="automatic",
                          # PERIMETER SPLINE OPTIONS
                          verify_spline::Bool=true,
                          spl_s=0.001, spl_k="automatic",
                          # FILE OPTIONS
                          save_path=nothing, file_name="mywindfarm",
                          paraview=true, num=nothing
                         ) where{T<:Real}
  perimeter = M2arr(_perimeter)
  windfarm = generate_layout(D, H, N, x, y, z, glob_yaw;
                                  hub=hub, tower=tower, blade=blade,
                                  data_path=data_path, save_path=nothing)

  perimeter_grid = generate_perimetergrid(perimeter, NDIVSx, NDIVSy, 0;
                                      verify_spline=verify_spline, spl_s=spl_s,
                                      spl_k=spl_k, save_path=nothing)

  _zmin = z_min=="automatic" ? 0 : z_min
  _zmax = z_max=="automatic" ? maximum(H) + 1.25*maximum(D)/2 : z_max
  fdom = generate_perimetergrid(perimeter,
                                    NDIVSx, NDIVSy, NDIVSz;
                                    z_min=_zmin, z_max=_zmax,
                                    verify_spline=false,
                                    spl_s=spl_s, spl_k=spl_k,
                                    save_path=nothing,
                                  )


  gt.calculate_field(fdom, wake, "wake", "vector", "node")


  if save_path!=nothing
    gt.save(windfarm, file_name; path=save_path, num=num)
    gt.save(perimeter_grid, file_name*"_perimeter"; path=save_path, num=num)
    gt.save(fdom, file_name*"_fdom"; path=save_path, num=num)

    if paraview
      strn = ""
      for i in 1:size(D,1)
        strn *= file_name*"_turbine$(i)_tower.vtk;"
        strn *= file_name*"_turbine$(i)_rotor_hub.vtk;"
        for j in 1:N[i]
          strn *= file_name*"_turbine$(i)_rotor_blade$(j).vtk;"
        end
      end

      strn *= file_name*"_perimeter.vtk;"
      strn *= file_name*"_fdom.vtk;"

      run(`paraview --data=$save_path/$strn`)
    end

  end

  return (windfarm, perimeter, fdom)
end

function M2arr(M::Array{T, 2}) where{T<:Real}
  return [ [p for p in M[i, :]] for i in 1:size(M,1) ]
end

# ------------ END OF WIND FARM ------------------------------------------------
