## \file
## \ingroup tutorial_tdataframe
## \notebook -draw
## This tutorial shows the potential of the VecOps approach for treating collections
## stored in datasets, a situation very common in HEP data analysis.
##
## \macro_code
##
## \date February 2018
## \author Danilo Piparo

import ROOT

tdf = ROOT.Experimental.TDataFrame(1024)
coordDefineCode = '''ROOT::Experimental::VecOps::TVec<double> {0}(len);
                     std::transform({0}.begin(), {0}.end(), {0}.begin(), [](double){{return gRandom->Uniform(-1.0, 1.0);}});
                     return {0};'''
d = tdf.Define("len", "gRandom->Uniform(0, 16)")\
       .Define("x", coordDefineCode.format("x"))\
       .Define("y", coordDefineCode.format("y"))

# Now we have in hands d, a TDataFrame with two columns, x and y, which
# hold collections of coordinates. The size of these collections vary.
# Let's now define radii out of x and y. We'll do it treating the collections
# stored in the columns without looping on the individual elements.
d1 = d.Define("r", "sqrt(x*x + y*y)")

# Now we want to plot 2 quarters of a ring with radii .5 and 1
# Note how the cuts are performed on TVecs, comparing them with integers and
# among themselves
ring_h = d1.Define("rInFig", "r > .4 && r < .8 && x*y < 0")\
           .Define("yFig", "y[rInFig]")\
           .Define("xFig", "x[rInFig]")\
           .Histo2D(("fig", "Two quarters of a ring", 64, -1, 1, 64, -1, 1), "xFig", "yFig")

cring = ROOT.TCanvas()
ring_h.Draw("Colz")
cring.Print("tdf016_vecOps_py.png")
