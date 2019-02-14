## Demonstrate flow subtraction

# In this example
# 1) Load the FLORIS model
# 2) Set the simulation to have only 1 turbine
# 3) Get a flow field for normal, and 20 deg yaw
# 4) Using overloaded subtraction, get the difference (20-baseline) flow field
# 5) Get a cut-through (vertical cut plane ) at 7 D downstream from 0-yaw, 20-deg, and subtracted flow field
# 6) Using overloaded subtraction, make a difference cut plane and confirm it matches the cut plane derived from the subtracted flow-field
