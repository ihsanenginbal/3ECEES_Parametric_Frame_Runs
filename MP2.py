
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
        for FRO in f_ro:
            for FCO in f_concrete:
                for FST in f_steel:
                    for FSP in f_span:
                        for FGH in f_ground_height:
                            for FUH in f_upper_height:

                                current_analysis+=1
                                average_time=Elapsed_Time/current_analysis
                                remaining_time=(number_of_analysis-current_analysis)*average_time
                                print('Running on CPU #' + str(pid) + ' ' + str(round(current_analysis/number_of_analysis*10000)/100) + '% at the moment |---| Record Number=' + str(record_no) + ' |---| Analysis ' + str(current_analysis) + ' of total ' + str(int(number_of_analysis)) + ' |---| Remaining Time=' + str(remaining_time/60/60) + 'hours' )

                                fac=[FRO, FCO, FST, FSP, FGH, FUH]
                                os.wipe()

                                ################ Create ModelBuilder (2D and 3 DOF) #######################
                                os.model('basic','-ndm',2,'-ndf',3)

                                ##############################################################################
                                ##############################################################################
                                ## INPUT PARAMETERS                                                         ##
                                ##############################################################################
                                ##############################################################################

                                # Reinforcement diameters (mm)
                                fi8=8/1000*fac[0]
                                fi10=10/1000*fac[0]
                                fi12=12/1000*fac[0]
                                fi14=14/1000*fac[0]
                                fi16=16/1000*fac[0]
                                fi18=18/1000*fac[0]
                                fi20=20/1000*fac[0]
                                fi22=22/1000*fac[0]

                                # parameters for material properties
                                fc=-7000*fac[1]	    # Concrete Cylinder Characteristic Strength, kPa	(Reported by the field teams, based on the Schmidt's hammer - no core sampling was allowed in the severely damaged buildings)
                                K=1.10		    # Confinement Factor (see below explanation)
                                # [taken from SeismoStruct Help Menu-->]  K is the constant confinement factor, defined as the ratio between the
                                # confined and unconfined compressive stress of the concrete, and used to scale up the stress-strain relationship
                                # throughout the entire strain range. Although it may be computed through the use of any confinement model available
                                # in the literature [e.g. Ahmad and Sahad, 1982; Sheikh and Uzumeri, 1982; Eurocode 8, 1996; Penelis and Kappos, 1997],
                                # the use of the Mander et al. [1989] is recommended. Its value usually fluctuates between the values of 1.0 and 1.3
                                # for reinforced concrete members.

                                fy=370000*fac[2]	# Steel Strength, kPa (Median value from Akyuz and Uyan, 1992)
                                cover=0.03		    # m

                                #  Span Lengths (m) - centroid to centroid of columns
                                # Span lengths are increased with factor fac[3] for parametric analysis
                                Lengths=np.array([1.80, 3.20, 2.80, 3.10, 2.80])*fac[3]

                                # Clear length of left and right balconies in m (zero if doesnt exist)
                                Left_Right_Balconies=[1.50, 1.44]

                                # Unit area seismic weight of left and right balconies in kN/m2 (zero if doesnt exist)
                                LRB_weight=[8.4, 8.4]

                                #  Floor Heights (m)
                                # Ground floor height is set with factor fac[4]
                                # Upper (normal) floor heights are set with factor fac[5]
                                Heights=np.array([3.0/fac[5]*fac[4], 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0])*fac[5]
