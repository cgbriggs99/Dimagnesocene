#!/usr/bin/python3

"""
pes_maker
---------

Makes PES plots of the various parameters.
"""

import math
import pickle
import numpy as np
import matplotlib.pyplot as plot
import os

def plot_from_file(fname, *args, **kwargs) :
    """
plot_from_file
--------------

Plots the data in a file.
"""
    data = []
    with open(fname, "r") as fp :
        # All entries are doubles.
        while True :
            try :
                data.append([pickle.loads(fp.read(21)), pickle.loads(fp.read(21))])
            except Exception as e :
                break
    
    # These are set up as parameter-energy pairs.
    plot.plot([d[0] for d in data], [d[1] for d in data], *args, **kwargs)

# Set up plots.
if os.path.isfile("out/dimgce_rr.dat") :
    plot.figure(dpi = 200)
    plot_from_file("out/dimgce_rr.dat")
    plot.xlabel("Ring-Ring Distance (Å)")
    plot.ylabel("Energy (Hartree)")
    plot.title("Ring-Ring Distance Potential Energy Surface")
    plot.savefig("out/dimgce_rr.png")
    
if os.path.isfile("out/dimgce_mgmg.dat") :
    plot.figure(dpi = 200)
    plot_from_file("out/dimgce_mgmg.dat")
    plot.xlabel("Mg-Mg Distance (Å)")
    plot.ylabel("Energy (Hartree)")
    plot.title("Mg-Mg Bond Distance Potential Energy Surface")
    plot.savefig("out/dimgce_mgmg.png")

if os.path.isfile("out/dimgce_angle.dat") :
    plot.figure(dpi = 200)
    plot_from_file("out/dimgce_angle.dat")
    plot.xlabel("Rotation Angle (degrees)")
    plot.ylabel("Energy (Hartree)")
    plot.title("Cp-Cp Angle Potential Energy Surface")
    plot.savefig("out/dimgce_angle.png")
