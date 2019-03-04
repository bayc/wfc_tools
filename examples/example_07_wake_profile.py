#
# Copyright 2019 NREL
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#

## Example 07
## Wake profile
## In this example:
## 1) Load the SOWFA and FLORIS model
## 2) Make the FLORIS to match the SOWFA simulation setup
## 3) Get vertical cut planes at 3 and 5 D
## 3) Compare the wake profiles at 3 and 5 D

import wind_farm_controls_tools as wfct
import wind_farm_controls_tools.visualization as vis
import matplotlib.pyplot as plt
import numpy as np


# Load SOWFA
sowfa_case = wfct.sowfa_utilities.SowfaInterface('sowfa_example')
sowfa_flow_field = sowfa_case.flow_field #TODO Correct?


# # Load FLORIS
# #TODO Make match SOWFA (waiting for earlier example to copy from)
floris_interface = wfct.floris_utilities.FlorisInterface("example_input.json")

# Set the relevant FLORIS parameters to equal the SOWFA case
floris_interface.floris.farm.set_wind_speed(sowfa_case.precursor_wind_speed, calculate_wake=False)
floris_interface.floris.farm.set_wind_direction(sowfa_case.precursor_wind_dir, calculate_wake=False)
floris_interface.floris.farm.set_turbine_locations(sowfa_case.layout_x, sowfa_case.layout_y, calculate_wake=False)
floris_interface.floris.farm.set_yaw_angles(np.radians(sowfa_case.yaw_angles), calculate_wake=False)
floris_interface.run_floris()
floris_flow_field = floris_interface.get_flow_field(resolution=sowfa_flow_field.resolution)

# # Confirm the flows compare
fig, axarr = plt.subplots(2,2)
ax=axarr[0,0]
hor_plane = wfct.cut_plane.HorPlane(sowfa_flow_field, 90)
wfct.visualization.visualize_cut_plane(hor_plane,ax=ax)
vis.plot_turbines(ax, sowfa_case.layout_x, sowfa_case.layout_y, sowfa_case.yaw_angles, sowfa_case.D)
ax.set_title('SOWFA')
ax=axarr[0,1]
hor_plane = wfct.cut_plane.HorPlane(floris_flow_field, 90)
wfct.visualization.visualize_cut_plane(hor_plane,ax=ax)
vis.plot_turbines(ax, floris_interface.floris.farm.layout_x, floris_interface.floris.farm.layout_y, floris_interface.get_yaw_angles(), floris_interface.floris.farm.turbine_map.turbines[0].rotor_diameter)
ax.set_title('FLORIS')


# Grab floris turbine cp/ct tables
# TODO for now assume only one turbine, is this how to do this?
# print(floris_interface.floris.farm.turbines)
for turbine in floris_interface.floris.farm.turbines: # turbine_map.items():
    floris_ws = turbine.power_thrust_table["wind_speed"]
    floris_ct = turbine.power_thrust_table["thrust"]
    floris_cp = turbine.power_thrust_table["power"]


# # Determine the cut planes distances for 7 D
# D = sowfa_case.D

# # Get the 5 values
D = sowfa_case.D 
sowfa_cross_5 = wfct.cut_plane.CrossPlane(sowfa_flow_field,5 * D + sowfa_case.layout_x[0])
floris_cross_5 = wfct.cut_plane.CrossPlane(floris_flow_field,5 * D + sowfa_case.layout_x[0])

# Visuzlie
ax=axarr[1,0]
wfct.visualization.visualize_cut_plane(sowfa_cross_5,ax=ax)
ax=axarr[1,1]
wfct.visualization.visualize_cut_plane(floris_cross_5,ax=ax)

# Map out the power function
def get_pow(cross_plane,x1_loc):
    return wfct.cut_plane.calculate_power(cross_plane,x1_loc=x1_loc,x2_loc=90,R=D/2.,ws_array=floris_ws,cp_array=floris_cp)

# Now get the profiles in power
y_points = np.linspace(sowfa_case.layout_x[0]-2*D,sowfa_case.layout_x[0]+2*D,100)
sowfa_pow = np.array([get_pow(sowfa_cross_5,x) for x in y_points])
floris_pow = np.array([get_pow(floris_cross_5,x) for x in y_points])
print(floris_pow)

# Compare the profiles
fig, ax = plt.subplots()
ax.plot(y_points,sowfa_pow,color='k',label='SOWFA')
ax.plot(y_points,floris_pow,color='r',label='FLORIS')
ax.grid(True)
ax.legend()
wfct.visualization.reverse_cut_plane_x_axis_in_plot(ax)

plt.show()