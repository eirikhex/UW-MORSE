# UW-MORSE

This repository contains UW MORSE. UW MORSE is an simulation environment for underwater robots. 

The code is NOT very good documented, nor supported. 

The simulation environmnet contains tree parts:
- a fork of the morse simulator (https://www.openrobots.org/wiki/morse) 
- a fork of blender, with a modified physics engine for enabling underwater physics (https://www.blender.org)
- scenarios folder containig underwater simulation environments and modules

### Installation

1. clone/fork the git repository
2. init, and update submodules
3. compile blender
4. Install necessary middleware (MOOS: http://www.moos-ivp.org ROS: http://www.ros.org/ )
5. compile and install morse fork
6. Run simulations in scenarios folder
7. Make you own simulations
8. Share your work, I will accept PRs

If the environment is used, a reference to this repository or to this article is appreciated:

E. H. Henriksen, I. Schjølberg and T. B. Gjersvik, "UW MORSE: The underwater Modular Open Robot Simulation Engine," 2016 IEEE/OES Autonomous Underwater Vehicles (AUV), Tokyo, 2016, pp. 261-267.
doi: 10.1109/AUV.2016.7778681
URL: http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7778681&isnumber=7778649
