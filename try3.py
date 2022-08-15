
import openseespy.opensees as os
import matplotlib.pyplot as plt
import math
import pickle
import os as osys
import numpy as np
import time

# Parametric analyses ranges
f_ro=[0.8, 1.0]
f_concrete=[0.75]
f_steel=[0.75]
f_span=[1.00]
f_ground_height=[1.00]	
f_upper_height=[1.00]

current_analysis=0

# Now read all the txt files transformed from the asc files, and run as many analyses
filelist=osys.listdir("GMfile/")

# OpenSeesPy Parallel commands ---------------------
#---------------------------------------------------
pid = os.getPID()
npC = os.getNP()
os.start()
# number of CPUs to be used in the parallel analysis
cpu_n=5

print('passed 1 with PID' + str(pid))
    
for filename in osys.listdir("GMfile/"):
    print('passed 2 with PID' + str(pid) ' at Current Anlysis: ' + str(current_analysis))
    
    if pid==current_analysis%cpu_n:
        print('passed 3 with PID' + str(pid) ' at Current Anlysis: ' + str(current_analysis))

        if filename.endswith(".txt"):
            print('passed 4 with PID' + str(pid) ' at Current Anlysis: ' + str(current_analysis))

            for FRO in f_ro:
                for FCO in f_concrete:
                    for FST in f_steel:
                        for FSP in f_span:
                            for FGH in f_ground_height:
                                for FUH in f_upper_height:

                                    print('passed 5 with PID' + str(pid) ' at Current Anlysis: ' + str(current_analysis))
                                    
                                    fac=[FRO, FCO, FST, FSP, FGH, FUH]
                                    
