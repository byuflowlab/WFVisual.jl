"""
  Methods for three-dimensional visualization of wind farm layout, wind turbine
  design, and wake models.

  # AUTHORSHIP
    * Author    : Eduardo J Alvarez
    * Email     : Edo.AlvarezR@gmail.com
    * Created   : Jul 2018
    * License   : MIT License
"""
module WFVisual
export generate_windfarm, dummyfun, dummyfun2


# ------------ GENERIC MODULES -------------------------------------------------
import JLD
import CSV
import Dierckx
import PyPlot
import PyCall

const plt = PyPlot

# ------------ FLOW MODULES ----------------------------------------------------
# https://github.com/byuflowlab/GeometricTools.jl
import GeometricTools
const gt = GeometricTools

# ------------ GLOBAL VARIABLES ------------------------------------------------
const module_path = splitdir(@__FILE__)[1]          # Path to this module
const def_data_path = joinpath(module_path, "../data")  # Path to data files

function dummyfun(X::Array{T,1},Y::Array{T,1}) where{T<:Real}

    println(typeof(X))
  return [X[1]*cos(X[2]*pi/180)+Y[1], X[1]*sin(X[2]*pi/180), X[3]]
end

function dummyfun2(args...)
    for arg in args
        println(typeof(args))
    end
end


# ------------ HEADERS ---------------------------------------------------------
for header_name in ["turbine", "farm"]
  include("WFVisual_"*header_name*".jl")
end

end # END OF MODULE
