
import openseespy.opensees as os
import matplotlib.pyplot as plt
import math
import pickle
import os as osys
import numpy as np
import time

from mpi4py import MPI
rank = MPI.COMM_WORLD.Get_rank()


# Parametric analyses ranges
f_ro=[0.8, 1.0]
f_concrete=[0.75, 1.00, 1.50]
f_steel=[0.75, 1.00, 1.50]
f_span=[1.00, 1.50]
f_ground_height=[1.00, 1.50]	
f_upper_height=[1.00]

current_analysis=0

filelist=osys.listdir("GMfile/")

number_of_analysis=len(filelist)/2*len(f_ro)*len(f_concrete)*len(f_steel)*len(f_span)*len(f_ground_height)*len(f_upper_height)


record_no=0

# OpenSeesPy Parallel commands ---------------------
#---------------------------------------------------
pid = os.getPID()
npC = os.getNP()
os.start()
# number of CPUs to be used in the parallel analysis
cpu_n=5

for filename in osys.listdir("GMfile/"):
    
    if filename.endswith(".txt"):
        record_no+=1
        for FRO in f_ro:
            for FCO in f_concrete:
                for FST in f_steel:
                    for FSP in f_span:
                        for FGH in f_ground_height:
                            for FUH in f_upper_height:

                                if rank==current_analysis%cpu_n:
                                #if 1==1:
                                    
                                    fac=[FRO, FCO, FST, FSP, FGH, FUH]

                                    print('Running on CPU #' + str(pid) + 'for the record ' + str(record_no) )
                                    
                                    current_analysis+=1
                                    

