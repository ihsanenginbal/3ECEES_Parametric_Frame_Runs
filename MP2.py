import openseespy.opensees as os
import matplotlib.pyplot as plt
import math
import pickle
import os as osys
import numpy as np
import time



# Units: kN, m, sec
# -------------------------------------------------------------------------
# Code          : PFN - 8B - 1
# Explanation   : Poor-Frame-Emergent Beam from Bayrakli/Izmir set
# Source        : Building information from Bekir Ozer Ay (METU), from Bayrakli/Izmir, is used for generating frames,Ref:226431 / Ax 9.
#                       Bal et al., 2008 is also used for defining parametric ranges. 
# Number of Bays: 5 Bays
# Number of Str.: 8-Storey
# Author        : Dr. Eleni Smyrou (e.smyrou@pl.hanze.nl)
# Version check : v4.0 / 25.12.2021 - Parametric
# ------------------------------------------------------------------------

##############################################################################
##############################################################################
## PARAMETRIC ANALYSES PARAMETERS & LOOPS                                   ##
##############################################################################
##############################################################################

# Parametric analyses ranges
f_ro=[0.8, 1.0]
f_concrete=[0.75, 1.00, 1.50]
f_steel=[0.75, 1.00, 1.50]
f_span=[1.00, 1.50]
f_ground_height=[1.00, 1.50]	
f_upper_height=[1.00]

current_analysis=0

# Read the acceleration files (in txt format, single data column)
# In this example, the acceleration data are coming from AFAD / Turkey
# The ground motion files are in .asc format
# Ass .asc files are turned into single-column txt files
# and header lines are removed for use in OpenSees.


# Now read all the txt files transformed from the asc files, and run as many analyses
filelist=osys.listdir("GMfile/")

number_of_analysis=len(filelist)/2*len(f_ro)*len(f_concrete)*len(f_steel)*len(f_span)*len(f_ground_height)*len(f_upper_height)


record_no=0

pid = os.getPID()
npC = os.getNP()
os.start()
#if np != 11:
#    exit()
    
Elapsed_Time=30
start_time=time.time()
for filename in osys.listdir("GMfile/"):
    record_no+=1
    if filename.endswith(".txt"):
        print(filename + ' on CPU ' + str(pid))
    
        fac=[FRO, FCO, FST, FSP, FGH, FUH]
        os.wipe()
        os.model('basic','-ndm',2,'-ndf',3)
