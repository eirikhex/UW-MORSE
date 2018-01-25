def read_config_file(filename="inputFile.txt",verbose=False):

    ########################################################
    ################   GET SPECIFICATIONS   ################
    ########################################################
    
    specs = {};
    
    file=open(filename, "r")
    lines=file.readlines()
    if verbose:
        print("reading file ", file.name)
        print("Specifications for   ", lines[2])

    
    #initial pose
    dummy=lines[4].split()
    poseNED=[float(dummy[0]), float(dummy[1]), float(dummy[2]), float(dummy[3]), float(dummy[4]), float(dummy[5])]
    poseENU=[poseNED[1], poseNED[0], -poseNED[2], poseNED[4], poseNED[3], -poseNED[5]] 
    
    specs["pose_NED"] = poseNED
    specs["pose_ENU"] = poseENU
    
    if verbose:
        print("Initial pose(NED) set to:  ", poseNED)
    
    
    #initial velocity
    dummy=lines[6].split()
    velocity=[float(dummy[0]), float(dummy[1]), float(dummy[2]), float(dummy[3]), float(dummy[4]), float(dummy[5])]
    specs["velocity"] = velocity
    if verbose:
        print("Initial velocity is ", velocity)
    
    #Mass Matrix
    dummy1=lines[8].split()
    dummy2=lines[9].split()
    dummy3=lines[10].split()
    dummy4=lines[11].split()
    dummy5=lines[12].split()
    dummy6=lines[13].split()
    MassMatrix=[[float(dummy1[0]), float(dummy1[1]), float(dummy1[2]), float(dummy1[3]), float(dummy1[4]), float(dummy1[5])],   
         [float(dummy2[0]), float(dummy2[1]), float(dummy2[2]), float(dummy2[3]), float(dummy2[4]), float(dummy2[5])],
         [float(dummy3[0]), float(dummy3[1]), float(dummy3[2]), float(dummy3[3]), float(dummy3[4]), float(dummy3[5])],
         [float(dummy4[0]), float(dummy4[1]), float(dummy4[2]), float(dummy4[3]), float(dummy4[4]), float(dummy4[5])],
         [float(dummy5[0]), float(dummy5[1]), float(dummy5[2]), float(dummy5[3]), float(dummy5[4]), float(dummy5[5])], 
         [float(dummy6[0]), float(dummy6[1]), float(dummy6[2]), float(dummy6[3]), float(dummy6[4]), float(dummy6[5])]]
    
    specs["Mass_Matrix"] = MassMatrix
    
    if verbose:
        print("M_rb set to \n ", MassMatrix)
    
    
    #Added mass matrix
    dummy1=lines[15].split()
    dummy2=lines[16].split()
    dummy3=lines[17].split()
    dummy4=lines[18].split()
    dummy5=lines[19].split()
    dummy6=lines[20].split()
    M_a=[[float(dummy1[0]), float(dummy1[1]), float(dummy1[2]), float(dummy1[3]), float(dummy1[4]), float(dummy1[5])],   
         [float(dummy2[0]), float(dummy2[1]), float(dummy2[2]), float(dummy2[3]), float(dummy2[4]), float(dummy2[5])],
         [float(dummy3[0]), float(dummy3[1]), float(dummy3[2]), float(dummy3[3]), float(dummy3[4]), float(dummy3[5])],
         [float(dummy4[0]), float(dummy4[1]), float(dummy4[2]), float(dummy4[3]), float(dummy4[4]), float(dummy4[5])],
         [float(dummy5[0]), float(dummy5[1]), float(dummy5[2]), float(dummy5[3]), float(dummy5[4]), float(dummy5[5])], 
         [float(dummy6[0]), float(dummy6[1]), float(dummy6[2]), float(dummy6[3]), float(dummy6[4]), float(dummy6[5])]]
    
    specs["Added_Mass"] = M_a
    
    if verbose:
        print(" Added mass is set to: \n", M_a)
    
    
    #Linear damping matrix
    dummy1=lines[22].split()
    dummy2=lines[23].split()
    dummy3=lines[24].split()
    dummy4=lines[25].split()
    dummy5=lines[26].split()
    dummy6=lines[27].split()
    D_lin=[[float(dummy1[0]), float(dummy1[1]), float(dummy1[2]), float(dummy1[3]), float(dummy1[4]), float(dummy1[5])],   
         [float(dummy2[0]), float(dummy2[1]), float(dummy2[2]), float(dummy2[3]), float(dummy2[4]), float(dummy2[5])],
         [float(dummy3[0]), float(dummy3[1]), float(dummy3[2]), float(dummy3[3]), float(dummy3[4]), float(dummy3[5])],
         [float(dummy4[0]), float(dummy4[1]), float(dummy4[2]), float(dummy4[3]), float(dummy4[4]), float(dummy4[5])],
         [float(dummy5[0]), float(dummy5[1]), float(dummy5[2]), float(dummy5[3]), float(dummy5[4]), float(dummy5[5])], 
         [float(dummy6[0]), float(dummy6[1]), float(dummy6[2]), float(dummy6[3]), float(dummy6[4]), float(dummy6[5])]]
    
    specs["Linear_Damping"] = D_lin
    
    if verbose:
        print(" Linear damping matrix is set to: \n", D_lin)
    
    
    #Quadratic damping matrix
    dummy1=lines[29].split()
    dummy2=lines[30].split()
    dummy3=lines[31].split()
    dummy4=lines[32].split()
    dummy5=lines[33].split()
    dummy6=lines[34].split()
    D_quad=[[float(dummy1[0]), float(dummy1[1]), float(dummy1[2]), float(dummy1[3]), float(dummy1[4]), float(dummy1[5])],   
         [float(dummy2[0]), float(dummy2[1]), float(dummy2[2]), float(dummy2[3]), float(dummy2[4]), float(dummy2[5])],
         [float(dummy3[0]), float(dummy3[1]), float(dummy3[2]), float(dummy3[3]), float(dummy3[4]), float(dummy3[5])],
         [float(dummy4[0]), float(dummy4[1]), float(dummy4[2]), float(dummy4[3]), float(dummy4[4]), float(dummy4[5])],
         [float(dummy5[0]), float(dummy5[1]), float(dummy5[2]), float(dummy5[3]), float(dummy5[4]), float(dummy5[5])], 
         [float(dummy6[0]), float(dummy6[1]), float(dummy6[2]), float(dummy6[3]), float(dummy6[4]), float(dummy6[5])]]
    
    specs["Quadratic_Damping"] = D_quad
    
    if verbose:
        print("Quadratic damping matrix is set to: \n", D_quad)
    
    
    #Centre of Gravity
    dummy=lines[36].split()
    COG=[float(dummy[0]), float(dummy[1]), float(dummy[2])]
    
    specs["Centre_of_Gravity"] = COG
    
    
    #Centre of Buoyancy
    dummy=lines[38].split()
    COB=[float(dummy[0]), float(dummy[1]), float(dummy[2])]
    
    specs["Centre_of_Buoyancy"] = COB
    
    #ROV Volume
    Volume=float(lines[40])
    specs['Volume'] = Volume
    if verbose:
        print("Volume is ", Volume)
    
    
    #Thruster allocations
    thrusterN=int(lines[42])
    ThrustAll=[[0 for x in range(thrusterN)] for x in range(6)]
    
    dummy1=lines[44].split()
    dummy2=lines[45].split()
    dummy3=lines[46].split()
    dummy4=lines[47].split()
    dummy5=lines[48].split()
    dummy6=lines[49].split()
    
    
    
    for i in range (0, thrusterN):
        ThrustAll[0][i]=float(dummy1[i])
        ThrustAll[1][i]=float(dummy2[i])
        ThrustAll[2][i]=float(dummy3[i])
        ThrustAll[3][i]=float(dummy4[i])
        ThrustAll[4][i]=float(dummy5[i])
        ThrustAll[5][i]=float(dummy6[i])
    
    specs["Number_of_Thrusters"] = thrusterN
    specs["Thrust_allocation_matrix"] = ThrustAll
    
    #Diameters
    dummy=lines[51].split()
    diameters=[]
    for i in range (0, thrusterN):
        diameters.append(float(dummy[i]))
    
    if verbose:
        print("Number of thrusters:  ", thrusterN)  
        print("Diameter for thrusters: ")
        print(diameters)
    
    specs['Thruster_Diameters'] = diameters
    
    
    #Thrust coefficient function
    dummy1=lines[53].split()
    dummy2=lines[54].split()
    K_t=[[float(dummy1[0]), float(dummy1[1]), float(dummy1[2]), float(dummy1[3])],[float(dummy2[0]), float(dummy2[1]), float(dummy2[2]), float(dummy2[3])]]
    
    specs["K_t"] = K_t
    
    if verbose:
        print("thrust coeff function:")
        print("K_t= ", K_t[0][0], " JÂ³ + ", K_t[0][1], " JÂ² +", K_t[0][2], " J +", K_t[0][3], "\t \t (n>0)")
        print("K_t= ", K_t[1][0], " JÂ³ + ", K_t[1][1], " JÂ² +", K_t[1][2], " J +", K_t[1][3], "\t \t (n<0)")
    
    #Thrust loss factors
    dummy1=lines[56].split()
    dummy2=lines[57].split()
    theta=[[0 for x in range(thrusterN)] for x in range(2)]
    for i in range (0, thrusterN):
        theta[0][i]=float(dummy1[i])
        theta[1][i]=float(dummy2[i])
    
    specs["Thrust_loss_factors"] = theta
    
    if verbose:
        print("thrust loss factors:")
        print(theta)
    
    #RPM limits
    dummy1=lines[59].split()
    dummy2=lines[60].split()
    RPMlim=[[0 for x in range(thrusterN)] for x in range(2)]
    for i in range (0, thrusterN):
        RPMlim[0][i]=float(dummy1[i])
        RPMlim[1][i]=float(dummy2[i])
      
    specs["RPM_Limits"] = RPMlim
    
    if verbose:
        print("RPM limits:")
        print(RPMlim)
    
    
    ##########################################
    file.close()
    return specs
    ##########################################