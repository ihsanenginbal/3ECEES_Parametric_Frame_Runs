
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
                                
                                # Column Top Loads - kN (from bottom to top) - loads from transverse frames, excluding column self weights
                                # When the span lengths are increased with the factor fac[3], the transverse
                                # axis lengths are also assumed to be increased. The column top loads
                                # coming from the transverse beams are thus increased proportionally with factor fac[3]
                                N0=np.array([[-6.3, -1.8, -8.9, -8.9, -1.8, -6.3],
                                             [-6.3, -1.8, -8.9, -8.9, -1.8, -6.3],
                                             [-6.3, -1.8, -8.9, -8.9, -1.8, -6.3],
                                             [-6.3, -1.8, -8.9, -8.9, -1.8, -6.3],
                                             [-6.3, -1.8, -8.9, -8.9, -1.8, -6.3],
                                             [-6.3, -1.8, -8.9, -8.9, -1.8, -6.3],
                                             [-6.3, -1.8, -8.9, -8.9, -1.8, -6.3],
                                             [-6.1, -1.4, -8.7, -8.7, -1.4, -6.1]])*fac[3]

                                # Beam Distributed Loads - kN/m
                                # Beam distributed loads are calculated as combination of the beam self weights and
                                # and the loads acting on the beams from the slabs. When the span lengths are increased
                                # with factor fac[3], the beam distributed loads will also increase because of the slab
                                # contribution on the total load. For the sake of simplicity, even when the span length is changed,
                                # the beam dimensions are kept constant and the beam distributed laods are increased only by half of the
                                # factor fac[3]. It should be noted that Bal et al. (2008, published report of IUSS and the paper in SDEE)
                                # show that there is no significant correlation between the beam section depth
                                # and the span length. The reasons for this are explaiend in the referred publications.
                                Wz=np.array([[-7.8, -8.3, -7.3, -8.1, -8.2],
                                             [-7.8, -8.3, -7.3, -8.1, -8.2],
                                             [-7.8, -8.3, -7.3, -8.1, -8.2],
                                             [-7.8, -8.3, -7.3, -8.1, -8.2],
                                             [-7.8, -8.3, -7.3, -8.1, -8.2],
                                             [-7.8, -8.3, -7.3, -8.1, -8.2],
                                             [-7.8, -8.3, -7.3, -8.1, -8.2],
                                             [-7.5, -8.1, -7.1, -7.9, -7.9]])*(1+(fac[3]-1)/2)

                                # Column section number assignments (from bottom to top)
                                # Number of rows of the below matrix is equal to number of floors
                                Column_Sections=[[1, 2, 3, 3, 2, 1],
                                                 [1, 2, 3, 3, 2, 1],
                                                 [1, 2, 3, 3, 2, 1],
                                                 [4, 5, 6, 6, 5, 4],
                                                 [4, 5, 6, 6, 5, 4],
                                                 [4, 5, 6, 6, 5, 4],
                                                 [7, 7, 8, 8, 7, 7],
                                                 [7, 7, 8, 8, 7, 7]]

                                # Beam section number assignments (from bottom to top)
                                # Number of rows of the below matrix is equal to number of floors
                                Beam_Sections=[ [9, 10, 10, 10, 9],
                                                [9, 10, 10, 10, 9],
                                                [9, 10, 10, 10, 9],
                                                [9, 10, 10, 10, 9],
                                                [9, 10, 10, 10, 9],
                                                [9, 10, 10, 10, 9],
                                                [9, 10, 10, 10, 9],
                                                [9, 10, 10, 10, 9],]

                                # Column section dimensions
                                Col_Widths=np.array([0.25, 0.25, 1.00, 0.25, 0.25, 0.80, 0.25, 0.60])
                                Col_Depths=np.array([1.05, 0.95, 0.25, 0.90, 0.80, 0.25, 0.60, 0.25])

                                # Change the column dimensions in steps of 5cm in the parametric analysis
                                # Linearly correlated with the span and transverse length change, fac[3]
                                Col_Widths=np.round(Col_Widths*fac[3]*20, 0)/20
                                Col_Depths=np.round(Col_Depths*fac[3]*20, 0)/20

                                # Column reinforcement
                                # Number of rows of this matrix has to be equal to the number of column sections, since each row corresponds to rebars of one column section
                                # Each row has 15 values, which are as:
                                #       Number of Top Rebars           , Diameter, MatTag
                                #       Number of Side-Top Rebars      , Diameter, MatTag  -> This is the total rebars on both edges
                                #       Number of Side-Middle Rebars   , Diameter, MatTag  -> This is the total rebars on both edges
                                #       Number of Side-Bottom Rebars  , Diameter, MatTag  -> This is the total rebars on both edges
                                #       Number of Bottom Rebars        , Diameter, MatTag
                                Col_Rebars=[ [5, fi16, 3, 2, fi14, 3, 4, fi14, 3, 2, fi14, 3, 5, fi16, 3],
                                             [6, fi16, 3, 2, fi14, 3, 0, fi14, 0, 2, fi14, 3, 6, fi16, 3],
                                             [5, fi16, 3, 2, fi14, 3, 0, fi14, 3, 2, fi14, 3, 5, fi16, 3],
                                             [4, fi16, 3, 2, fi14, 3, 2, fi14, 3, 2, fi14, 3, 4, fi16, 3],
                                             [5, fi16, 3, 2, fi14, 3, 0, fi14, 3, 2, fi14, 3, 5, fi16, 3],
                                             [3, fi16, 3, 2, fi14, 3, 0, fi14, 3, 2, fi14, 3, 3, fi16, 3],
                                             [3, fi16, 3, 2, fi14, 3, 0, fi14, 3, 2, fi14, 3, 3, fi16, 3],
                                             [3, fi16, 3, 2, fi14, 3, 0, fi14, 3, 2, fi14, 3, 3, fi16, 3]]

                                # Slab thickness	es of the T-beam sections
                                Hs=[0.12, 0.12]

                                # Clear beam depth from the bottom face of the slab to the bottom face of the beam (m)
                                Hb=[0.38, 0.38]

                                # Effective slab width (m)
                                Bs=[0.70, 0.70]

                                # Beam width at the bottom (m)
                                Bw=[0.25, 0.25]

                                # Beam reinforcement
                                # Number of rows of this matrix has to be equal to the number of beam sections, since each row corresponds to rebars of one beam section
                                # Each row has 12 values, which are as:
                                #       Number of Top Rebars       , Diameter, MatTag
                                #       Number of Slab Rebars      , Diameter, MatTag
                                #       Number of Beam Body Rebars , Diameter, MatTag
                                #       Number of Bottom Rebars    , Diameter, MatTag
                                Beam_Rebars=[ [2, fi16, 3, 4, fi8, 3, 0, 0, 0, 2, fi16, 3],
                                              [4, fi16, 3, 4, fi8, 3, 0, 0, 0, 3, fi16, 3]]

                                # Meshing parameters
                                np_int=5		    # number of gauss-lobatto points
                                distance=0.015	# meshing size for the fibers

                                ##############################################################################
                                ##############################################################################
                                ## MATERIALS                                                                ##
                                ##############################################################################
                                ##############################################################################
                                fpc=fc*K

                                # epsc0 is the strain at compressive strength (negative value)
                                epsc0=-0.002*(1+5*(K-1))	# from Pauly and Priestly, 1992, which is modified from Mander Model

                                # epsU is the strain at crushing strength (negative value)
                                epsU=-0.004-0.0014*K		# Modified from Pauly and Priestly, 1992, and Turkish EQ Code, Chapter 7

                                # fcu, which represents the concrete compr. stregnth at hoop failure, is assumed as fcc*(0.6*K) for the sake of simplification

                                ################ Define materials for nonlinear columns ####################
                                # CONCRETE,,,,   tag,   fcc,   ec0,,  f'cu,,,epsu, ratio,, ftens,,espst0,, ft0,,beta  ulttens

                                # uniaxialMaterial Concrete02 matTag fpc epsc0,fpcu   ,epscu lambda ft Ets
                                os.uniaxialMaterial('Concrete02',1,fpc,epsc0,fpc*0.3*K,epsU,0.4,3000,1000),
                                # Confined concrete
                                os.uniaxialMaterial('Concrete01',2,fc,-0.002,0,-0.004)
                                # Reinforcement steel (Giuffrè-Menegotto-Pinto model)
                                Es=2e8
                                R0=30
                                cR1=0.9
                                cR2=0.15; # Giuffrè-Menegotto-Pinto parameter R0
                                os.uniaxialMaterial('Steel02',3,fy,Es,0.005,R0,cR1,cR2)

                                ##############################################################################
                                ##############################################################################
                                ## WEIGHTS & MASSES                                                         ##
                                ##############################################################################
                                ##############################################################################

                                # Find the axis positions
                                Axes=np.append(0,np.cumsum([Lengths]))

                                # Find the floor levels
                                Levels=np.append(0,np.cumsum([Heights]))
                                
                                # Calculate the column self-weights for mass calculations - Nsf
                                N_sf=np.zeros((len(Column_Sections), len(Column_Sections[0])))
                                for i in range(len(Column_Sections)):
                                    for j in range(len(Column_Sections[0])):
                                        volume=Col_Widths[Column_Sections[i][j]-1]*Col_Depths[Column_Sections[i][j]-1]
                                        N_sf[i][j]=-1*volume*Heights[i]*24

                                # Calculate the column loads from beam distributed loads, Wz
                                # These loads are used only for calculating the column-top masses
                                # They are not added as column top loads as beam distributed loads
                                # are already defined as element distributed loads for beams
                                N_wz=np.zeros((len(Levels)-1, len(Axes)))
                                for i in range(len(Levels)-1):
                                    for j in range(len(Axes)):
                                        if j==0:  # If the left-most column
                                            N_wz[i][j]=-1*LRB_weight[0]*Left_Right_Balconies[0]+Wz[i][j]*Lengths[j]/2
                                        elif j==len(Axes)-1:  # If the right-most column
                                            N_wz[i][j]=-1*LRB_weight[1]*Left_Right_Balconies[1]+Wz[i][j-1]*Lengths[j-1]/2
                                        else:
                                            N_wz[i][j]=Wz[i][j-1]*Lengths[j-1]/2+Wz[i][j]*Lengths[j]/2

                                # Column top point load sum
                                N_col=N0+N_sf+N_wz

                                # Colum top lumped masses in tonnes
                                M_lumped=(N_col)*-1/9.81

                                ##############################################################################
                                ##############################################################################
                                ## NODES                                                                    ##
                                ##############################################################################
                                ##############################################################################

                                # Create the nodes & assign the masses
                                nd_counterX=0
                                total_mass_check=0
                                for x in Axes:
                                    nd_counterX+=1
                                    nd_counterY=0
                                    for y in Levels:
                                        nd_counterY+=1
                                        node_no=(nd_counterY-1)*100+nd_counterX
                                        os.node(node_no, Axes[nd_counterX-1], Levels[nd_counterY-1])
                                        if y>0:
                                            os.mass(node_no, M_lumped[nd_counterY-2][nd_counterX-1], M_lumped[nd_counterY-2][nd_counterX-1], 0)
                                            # Check the total mass of the frame
                                            total_mass_check=total_mass_check+M_lumped[nd_counterY-2][nd_counterX-1]

                                # Fix the base
                                os.fixY(0,1,1,1)

                                ##############################################################################
                                ##############################################################################
                                ## SECTIONS                                                                 ##
                                ##############################################################################
                                ##############################################################################

                                # Define cross-section for nonlinear columns

                                # Call the relevant section function
                                print('reached till section def')
