# EXAMPLE 3
# In this example, open a SOWFA case including all meta-data
# Show the data
# PLot the flow with turbine positions indicated


# DOES NOT WORK?
# import wind_farm_controls_tools as wfct #Why doesn't this way work?
# sowfa_case = wfct.sowfa_utilities.SowfaInterface('sowfa_example')

# This seems to work:
#TODO Super ugly though get to an "as" type import
from wind_farm_controls_tools.sowfa_utilities import SowfaInterface
from wind_farm_controls_tools.visualization import plot_turbines
from wind_farm_controls_tools.cut_plane import HorPlane
import matplotlib.pyplot as plt

# Load the sowfa case in
sowfa_case = SowfaInterface('sowfa_example')

# Plot the flow and turbines using the input information
fig, ax = plt.subplots()
flow_field = sowfa_case._flow_field
hor_plane = HorPlane(flow_field,90)
hor_plane.visualize(ax=ax)
plot_turbines(ax, sowfa_case.layout_x, sowfa_case.layout_y, sowfa_case.yaw_angles, sowfa_case.D)

plt.show()

# Describe self
# sowfa_case.describe()
print(sowfa_case)