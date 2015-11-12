# evocrimesim
A model in Python with a GUI in Pygame. The system is a model for cop, robber and civilian agents interacting in a city grid environment. It was created as a BSc dissertation at Imperial College London in 2015.

The model is presented in this project report https://www.dropbox.com/s/hb1d6mk6wwo7n0o/Comp%20Evo%20Project.pdf?dl=0

Instructions

The following key presses enable interaction with the simulation.

General use:

"p" - Pause/Play
"d" - Toggle display on and off
"click" - Clicking on any agent when paused will print the agents status and genes in the console

NOTE: In order to progress the simulation considerably toggle the display off by pausing, hitting "d" and the pausing once more. The progress in iteration count may be followed by print statements in the console.

Plotting:

"s" - Plots gene maps of the robbers gene space.
"z" - Creates a 3d plot of the robbers gene space
"m" - Creates a heatmap of arrests in the simulation
"c" - Creates a heatmap of crime in the simulation
"x" - Plots populations of agents against iteration count (main loop cycles)
"a" - Plots cop vision against cop speed genes
"f" - Manual redistribution of houses in the city
