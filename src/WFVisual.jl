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
export generate_windfarm


# ------------ GENERIC MODULES -------------------------------------------------
using JLD
using CSV
using Dierckx
using PyPlot
using PyCall
using DataFrames
using LinearAlgebra

const plt = PyPlot

# ------------ FLOW MODULES ----------------------------------------------------
# https://github.com/byuflowlab/GeometricTools.jl
import GeometricTools
const gt = GeometricTools

# ------------ GLOBAL VARIABLES ------------------------------------------------
const module_path = splitdir(@__FILE__)[1]          # Path to this module
const def_data_path = joinpath(module_path, "../data")  # Path to data files

# ------------ HEADERS ---------------------------------------------------------
for header_name in ["turbine", "farm"]
  include("WFVisual_"*header_name*".jl")
end

end # END OF MODULE
