# README #

This repository contains simulation scenarios for the Underwater MORSE simulator. 

### Organization  of Repository###

 Currently organized by middleware (ROS/MOOS)

### Tips and tricks ###

To make a link in the local Morse to the simulation environments run: `morse create <MOOS/ROS>/<scenario name>`

example: `morse create MOOS/subsea`  

This will return an error: `* A directory called "MOOS/subsea" already exists!` But will still make the link.

It is now possible to run the scenario by the command:
`morse run MOOS/subsea`